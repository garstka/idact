#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

REQUIREMENTS = ['click>=6.7',
                'fabric3>=1.14',
                'bitmath>=1.3.1.2',
                'python-dateutil>=2.7.2',
                'sshtunnel>=0.1.4',
                'paramiko>=2.4.1',
                'dask>=0.18.2',
                'distributed>=1.22.0',
                'requests>=2.18.4',
                'bokeh>=0.13.0',
                'jupyter>=1.0.0']

setup(
    author="Matt Garstka",
    author_email='matt@garstka.net',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description=("Tools taking care of the tedious aspects"
                 " of working with big data on a cluster."),
    entry_points={
        'console_scripts': [
            'idact-notebook=idact.notebook:main',
        ],
    },
    install_requires=REQUIREMENTS,
    license="MIT license",
    long_description=README,
    include_package_data=True,
    keywords='idact',
    name='idact',
    packages=find_packages(include=['idact']),
    url='https://github.com/garstka/idact',
    version='0.4',
    zip_safe=False,
)
