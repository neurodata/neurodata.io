---
$title@: Annotate a volume
$order: 4
---

[TOC]

This guide shows how to annotate data in a way that NeuroData can import into our processing pipelines.

>>>NOTE: This guide is based heavily on a guide written by the Nomads NeuroDataDesign team.  The original guide can be found [here](https://neurodata-annotator.readthedocs.io/en/latest/).

### Annotate with FIJI

1. Install onto your system using [https://imagej.net/Fiji/Downloads/](https://imagej.net/Fiji/Downloads/).

2. Open FIJI, and start a new blank TrakEM2.

    ![new blank](/static/images/help/new_blank.png "new blank")

3. Navigate to the folder of your image volume and select "open".

4. This should have changed your ImageJ canvas. Now, drag your volume from your folder into the canvas.

5. In the popup window, make sure that "Resize canvas to fit stack" is checked. After clicking OK, your canvas should snap to your image.

6. In your TrakEM2 properties, right click on "anything" in the template column and add a new "area_list".

    ![new area list](/static/images/help/new_area_list.png "new area list")

7. Drag the entire "anything" folder into "Unitled 0" in the middle column.

8. Right click the nested "anything" folder inside "Untitled 0" and add a "new area list".

    ![final area list](/static/images/help/final_area_list.png "final area list")

9. Annotate Your Data by drawing all over it. You can scroll to annotate different slices in your tif.

10. When done, right click your canvas and select "Export" -> "Arealists as labels (tif)".

    >>>NOTE: At any point, you can export your annotations as an xml by the same method listed above. Opening the xml file will start you where you left off.

11. A black screen will appear - these are your annotations, don't worry if you can't see them.

12. Save your annotations in the correct directory *with the same name*, an example given below.

    ![annotation file](/static/images/help/annotation_file.png "annotation file")

### Annotate with Neuroglancer

Alternatively, you can annotate with neuroglancer.  Follow our guide on creating neuroglancer point annotations [here]([url('/content/guides/neuroglancer-pt-annotations.md')]).