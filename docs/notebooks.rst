Tutorial notebooks
==================

You can use a local Jupyter Notebook to run each tutorial notebook.

.. code-block:: bash

      python -m pip install jupyterlab
      jupyter lab

01. ProSandbox
--------------

Demonstrates simple interactions with the Prometheus cluster using `idact`.

.. toctree::
    :maxdepth: 3

    _notebooks/01-ProSandbox.ipynb

02a. DaskWorkflow-Local
-----------------------

Part 1 of a demo showing how to deploy and work with Dask using a Jupyter
Notebook deployed on a cluster.

.. toctree::
    :maxdepth: 3

    _notebooks/02a-DaskWorkflow-Local.ipynb

02b. DaskWorkflow-Remote
~~~~~~~~~~~~~~~~~~~~~~~~

Part 2 of the Dask workflow demo, intended to be uploaded to the cluster while
working with part 1.

.. toctree::
    :maxdepth: 3

    _notebooks/02b-DaskWorkflow-Remote.ipynb
