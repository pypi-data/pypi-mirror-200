#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 14:17:36 2021

@author: ross
"""

import setuptools

setuptools.setup(
    name = 'ocrp',
    version = '0.1.9.8',
    author = 'Ross Ashman',
    description = 'a parser for AWS and Azure ocr json files',
    packages = setuptools.find_packages()
    )