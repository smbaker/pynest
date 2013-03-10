#!/usr/bin/env python

from distutils.core import setup
readme = open('README.txt').read()
setup(name='pyenest',
      version='0.1',
      description='Python API for Nest Thermostat - Altered',
      author='Eugene Efremov',
      author_email='eaefremov@gmail.com',
      url='http://www.github.com/eae',
      scripts=['nest.py'],
     )
