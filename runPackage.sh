#!/bin/bash

# This script is used to build and install the Python package.

# Run the setup.py commands
python setup.py bdist_wheel sdist

# Install the package locally
pip install .
