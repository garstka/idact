#!/usr/bin/env python3
"""Deploys documentation to GitHub pages.

    If the environment variable :attr:`TRAVIS_BRANCH` is set, it overrides
    the current git branch.
    If the environment variable :attr:`GH_TOKEN` is set, it is used as the API
    token.
"""

import os
import shutil
import subprocess as sub
import sys


def get_current_git_branch():
    """Returns the current git branch."""
    return str(sub.check_output("git rev-parse --abbrev-ref HEAD",
                                shell=True).splitlines()[0], 'utf-8')


GIT_CONFIG = ['user.email travis@travis-ci.com',
              'user.name "Travis CI"']

GIT_BRANCH = os.environ.get('TRAVIS_BRANCH', get_current_git_branch())

WORKING_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                            '../docs'))

DEPLOY_REPO_DIR = os.path.join(WORKING_DIR, 'deploy-repo')
DEPLOY_REPO_REMOTE = "https://{token}github.com/garstka/garstka.github.io.git"

DEPLOY_DOCS_PARENT_DIR = os.path.join(DEPLOY_REPO_DIR, 'idact')
DEPLOY_DOCS_DIR = os.path.join(DEPLOY_DOCS_PARENT_DIR,
                               '{git_branch}/html'.format(
                                   git_branch=GIT_BRANCH))

SOURCE_DOCS_DIR = os.path.join(WORKING_DIR, '_build/html')

BUILD_NUMBER = os.environ.get('TRAVIS_BUILD_NUMBER', 'manual')

COMMIT_MESSAGE = ("Deploy docs for branch {git_branch},"
                  " build: {build_number}").format(git_branch=GIT_BRANCH,
                                                   build_number=BUILD_NUMBER)


def main():
    def call(command):
        sub.check_call(command, shell=True)

    try:
        os.chdir(WORKING_DIR)
        print("Deploying docs...")

        if os.path.isdir(DEPLOY_REPO_DIR):
            shutil.rmtree(DEPLOY_REPO_DIR)
        os.mkdir(DEPLOY_REPO_DIR)
        os.chdir(DEPLOY_REPO_DIR)

        call("git init")
        for config in GIT_CONFIG:
            call("git config {}".format(config))

        token = os.environ.get('GH_TOKEN', '')
        if token:
            token += '@'
        remote = DEPLOY_REPO_REMOTE.format(token=token)

        call("git remote add origin {}".format(remote))
        call("git fetch origin")
        call("git checkout master")

        if os.path.isdir(DEPLOY_DOCS_DIR):
            shutil.rmtree(DEPLOY_DOCS_DIR)

        shutil.copytree(SOURCE_DOCS_DIR, DEPLOY_DOCS_DIR)

        call("git add {}".format(DEPLOY_DOCS_DIR))

        call('git commit -m "{}"'.format(COMMIT_MESSAGE))
        call("git push")

        return 0
    except Exception as e:  # pylint: disable=broad-except
        print(e)
        return 1


if __name__ == '__main__':
    sys.exit(main())
