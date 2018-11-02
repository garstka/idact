# -*- coding: utf-8 -*-
"""Console script for idact-notebook.

How to run::

  python -m idact.notebook --help

Or::

  idact-notebook --help

.. click:: idact.notebook:main
   :prog: idact-notebook
   :show-nested:

"""

import sys
from idact.detail.jupyter_app.main import main

if __name__ == "__main__":
    sys.exit(
        main())  # pragma: no cover, pylint: disable=no-value-for-parameter
