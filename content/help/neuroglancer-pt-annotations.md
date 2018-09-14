---
$title@: Add point annotations in neuroglancer
---

1. Click on the JSON editor (top right corner of the web browser and looks like `{}`). The results should look something like:

    ![json editor](/static/images/help/image1.png "json editor")

1. Click the blue arrows next to “layers”. The result should look like this:

    ![layers](/static/images/help/image2.png "layers")

1. Now, add a comma at the end of the line underneath “layers”. Then copy and paste this on the next line:

        "annotations":
        {
        "type":"pointAnnotation",
        "points":[]
        }

    The result should look like this:
    ![pointAnnotation](/static/images/help/image3.png "pointAnnotation")

1. Right-click on the new channel called “annotations”. Now click on button to the right of the color (highlighted in blue in image below):

    !["add point](/static/images/help/image4.png "add point")

1. Now that you have selected the point annotations, you can ctrl + click on any location in the image and yellow spheres will show up at those locations. The locations are stored in the JSON editor and can be accessed at any time by clicking the `{}` in the top right of the web browser.
