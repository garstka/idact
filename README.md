# Interactive Data Analysis Convenience Tools

[![Build Status](https://travis-ci.com/garstka/eng-project.svg?token=cvggfL1vjmB383MxWGF4&branch=master)](https://travis-ci.com/garstka/eng-project)
[![Build Status](https://travis-ci.com/garstka/eng-project.svg?token=cvggfL1vjmB383MxWGF4&branch=develop)](https://travis-ci.com/garstka/eng-project)

Tools taking care of the tedious aspects of working with big data on a cluster.

## Requirements

Python 3.5+ is required.

If this is not the default installation, use the proper executables,
e.g. pip3 and python3 instead of pip and python for each command
in this README.

You can also use the absolute paths to pip and python executables.

## Install

```
pip install git+https://github.com/garstka/eng-project
```

## Prepare dev environment

```
git clone https://github.com/garstka/eng-project
cd eng-project
```

With Conda:

```
conda env create -f envs/environment-dev.yml
conda activate idact-dev
```

Without Conda:

```
pip install -r requirements_dev.txt
```

## Run tests with coverage, flake8 and Pylint

Functional tests require the testing container to be up and running,
see testing_setup/README.md.

```
python scripts/run_tests.py
```

## Build docs and coverage

```
python scripts/build_docs.py
python scripts/view_coverage.py
```

Each script will open the generated html page in the default browser, unless
`--no-show` parameter is passed.
