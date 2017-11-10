# neurodata.io

A short introduction to your project could go here. This README outlines the details of collaborating on this Grow website.

## Prerequisites

At a minimum, you will need the following tools installed:

1. [Git](http://git-scm.com/)
2. [Grow](https://grow.io)

If you do not have Grow, you can install it using:

```
curl https://install.growsdk.org | bash
```
or
```
pip install grow
```
Note that grow does not yet support Python 3.

## Building the site

You can use the `grow build` command to build your whole site to the `build` directory. This is a good way to test and verify the generated code.

```
grow build
```

Make sure to run `grow build` in the root directory of the site. If you get an error along the lines of `podspec not found`, you are probably not in the right directory.

## Viewing the built site

It is best to use a local web server to view the site. We suggest the node http server. If you have npm, you can install it like this:
```
npm install -g http-server
```

If you don't have npm, go get the [Node Version Manager](https://github.com/creationix/nvm) and install node version 6 or version 8 (whatever is installed by default). That should give you npm.

Then, from the `build` directory, run 
```
http-server .
```

A server will start making the site accessible on `http://localhost:8080` (or the next available port if 8080 is occupied).