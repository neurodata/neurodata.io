---
$title@: Download
$category: Access
---

[TOC]

This page explains how to access/download data hosted by NeuroData. [Data]([url('/content/projects/ocp.yaml')]) are publicly available. We host our data on an AWS Open Data Bucket in [Neuroglancer Precomputed format](https://github.com/google/neuroglancer/tree/master/src/neuroglancer/datasource/precomputed).

#### Data listing

The open data bucket name is `open-neurodata`.

With an AWS account and the AWS [Command Line Interface](https://aws.amazon.com/cli/), one can list the projects using this command:

```sh
aws s3 ls open-neurodata
```

#### Perform a cutout

To load a cutout into an `ipython` or `jupyter` session, we suggest [CloudVolume](https://github.com/seung-lab/cloud-volume), a python interface to Neuroglancer precomputed.  

`pip install numpy cloud-volume` and run the following code:

```python
# pip install numpy tifffile cloud-volume
from cloudvolume import CloudVolume

vol = CloudVolume(
    "s3://open-neurodata/bock11/image", mip=0, use_https=True
)

# load data into numpy array
cutout = vol[65024:65536, 62464:62976, 3616:3632]
```

#### Save cutout to TIFF

```python
# pip install tifffile
import tifffile

# save cutout as TIFF
tifffile.imwrite("data.tiff", data=np.transpose(cutout))
```

#### [neuroglancer](https://viz.neurodata.io)

To visualize the data before downloading you can use neuroglancer. Links to each dataset can be found on each project's listing on [OCP]([url('/content/projects/ocp.yaml')]). Additional information on Neuroglancer can be found [here]([url('/content/guides/visualization.md')]).
