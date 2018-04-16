---
$title@: Data Access
$hidden: true
$view: /views/access.html
options: 
    - ndwebtools
    - ndpull
    - intern
---

Data hosted by [neurodata.io](https://neurodata.io/data) are publicly available. NeuroData utilizes the [BOSS](https://api.boss.neurodata.io), co-developed with [JHU-APL](https://github.com/jhuapl-boss/), as a data store.  This document explains how to access this data.

BOSS has the following hierarchical organization:

1. **Collection:** typically either the name of the lab PI or the person who collected the data

2. **Experiment:** within this level, data share a common voxel extent and voxel size.  Often synonymous with actual experiments.

3. **Channel:** data reside at this level and are either `uint8`/`uint16` image data or `uint64` annotations

### Methods for accessing data

All data access currently requires registration. Create an account at [api.boss.neurodata.io](https://api.boss.neurodata.io)

#### [ndwebtools](https://ndwebtools.neurodata.io)

A frontend for navigating BOSS projects. It provides (limited) TIFF cutouts to data and links to data visualization.  Larger cutouts (> 1GB) should be performed programmatically using one of the tools below.

- Log in at [ndwebtools.neurodata.io](https://ndwebtools.neurodata.io)

- Navigate the available projects by clicking the links to collections and experiments.  Clicking on any experiment takes you to the cutout page.

- The cutout page provides TIFF downloads and viz links for the channels within the experiment.

#### [ndpull](https://github.com/neurodata/ndpull)

A Python package for downloading volumes of data from the BOSS as TIFF stacks. This tool is installed locally and used from the command line.

- Installation and usage instructions on its [GitHub page](https://github.com/neurodata/ndpull/)

#### [intern](https://github.com/jhuapl-boss/intern)

A Python package developed by JHU-APL for interactively and programatic usage of the BOSS.

- Installation and usage instructions available on its [GitHub page](https://github.com/jhuapl-boss/intern)

### Questions/comments?  Email [support@neurodata.io](mailto:support@neurodata.io)