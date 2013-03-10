#!/usr/bin/env python

from distutils.core import setup, find_packages
readme = open('README.txt').read()
setup(name='pyenest',
      version='0.2',
      description='Python API for Nest Thermostat - Altered',
      author='Eugene Efremov',
      author_email='eaefremov@gmail.com',
      url='http://www.github.com/eae',
      packages=find_packages(),
     )
