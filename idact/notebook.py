# -*- coding: utf-8 -*-
"""Console script for idact-notebook."""

import sys
from idact.detail.jupyter_app.main import main

if __name__ == "__main__":
    sys.exit(
        main())  # pragma: no cover, pylint: disable=no-value-for-parameter
