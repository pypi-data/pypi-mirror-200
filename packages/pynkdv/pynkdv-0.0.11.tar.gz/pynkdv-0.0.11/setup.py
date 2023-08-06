#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='pynkdv',
    version='0.0.11',
    author='rui',
    author_email='19251017@life.hkbu.edu.hk',
    url='https://github.com/edisonchan2013928/PyNKDV',
    description='for nkdv in python',
    packages=['pynkdv'],
    install_requires=['nkdv', 'geopandas', 'osmnx', 'pandas', 'shapely', 'scipy'],
    entry_points={
    }
)