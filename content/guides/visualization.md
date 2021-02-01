---
$title@: Visualization
$category: Access
---

[TOC]

### Neuroglancer

[Neuroglancer](https://github.com/google/neuroglancer) is a browser-based application utilizing WebGL for viewing 3D imaging volumes, meshes, segmentations and annotations.  It supports a number of data sources, including [BOSS](https://bossdb.org), [render](https://github.com/saalfeldlab/render), [precomputed](https://github.com/google/neuroglancer/tree/master/src/neuroglancer/datasource/precomputed), [N5](https://github.com/saalfeldlab/n5) and [nifti](https://nifti.nimh.nih.gov/) files.

NeuroData maintains a Neuroglancer [fork](https://github.com/neurodata/neuroglancer), hosted at [viz.neurodata.io](https://viz.neurodata.io).  This version has the following customizations:

1. Color customization interface (useful for colorizing multiple overlaid channels)
1. Export state to JSON
1. Export and load state to/from an external JSON server
1. Segmentation overlays for ARA and Zbrain ontologies, at [ara.viz.neurodata.io](https://ara.viz.neurodata.io) and [zbrain.viz.neurodata.io](https://zbrain.viz.neurodata.io)

### View Local Images in Neuroglancer Example

The following example can be used to help you view your own images in neuroglancer. This example uses a <a href="/static/guides/downloadable_files/upload.py" download>script</a> to generate a test image, then convert from tif to precomputed format. You will need to use Python 3, and install all the dependencies of the script, including tifffile, cloudvolume, and joblib. It will also require running a [script](https://github.com/google/neuroglancer/blob/master/cors_webserver.py)  from neuroglancer to host the local data:

1. mkdir ./test_output
1. python upload.py precomputed://file://test_output/
1. cd ./test_output
1. python \*\*path to neuroglancer\*\*/cors_webserver.py

At this point, the data can be viewed in neuroglancer:

1. Navigate to a place where neuroglancer is hosted, e.g. [viz.neurodata.io/](https://viz.neurodata.io/)
1. Click the "+" icon to add a source
1. In the Source field, type precomputed://http://127.0.0.1:9000
1. In the green bar above the Source field, make sure the source format is selected to be "image" (not "new" or "auto" etc.)

If you see a 10x10x10 cube of random grayscale intensities, the example succeeded.

### Selected links

The following URLs link to highlighted visualizations

1. [Lee16](https://viz.neurodata.io/#!%7B%22layers%22:%5B%7B%22source%22:%22precomputed://https://open-neurodata.s3.amazonaws.com/lee/lee16/image%22%2C%22type%22:%22image%22%2C%22blend%22:%22default%22%2C%22name%22:%22lee16%22%7D%5D%2C%22navigation%22:%7B%22pose%22:%7B%22position%22:%7B%22voxelSize%22:%5B4%2C4%2C40%5D%2C%22voxelCoordinates%22:%5B88876.0703125%2C84433.4609375%2C544.1320190429688%5D%7D%7D%2C%22zoomFactor%22:80.34214769275067%7D%2C%22perspectiveOrientation%22:%5B-0.20964106917381287%2C0.42196616530418396%2C0.12354789674282074%2C0.8733447790145874%5D%2C%22perspectiveZoom%22:992.2747156050259%2C%22layout%22:%224panel%22%7D): Over 20 trillion voxel serial EM dataset
1. [zbrain](https://zbrain.viz.neurodata.io/?json_url=https://json.neurodata.io/v1?NGStateID=daDgh1R0VeRGYQ) Zebrafish Atlas (by Owen Randlett), meshed and overlaid with light data channels
1. [synaptomes](https://viz.neurodata.io/?json_url=https://json.neurodata.io/v1?NGStateID=TV8ahpiXYtyclw): Manually annotated synapses on Electron Microsopy coregistered with array tomography
<!-- 1. [synaptomes](https://viz.neurodata.io/?json_url=https://api.myjson.com/bins/17xtbq): Manually annotated synapses meshed and overlaid with EM and array tomography -->
1. [ARA](https://ara.viz.neurodata.io/?json_url=https://json.neurodata.io/v1?NGStateID=s4m0p-iQnlqCMg) Allen Reference Atlas meshed
<!-- 1. [Cell detections](https://viz.neurodata.io/?json_url=https://api.myjson.com/bins/89y6u) Point annotations representing cell detections of different regions of light data overlaid with the Allen Reference Atlas.   -->

### Annotation features

Please see our guides for some additional neuroglancer features

1. [Add point annotations from within Neuroglancer]([url('/content/guides/neuroglancer-pt-annotations.md')])
1. [Add point annotations programmatically]([url('/content/guides/programmatic-neuroglancer-annotations.md')])
1. [Create precomputed volume]([url('/content/guides/precomputed.md')])