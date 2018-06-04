---
$title@: BOSS to precomputed neuroglancer format
options: 
    - name: steps
      link: steps
    - name: prerequisites
      link: prerequisites
    - name: download
      link: download-data-from-boss-using-ndpull
    - name: create
      link: create-compressed-segmentations
    - name: host
      link: host-the-directory-somewhere
    - name: view
      link: view-the-output
---


## Generate precomputed compressed segmentations & meshes from BOSS volume

### Steps

1. Download data from BOSS using `ndpull`
1. Generate the precomputed compressed segmentation files using `neuroglancer-scripts`
1. Generate meshes using `neuroglancer python` and custom script
1. Host them somewhere and point neuroglancer at the directory

### Prerequisites

Install the following software:

1. [python3](https://www.python.org/)
1. [ndpull](https://github.com/neurodata/ndpull)
    1. `pip install git+git://github.com/neurodata/ndpull.git`
1. [neuroglancer-scripts](https://github.com/HumanBrainProject/neuroglancer-scripts)
    1. install dev version
1. [neuroglancer](https://github.com/google/neuroglancer) (for meshing)
    1. [node](https://nodejs.org/) (package for [Ubuntu](https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions))
    1. install Java (needed for webpack)
    1. run the install scripts from neuroglancer root directory (`npm i`)
    1. start the web server `npm run dev-server` (this compiles webpack)
    1. navigate to python directory and run (installs neuroglancer package)
        1. `pip install numpy tornado==4.5.3`
        1. `python setup.py develop`
        1. `python setup.py bundle_client`

### Download data from BOSS using ndpull (only needed if you don't have local access to data)

1. create a project directory
1. create subdirectory for TIFF files
1. use ndpull to download the files

```sh
mkdir zbrain-project; cd zbrain-project

mkdir data

ndpull --config_file neurodata.cfg --collection ZBrain --experiment Zbrain --channel Masks --res 0 --full_extent --outdir data
```

### Create compressed segmentations

1. Create basic `info` file:

```json
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
```

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

<script src="https://gist.github.com/falkben/1fa46f4acac75a5bd5fc1d91bb7e1aef.js"></script>

### Host the directory

1. nginx
    1. Copy the `output` directory to a server to host
    1. Enable CORS: [nginx config](https://enable-cors.org/server_nginx.html)
    1. Enable sending compressed files in place of uncompressed files. [nginx config](https://docs.nginx.com/nginx/admin-guide/web-server/compression/#sending-compressed-files)
1. S3
    1. Strip the .gz extension from each file
    1. Add CORS support to the bucket (in bucket properties)
    1. Give the bucket read permissions using bucket policy
    1. Upload the directory to to the bucket
    1. Add metadata to all objects that are gzipped (e.g. the segments but not the meshes) to have `Content-Encoding` be `gzip` (can do this in bulk on AWS Console)

### View the output

The final URL to construct should be a neuroglancer URL with precomputed as the source.  Use the ids printed at the end of the mesh creation for the `segments` field