---
$title@: Precomputed neuroglancer format
$category: Storage
$order: 2
---

[TOC]

The precomputed format [specification](https://github.com/google/neuroglancer/tree/master/src/neuroglancer/datasource/precomputed) is a data source format for loading data into [neuroglancer](https://github.com/google/neuroglancer).  This page documents how to generate precomputed compressed segmentations & meshes.

>Cloud-Volume: This guide utilizes `neuroglancer-scripts`, however [Cloud-Volume](https://github.com/seung-lab/cloud-volume) currently has better scaling and is preferred

### Steps

1. Generate the precomputed compressed segmentation files using `neuroglancer-scripts`
1. Generate meshes using `neuroglancer python` and custom script
1. Host them somewhere and point neuroglancer at the directory

### Prerequisites

Install the following software:

1. [python3](https://www.python.org/)
1. Create Python virtual environment
    - `python3 -m venv env/`
    - `. env/bin/activate`
1. [neuroglancer-scripts](https://github.com/HumanBrainProject/neuroglancer-scripts)
    - **install dev version** (pypi version has bugs)
        - `git clone https://github.com/HumanBrainProject/neuroglancer-scripts.git`
        - `cd neuroglancer-scripts`
        - `pip install -e .[dev]`
1. [neuroglancer](https://github.com/google/neuroglancer) (for meshing)
    1. Optional:
        1. [node](https://nodejs.org/) (package for [Ubuntu](https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions))
        1. install Java (needed for webpack)
        1. run the install scripts from neuroglancer root directory (`npm i`)
        1. start the web server `npm run dev-server` (this compiles webpack)
    1. navigate to python directory and run (installs neuroglancer package)
        1. `pip install numpy tornado==4.5.3`
        1. `python setup.py develop`
        1. `python setup.py bundle_client`

### Create compressed segmentations

1. Create basic `info` file:

        {
            "encoding": "compressed_segmentation",
            "scales": [
                {
                    "voxel_offset": [0,0,0],
                    "resolution": [798,798,2000],
                    "size": [1406,621,138]
                }
            ],
            "compressed_segmentation_block_size": [8,8,8],
            "data_type": "uint64",
            "mesh": "mesh",
            "type": "segmentation",
            "num_channels": 1
        }

1. Create additional scales (chunk size 128)

    `mkdir output; generate-scales-info info output --target-chunk-size 128`

1. Create res 0 precomputed data:

    `slices-to-precomputed data/ output/ --flat`

1. Create the downsampled data:

    `compute-scales --flat --downscaling-method majority output/`

### Create the meshes using neuroglancer

1. create mesh directory
    `mkdir mesh`
1. change directory to `neuroglancer/python`
1. run the following script: `python mesh.py DATA/ XXX YYY ZZZ`

#### `mesh.py`

```python
from pathlib import Path
import argparse

import numpy as np
import tifffile as tiff

import neuroglancer

parser = argparse.ArgumentParser(description='create meshes')
parser.add_argument('img_path_str', type=str, help='path to images')
parser.add_argument('voxel_size', nargs=3, type=int,
                    help='voxel size (x, y, z)')

args = parser.parse_args()

img_path_str = args.img_path_str
voxel_size = args.voxel_size

json_descriptor = '{{"fragments": ["mesh.{}.{}"]}}'

img_path = Path(img_path_str)

mesh_list = []
for f in sorted(img_path.glob('*.tif')):
    A = tiff.imread(str(f))
    mesh_list.append(A)
mesh = np.dstack(mesh_list)
mesh = np.transpose(mesh, (2, 0, 1))

ids = [int(i) for i in np.unique(mesh[:])]

vol = neuroglancer.LocalVolume(
    data=mesh,
    voxel_size=voxel_size,
)

img_path.parent.joinpath(
    'output', 'mesh').mkdir(exist_ok=True, parents=True)

for ID in ids[1:]:
    print(ID)
    mesh_data = vol.get_object_mesh(ID)
    with open(
            str(img_path.parent / 'output' / 'mesh' / '.'.join(
                ('mesh', str(ID), str(ID)))), 'wb') as meshfile:
        meshfile.write(mesh_data)
    with open(
            str(img_path.parent / 'output' / 'mesh' / ''.join(
                (str(ID), ':0'))), 'w') as ff:
        ff.write(json_descriptor.format(ID, ID))

print('ids to insert into URL:')
ids_string = '[\'' + '\'_\''.join([str(i) for i in ids[1:]]) + '\']'
print(ids_string)

print('done')
```

### Host the directory

#### nginx
1. Copy the `output` directory to a server to host
1. Enable CORS: [nginx config](https://enable-cors.org/server_nginx.html)
1. Enable sending compressed files in place of uncompressed files. [nginx config](https://docs.nginx.com/nginx/admin-guide/web-server/compression/#sending-compressed-files)
#### S3
<span>1.</span> Strip the .gz extension from each file (script below)

```python
# from within the output directory:
# python rename_files.py .
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('path', type=str)
args = parser.parse_args()

p = Path(args.path)
all = set(p.glob('**/*'))
mesh = set(p.glob('mesh*'))
ids_files = all-mesh

for f in ids_files:
    f.rename(f.with_suffix(''))
```

<span>2.</span> Add CORS support to the bucket (in bucket properties) -- should look something like:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<CORSRule>
    <AllowedOrigin>*</AllowedOrigin>
    <AllowedMethod>GET</AllowedMethod>
    <MaxAgeSeconds>3000</MaxAgeSeconds>
    <AllowedHeader>Authorization</AllowedHeader>
</CORSRule>
</CORSConfiguration>
```

<span>3.</span> Give the bucket read permissions using bucket policy
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::BUCKETNAME/*"
        }
    ]
}
```
<span>4.</span> Upload the directory to to the bucket

`aws s3 sync . s3://BUCKET_NAME/PROJECT_NAME --profile AWS_PROFILE`

<span>5.</span> Add metadata to all objects that are gzipped (e.g. the segments but not the meshes) to have `Content-Encoding` be `gzip` (can do this in bulk on AWS Console)

### View the output

The final URL to construct should be a neuroglancer URL with precomputed as the source.  Use the ids printed at the end of the mesh creation for the `segments` field.

Here's an examples of the json for one of our publicly available datasets:

```json
{
  "layers": {
    "EM25K": {
      "source": "precomputed://https://open-neurodata.s3.amazonaws.com/collman/collman15v2/EM25K",
      "type": "image",
      "opacity": 1,
      "blend": "additive"
    },
    "annotation": {
      "source": "precomputed://https://open-neurodata.s3.amazonaws.com/collman/collman15v2/annotation",
      "type": "segmentation"
    }
  },
  "navigation": {
    "pose": {
      "position": {
        "voxelSize": [
          2.240000009536743,
          2.240000009536743,
          70
        ],
        "voxelCoordinates": [
          2807.0712890625,
          2267.177001953125,
          13.5
        ]
      }
    },
    "zoomFactor": 44.99160289949089
  },
  "selectedLayer": {
    "layer": "EM25K"
  },
  "layout": "4panel"
}
```
