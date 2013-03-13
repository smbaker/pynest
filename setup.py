#!/usr/bin/env python

from setuptools import setup, find_packages
readme = open('README.txt').read()
setup(name='pyenest',
      version='0.3',
      description='Python API for Nest Thermostat - Edited',
      author='Eugene Efremov',
      author_email='eaefremov@gmail.com',
      url='http://www.github.com/eae',
      packages=find_packages())
