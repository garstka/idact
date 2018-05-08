# Interactive Data Analysis Convenience Tools

[![Build Status](https://travis-ci.com/garstka/eng-project.svg?token=cvggfL1vjmB383MxWGF4&branch=master)](https://travis-ci.com/garstka/eng-project)
[![Build Status](https://travis-ci.com/garstka/eng-project.svg?token=cvggfL1vjmB383MxWGF4&branch=develop)](https://travis-ci.com/garstka/eng-project)

Tools taking care of the tedious aspects of working with big data on a cluster.


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

```
python scripts/run_tests.py
```

## Build docs and view in browser

```
python scripts/build_docs.py
```

## Build coverage and view in browser

```
python scripts/view_coverage.py
```
