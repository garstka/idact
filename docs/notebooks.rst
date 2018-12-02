Tutorial notebooks
==================

You can use a local Jupyter Notebook to run each tutorial notebook.

.. code-block:: bash

      python -m pip install jupyterlab
      jupyter lab


01. Connecting to a cluster
---------------------------

Overview
~~~~~~~~

 - Add and configure a cluster.
 - Connect to the cluster.
 - Save and load your environment.
 - Modify and remove cluster config.

Contents
~~~~~~~~

.. toctree::
    :maxdepth: 3

    _notebooks/01-Connecting_to_a_cluster.ipynb

02. Allocating nodes
--------------------

Overview
~~~~~~~~

 - Allocate nodes on a cluster.
 - Examine allocated nodes.
 - Open tunnels to nodes.
 - Cancel node allocations.

Contents
~~~~~~~~

.. toctree::
    :maxdepth: 3

    _notebooks/02-Allocating_nodes.ipynb


03. Deploying Jupyter
---------------------

Overview
~~~~~~~~

 - Configure remote Jupyter deployment.
 - Deploy Jupyter on a compute node.
 - Access deployed Jupyter Notebook.

Contents
~~~~~~~~

.. toctree::
    :maxdepth: 3

    _notebooks/03-Deploying_Jupyter.ipynb


04. Deploying Dask
------------------

Overview
~~~~~~~~

 - Configure remote Dask.distributed deployment.
 - Deploy Dask.distributed scheduler and workers on compute nodes.
 - Access scheduler and worker dashboards.

Contents
~~~~~~~~

.. toctree::
    :maxdepth: 3

    _notebooks/04-Deploying_Dask.ipynb


05. Configuring idact on a cluster
----------------------------------

Overview
~~~~~~~~

 - Synchronize the environment between idact and the cluster.
 - Initialize idact config on the cluster from a deployed notebook.

Contents
~~~~~~~~

.. toctree::
    :maxdepth: 3

    _notebooks/05a-Configuring_idact_on_a_cluster_-_local_part.ipynb

.. toctree::
    :maxdepth: 3

    _notebooks/05b-Configuring_idact_on_a_cluster_-_remote_part.ipynb


06. Working on a cluster
------------------------

Overview
~~~~~~~~

 - Synchronize deployments between the local machine and a notebook running on the cluster.
 - Perform simple computations using the Dask deployment on a deployed notebook.
 - Clear synchronized deployments.

Contents
~~~~~~~~

.. toctree::
    :maxdepth: 3

    _notebooks/06a-Working_on_a_cluster_-_local_part.ipynb

.. toctree::
    :maxdepth: 3

    _notebooks/06b-Working_on_a_cluster_-_remote_part.ipynb


07. Adjusting timeouts
----------------------

Overview
~~~~~~~~

 - Adjust deployment timeouts, if your deployments fail too often.

Contents
~~~~~~~~

.. toctree::
    :maxdepth: 3

    _notebooks/07-Adjusting_timeouts.ipynb


08. Using the quick deployment app
----------------------------------

Overview
~~~~~~~~

 - Use the idact-notebook app to quickly deploy a notebook to work with.

Contents
~~~~~~~~

.. toctree::
    :maxdepth: 3

    _notebooks/08a-Using_the_quick_deployment_app_-_local_part.ipynb

.. toctree::
    :maxdepth: 3

    _notebooks/08b-Using_the_quick_deployment_app_-_remote_part.ipynb


09. Demo analysis
-----------------

Overview
~~~~~~~~

 - Download a large quantity of CSV data for analysis.
 - Load the data using Dask on the cluster.
 - Convert the data to a more suitable format: Apache Parquet.
 - Load the data from Parquet.
 - Perform a simple data analysis.

Contents
~~~~~~~~

.. toctree::
    :maxdepth: 3

    _notebooks/09a-Demo_analysis_-_local_part.ipynb

.. toctree::
    :maxdepth: 3

    _notebooks/09b-Demo_analysis_-_remote_part.ipynb
