#!/usr/bin/env python3

from setuptools import setup

import sys
if sys.version_info < (3, 5):
    raise Exception('Python 3.5 or higher is required to use PyLinkbot3.')

setup (name = 'PyLinkbot',
       author = 'David Ko',
       author_email = 'david@barobo.com',
       version = '3.0.0a0',
       description = "This is a pure Python implementation of PyLinkbot. See http://github.com/BaroboRobotics/PyLinkbot",
       package_dir = {'':'src'},
       packages = ['linkbot', 'linkbot.async'],
       url = 'http://github.com/BaroboRobotics/PyLinkbot3',
       install_requires=[
           'PyRibbonBridge>=0.0.5', 
           'PySfp>=0.1.1', 
           'websockets>=3.0',],
       classifiers=[
           'Development Status :: 3 - Alpha',
           'Intended Audience :: Education',
           'Operating System :: OS Independent',
           'Programming Language :: Python :: 3.5',
       ],
)
