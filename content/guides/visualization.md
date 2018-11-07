---
$title@: Visualization
$category: Access
---

[TOC]

### Neuroglancer

[Neuroglancer](https://github.com/google/neuroglancer) is a browser-based application utilizing WebGL for viewing 3D imaging volumes, meshes, segmentations and annotations.  It supports a number of data sources, including BOSS, render, precomputed, and nifti files.

NeuroData maintains a [fork](https://github.com/neurodata/neuroglancer), hosted at [viz.neurodata.io](https://viz.neurodata.io).  This version has the following customizations:

1. Color customization interface (useful for colorizing multiple overlaid channels)
1. Export state to JSON
1. Export and load state to/from an external JSON server

To load data into neuroglancer from our BOSS deployment, we recommend using [ndwebtools](https://ndwebtools.neurodata.io), as specifying the data links in the neuroglancer interface by hand is error-prone.

### Selected links

The following URLs link to highlighted visualizations

1. [Lee16](https://ndwebtools.neurodata.io/ndviz_url/lee/lee16/image/): Over 20 trillion voxel serial EM dataset
1. [zbrain](https://viz.neurodata.io/?json_url=https://api.myjson.com/bins/13225y) Zebrafish Atlas (by Owen Randlett), meshed and overlaid with light data channels
<!-- 1. [synaptomes](https://viz.neurodata.io/?json_url=https://api.myjson.com/bins/17xtbq): Manually annotated synapses meshed and overlaid with EM and array tomography -->
1. [ARA](https://viz.neurodata.io/?json_url=https://api.myjson.com/bins/fwaqe) Allen Reference Atlas meshed
<!-- 1. [Cell detections](https://viz.neurodata.io/?json_url=https://api.myjson.com/bins/89y6u) Point annotations representing cell detections of different regions of light data overlaid with the Allen Reference Atlas.   -->

### Annotation features

Please see our guides for some additional neuroglancer features

1. [Add point annotations from within Neuroglancer]([url('/content/guides/neuroglancer-pt-annotations')])
1. [Add point annotations programmatically]([url('/content/guides/programmatic-neuroglancer-annotations')])
1. [Create precomputed volume]([url('/content/guides/boss-to-precompute')])