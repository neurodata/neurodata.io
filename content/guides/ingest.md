---
$title@: Ingest
$order: 3
---

[TOC]

This guide shows how to send data to NeuroData by _ingesting_ into the BOSS.  Currently, TIFF/OME/PNG are supported using this method.

As with [data access]([url('/content/guides/access.md')]), we will be using [ndex](https://github.com/neurodata/ndex) to directly upload data.

>>> Note: the most up to date guide for data ingest is maintained in the `ndex` repo on [GitHub](https://github.com/neurodata/ndex/blob/master/README.md)

### Install

- Install or insure you have [Python 3](https://www.python.org/downloads/) (x64).  Versions 3.5, 3.6, 3.7 supported

    `python --version`

- Create a python 3 [virtual environment](https://virtualenv.pypa.io/en/stable/)

    `virtualenv env`

- Activate virtual environment

- Install compiler for Windows

    - [Visual C++ Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2017)

- Install

    - Via PyPI (Preferred)

        `pip install ndexchange`

    - From github (Latest dev version)

        `pip install git+git://github.com/neurodata/ndex.git`

### Config

1. Register for a free account and generate a [Boss API key](https://api.boss.neurodata.io/v1/mgmt/token) and save it to file named `neurodata.cfg` (using the format provided in [neurodata.cfg.example](examples/neurodata.cfg.example))

1. To send messages through Slack (optional) you will also need a [Slack API key](https://api.slack.com/custom-integrations/legacy-tokens) and save to file `slack_token`.

1. To perform ingest, you must have `resource manager` permissions in the BOSS (ask an [admin](mailto:support@neurodata.io) to get these privileges).

### Upload images (ndpush)

1. To generate an ingest's command line arguments, create and edit a file copied from provided example: [gen_commands.example.py](https://raw.githubusercontent.com/neurodata/ndex/master/examples/neurodata.cfg.example).

2. Add your experiment details and run it from within the activated python environment (`python gen_commands.py`). It will generate command lines to run and estimate the amount of memory needed. You can then copy and run those commands.

3. Alternatively, run: ndpush -h to see the complete list of command line options.
