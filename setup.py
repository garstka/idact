#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('requirements.txt') as requirements_file:
    REQUIREMENTS = [i for i in requirements_file.readlines() if i]

setup(
    author="Matt Garstka",
    author_email='matt@garstka.net',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Distributed Computing',
        'Topic :: Utilities',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Natural Language :: English',
    ],
    description=("A library that takes care of several tedious aspects"
                 " of working with big data on an HPC cluster."),
    entry_points={
        'console_scripts': [
            'idact-notebook=idact.notebook:main',
        ],
    },
    install_requires=REQUIREMENTS,
    license="MIT license",
    long_description=README,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords=("interactive data analysis"
              " dask distributed jupyter notebook deployment"
              " slurm allocation cluster HPC"
              " ssh tunnel"),
    name='idact',
    packages=find_packages(include=['idact']),
    url='https://github.com/garstka/idact',
    version='0.5',
    zip_safe=False,
)
