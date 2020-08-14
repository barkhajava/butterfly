#!/usr/bin/env python
import os
from setuptools import find_packages
from setuptools import setup

VERSION = 0.2
version = os.path.join('butterfly', '__init__.py')


README = open('README.md').read()

INSTALL_REQ = [
    'h5py>=2.6.0',
    'scipy>=0.17.0'
    'numpy>=1.12.0',
    'tornado>=4.4.2',
    'futures>=3.0.5',
    'pyaml>=16.12.2',
    'tifffile>=0.11.1',
    'pymongo>=3.4.0',
	'rh_logger>=2.0.0',
]

setup(
    version=VERSION,
    name='bfly',
    author='Daniel Haehn',
    packages=find_packages(),
    author_email='haehn@seas.harvard.edu',
    url="https://github.com/Rhoana/butterfly",
    description="butterfly dense image server",
    # Installation requirements
    install_requires= INSTALL_REQ,
    # Allows command line execution
    entry_points=dict(console_scripts=[
        'bfly = butterfly.cli:main',
        'bfly_query = butterfly.cli:query',
    ])
)
