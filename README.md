# neurodata.io

This is the static site generator code for [neurodata.io](https://neurodata.io)

## Prerequisites

At a minimum, you will need the following tools installed:

1. [Git](http://git-scm.com/)
2. [Grow](https://grow.io)

If you do not have Grow, you can install it using:

```sh
curl https://install.grow.io | bash
```

or (from a virtual environment)

```sh
pip install grow
```

Note that grow does not yet support Python 3.

## Running the development server

Prior to starting the development server, you may have to install dependencies used by your project. The `grow install` command walks you through this and tries to set up your environment for you.

The `grow run` command starts your development server. You can make changes to your project files and refresh to see them reflected immediately.

```sh
grow install
grow run
```

## Building

You can use the `grow build` command to build your whole site to the `build` directory. This is a good way to test and verify the generated code.

```sh
grow build
```

## Contributing

Please submit pull requests to `deploy` branch.


## [DEV/QC] Bib files and references

There is a LaTeX file that will build the references into a PDF, mostly
for QC. It is located in the root directory and can be built by running
`make` in the root directory.
