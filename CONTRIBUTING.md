# Contributing

## Guidelines [work in progress]

### Submitting  issues

Please include:
 - description of the issue,
 - steps to reproduce,
 - the error message and/or log fragment,
 - the local operating system and Python distribution,
 - `conda env export` for Anaconda or `pip list` for `virtualenv` or similar,
 - info about the cluster (if not Cyfronet/Prometheus),
 - workaround if available.

### Contributing changes

Please:
 - Fork `idact` on GitHub.
 - Create a new branch off the `develop` branch.
 - Run the testing setup in docker to test changes locally (see `scripts`).
 - Add unit and/or functional tests.
 - Submit a pull request to the develop branch.

## Release instructions

 - Bump version in `idact/__init__.py` and `setup.py` (`0.y-1 -> 0.y`).
 - Update `docs/changelog.md`
 - Update `docs/docs_by_version.md`
 - Submit a pull request from develop branch to master.
 - Commit title: `Version 0.y`, changelog in the message.
 - Merge the pull request.
 - Create a GitHub release on the branch master.
 - Release (tag) name `0.y`, title: `Version 0.y`.
 - Package will be released to pypi automatically.
 - Upload zipped notebooks as assets if they changed since last release.
