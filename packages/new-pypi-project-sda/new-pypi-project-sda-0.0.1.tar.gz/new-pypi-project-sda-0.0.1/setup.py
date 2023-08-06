#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='new-pypi-project-sda',
    version='0.0.1',
    author="Maciej Oliwa",
    author_email="oliwa.maciej@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    description='Some code for SDA students.'
)
