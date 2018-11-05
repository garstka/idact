# Development overview

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
