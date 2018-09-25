---
$title@: "Programmatically annotate in R"
author: "Jesse Leigh Patsolic"
date: 2018-09-07
$order: 3
hidden_sidebar: true
---

<!--
### ### INITIAL COMMENTS HERE ###
###
### Jesse Leigh Patsolic 
### 2018 <jpatsolic@jhu.edu>
### S.D.G 
#
-->

[TOC]

### Using the exported JSON file

When using [neuroglancer](http://viz.neurodata.io/) to view your dataset you may want to add some point annotations to share with collaborators. The
following will help you use R to do that. 

When you have your neuroglancer window set the way you want it with all the channels and colors set accordingly use the export JSON functionality by clicking the `{}` in the upper right of the window and the click `export`.  This will download a file called `state.json`.  Place this
file in the directory with your R script.  

#### File setup

We'll read the JSON file into R as a list using the `rjson` package.


```r
f <- file('state.json', 'r')
h <- rjson::fromJSON(file = f)
close(f)
```


#### Add an annotation layer

We'll need to grab some settings from the existing state and setup a new
annotation layer, called `MyAnnotations`.


```r
## grab voxel size of current navigation settings
voxelSize <- h$navigation$pose$positio$voxelSize

## grab current voxel coordinates
voxelCoordinates <- h$navigation$pose$positio$voxelCoordinates

## Create a new list for the new layer
MyAnnotations <- list(type = "annotation",
                      tool = "annotateSphere",
                      annotationColor = "#ff9900", # orange
                      voxelSize = as.numeric(voxelSize)
                     )

## Example of the structure for 2 ellipsoid annotations ##
##annotations <- list(list(center = c(6963, 7296.5, 23.5), 
##                         radii = c(68.2422180175781, 68.2422180175781, 4.09453296661377), 
##                         type = "ellipsoid", 
##                         id = "1", 
##                         description = "1"),
##                    list(center = c(6968, 7298, 23.5), 
##                         radii = c(80, 80, 8), 
##                         type = "ellipsoid", 
##                         id = "2", 
##                         description = "2"))
```

#### Function to format annotations

The following function takes `x, y, z,` and `id` parameters and uses the
`voxelSize` to specify spherical annotations, you can change this if you
want ellipsoidal annotations.


```r
makeEllipse <- function(x, y, z, id, 
                        rx = 100/voxelSize[1], 
                        ry = 100/voxelSize[2], 
                        rz = 100/voxelSize[3], 
                        type = "ellipsoid", 
                        desc = id) {

  list(center = c(x, y, z), 
       radii = c(rx, ry, rz), 
       type = type, 
       id = as.character(id), 
       description = as.character(desc))
}
```

###### Set up a toy example

If you already have a set of `x, y, z` coordinates with id's you can skip this. 


```r
n <- 10
cx <- voxelCoordinates[1]
cy <- voxelCoordinates[2]
cz <- voxelCoordinates[3]
r <- 5 * voxelSize[3]

th <- seq(0,2*pi, length = n)
toy <- cbind(x = r * cos(th) + cx, y = r * sin(th) + cy, z = cz, id = 1:n)
```

#### Edit the state list

Using this example you'll need to have your `x, y, z` and `id` variables
in a matrix or data.frame -- mine is called `toy`.


```r
dat <- apply(toy, 1, as.list)
out <- lapply(dat, function(x) do.call(makeEllipse,x))

## store our annotations in the new layer list
MyAnnotations$annotations <-  out

## add our new layer to the state
h$layers$MyAnnotations <- MyAnnotations
```

#### Write to file


```r
myFile <- file("MyAnnotationState.json", "w")
writeLines(rjson::toJSON(h, indent = 2), myFile) 
close(myFile)
```

Now you can replace the JSON state in your neuroglancer window with the
contents of your new JSON file `MyAnnotationStats.json`.


<!--
#clipy <- pipe("pbcopy", "w")
#dput(h$layers$centroids$annotations[[2]], file = clipy)
#close(clipy)

#   Time: A few hours, mostly wrangling JSON formatting to match neuroglancer
##  Working status: Check
### Comments:
####Soli Deo Gloria
--> 