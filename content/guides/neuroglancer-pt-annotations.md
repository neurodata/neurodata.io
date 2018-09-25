---
$title@: "Manually annotate in Neuroglancer"
hidden_sidebar: true
$order: 2
---

[TOC]

This guide demonstrates how to add point annotations manually to a neuroglancer view.

### Open JSON editor

Click on the JSON editor (top right corner of the web browser and looks like `{}`). The results should look something like:

![json editor](/static/images/help/json_editor.png "json editor")

### Open layers

Click the blue arrows next to “layers”. The result should look like this:

![layers](/static/images/help/layers.png "layers")

### Add annotation layer

Now, add a comma at the end of the line underneath “layers”. Then copy and paste this on the next line:

```json
"annotations":
{
"type":"pointAnnotation",
"points":[]
}
```

The result should look like this:
![pointAnnotation](/static/images/help/point_annotations.png "pointAnnotation")

### Select the annotation type

Right-click on the new channel called “annotations”. Now click on button to the right of the color (highlighted in blue in image below):

!["add point](/static/images/help/add_point.png "add point")

### Add points

Now that you have selected the point annotations, you can ctrl + click on any location in the image and yellow spheres will show up at those locations. The locations are stored in the JSON editor and can be accessed at any time by clicking the `{}` in the top right of the web browser.

### Move a point

To move an existing annotation, hold down `ALT` and click the annotation.  You can then drag the annotation around and drop it in a new location.