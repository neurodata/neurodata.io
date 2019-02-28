---
$title@: Analyze
$order: 2
$category: Analyze
---

[TOC]

To run analysis on our data we offer the following options

### ndex

To download portions or entire datasets as TIFF stacks or individual files for local analysis, follow the guide on [access]([url('/content/guides/download.md')]).

### nd-multicore

For processing data in parellel, please use <a href="https://github.com/rguo123/nd-multicore" target="_blank" rel="noopener">nd-multicore</a>.  

### Considerations

As data transfer within an AWS region is free, and to keep our costs manageable for hosting these data publically, we ask that access to large datasets are made from within an AWS instance in the same region as the BOSS (`us-east-1`).  Additionally, for parallel jobs, please keep the number of requests you perform to < 25 simultaneous workers.

### Analysis pipelines

Our analysis pipelines are under active development.  Please take a look at our list of maintained [tools]([url('/content/pages/tools.html')]).  We are currently working on guides for cell detections and registration pipelines.  If there's anything else you would like to see, please let us know.