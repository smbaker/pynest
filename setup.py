#!/usr/bin/env python

from distutils.core import setup

setup(name='pynest',
      version='1.0',
      description='Python API for Nest Thermostat',
      author='Scott Baker',
      author_email='smbaker@gmail.com',
      url='http://www.smbaker.com/',
      py_modules = ['cosm','nest']
      scripts=['nesttool.py','nest_cosm.py'],
     )
