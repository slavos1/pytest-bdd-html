#!/usr/bin/env python

import setuptools

if __name__ == "__main__":
    setuptools.setup(package_data={'': ['**/*.csv']},
    include_package_data=True)

