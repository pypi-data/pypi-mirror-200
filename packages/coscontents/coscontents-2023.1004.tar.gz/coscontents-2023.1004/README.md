# IBM Cloud Object Storage Jupyter Contents

This package contains a [juypterlab contents](https://jupyter-notebook.readthedocs.io/en/stable/extending/contents.html)
contents manager to allow storing jupyter notebooks on IBM Cloud Object Storage. It also supports local filesystem access so
you can store notebooks locally.

Currently only python 3.7 is supported.

## Usage

To use the content manager, first you must install it:

```
pip install coscontents
```

> Prefer installation via pip. The old way `python setup.up install` fetches dev versions of packages and may
break the build. Pip always fetches stable versions.

Next adjust your jupyter config usually `/etc/jupyter/jupyter_notebook_config.py` or you can create a
`jupyter_notebook_config.py` file in your current working directory.

Add the following line:
```
c.ServerApp.contents_manager_class = "coscontents.COSContentsManager"
```

## Local testing

The easiest way to test this locally is to work in a virtual environment.
You can use your preferred virtual environment management tool (e.g. Conda),
or to set up a fresh venv, run:

```
$ cd path/to/COSContents
$ python3 -m venv venv
$ . ./venv/bin/activate
```

Install all the dependencies, and set yourself up for development:

```
$ pip install --editable .
[...]
$ pip install jupyterlab
[...]
```

Jupyter itself is not included in the `install_requires` because while it is
useful for development and testing, this code does not actually depend upon it.
Now you have all the prerequisites installed, and the `coscontents` package
points to the files in your working directory.

If you have not already an IBM Cloud Account and a COS bucket you will need it

```
>>> # This is a dummy value; replace it with your own token or user/pass.
```

The only remaining step is to launch Jupyter and configure it to use the
`COSContentsManager` class:

```
$ jupyter lab --ServerApp.contents_manager_class=coscontents.COSContentsManager
```

This will run a local test Jupyter lab server without changing your default
Jupyter configuration. You can make this your default by following the
instructions in "Usage" above.

Now the server is running, and you just need to follow Jupyter's directions to
connect! Certain actions (like file navigation) may take longer than you would
expect, because it has to communicate with the remote IBM Cloud server.

## How it Works

TODO explain

Features
-----
- Mix and match different content managers for different directories 
- Easily move files between different content managers (i.e local files to s3 backed manager) 
- Path validation to keep consistent naming scheme and/or prevent illegal characters

Usage
-----

The following code snippet creates a HybridContentsManager with two directories with different content managers. 

```python
c.ServerApp.contents_manager_class = HybridContentsManager

c.HybridContentsManager.manager_classes = {
    # NOTE: LargFileManager only exists in notebook > 5
    # If using notebook < 5, use FileContentManager instead
    "": LargeFileManager,
    "COS": COSContentsManager
}

# Each item will be passed to the constructor of the appropriate content manager.
c.HybridContentsManager.manager_kwargs = {
    # Args for root LargeFileManager
    "": {
        "root_dir": read_only_dir
    },
    # Args for the shared COSContentsManager directory
    "COS": {
        "access_key_id": ...,
        "secret_access_key": ...,
        "endpoint_url":  ...,
        "bucket": ...,
        "region_name": ...
    },
}

def only_allow_notebooks(path):
  return path.endswith('.ipynb')

# Only allow notebook files to be stored in COS
c.HybridContentsManager.path_validators = {
    "COS": only_allow_notebooks
}
```


### Listing

The listings show up under the "COS" folder of the notebook file browser.

## Acknowledgements

This code is based on:

* [https://github.com/danielfrg/s3contents]
* [https://github.com/TileDB-Inc/TileDB-Cloud-Jupyter-Contents]
* [https://github.com/viaduct-ai/hybridcontents]

