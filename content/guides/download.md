---
$title@: Download
hidden_sidebar: true
---

[TOC]

This document explains how to access/download data hosted by NeuroData. [Data]([url('/content/pages/data')]) are publicly available. NeuroData utilizes the [BOSS](https://api.boss.neurodata.io), co-developed with [JHU-APL](https://github.com/jhuapl-boss/), as a data store.  We also selectively host small datasets on S3 for fast data visualization in neuroglancer.  For that, see our guide on the [precomputed format]([url('/content/guides/boss-to-precompute')]).

### Boss hierarchy

1. **Collection:** typically either the name of the lab PI or the person who collected the data
2. **Experiment:** within this level, data share a common voxel extent and voxel size.  Often synonymous with actual experiments.
3. **Channel:** data reside at this level and are either `uint8`/`uint16` image data or `uint64` annotations

Further information on BOSS organization can be found in the [docs](https://docs.theboss.io/v1/docs).

### Methods for accessing data

Data access requires a free account. Create an account at [api.boss.neurodata.io](https://api.boss.neurodata.io).  All methods require a login.

There are four methods for getting data from the BOSS:

#### [ndwebtools](https://ndwebtools.neurodata.io)

A frontend for navigating BOSS projects. It provides TIFF cutouts (limited to < 1GB) to data and links to data visualization (through neuroglancer).  Larger cutouts should be performed programmatically using either `ndex` or `intern` detailed below.

- Log in at [ndwebtools.neurodata.io](https://ndwebtools.neurodata.io)
- Navigate the available projects by clicking the links to collections and experiments.  Clicking on any experiment takes you to the cutout page.
- The cutout page provides TIFF downloads and viz links for channels within each experiment.

#### [neuroglancer](https://viz.neurodata.io)

To visualize the data before downloading you can use neuroglancer.  Please see our [guide]([url('/content/guides/neuroglancer')]).

#### [ndex](https://github.com/neurodata/ndex)

A Python command-line tool for downloading volumes of data from the BOSS as TIFF stacks.  This library can also be loaded from within Python.

Installation and usage instructions on its [GitHub page](https://github.com/neurodata/ndex/)

#### [intern](https://github.com/jhuapl-boss/intern)

A Python package developed by JHU-APL for interactive and programmatic usage of the BOSS.

Installation and usage instructions available on its [GitHub page](https://github.com/jhuapl-boss/intern)