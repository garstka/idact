===========================================
Interactive Data Analysis Convenience Tools
===========================================

.. image:: https://travis-ci.com/garstka/eng-project.svg?token=cvggfL1vjmB383MxWGF4&branch=master
    :target: https://travis-ci.com/garstka/eng-project

.. image:: https://travis-ci.com/garstka/eng-project.svg?token=cvggfL1vjmB383MxWGF4&branch=develop
    :target: https://travis-ci.com/garstka/eng-project

Tools taking care of the tedious aspects of working with big data on a cluster.


Install
-------

.. code-block:: bash

    pip install git+https://github.com/garstka/eng-project

Prepare dev environment
-----------------------

.. code-block:: bash

    git clone https://github.com/garstka/eng-project
    cd eng-project

With Conda:

.. code-block:: bash

    conda env create -f envs/environment-dev.yml
    conda activate idact-dev

Without Conda:

.. code-block:: bash

    pip install -r requirements_dev.txt

Run tests with coverage, flake8 and Pylint
------------------------------------------

.. code-block:: bash

    python scripts/run_tests.py

Build docs and view in browser
------------------------------

.. code-block:: bash

    python scripts/build_docs.py

Build coverage and view in browser
----------------------------------

.. code-block:: bash

    python scripts/view_coverage.py
