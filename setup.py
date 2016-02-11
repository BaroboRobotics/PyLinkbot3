#!/usr/bin/env python3

from setuptools import setup

import sys
if sys.version_info < (3, 5):
    print('Python 3.5 or higher is required to use PyLinkbot3.')
    sys.exit(1)

setup (name = 'PyLinkbot',
       author = 'David Ko',
       author_email = 'david@barobo.com',
       version = '3.0.0a0',
       description = "This is a pure Python implementation of PyLinkbot. See http://github.com/BaroboRobotics/PyLinkbot",
       package_dir = {'':'src'},
       packages = ['linkbot'],
       url = 'http://github.com/BaroboRobotics/PyLinkbot3',
       install_requires=['protobuf>=3.0.0b2', 'PyRibbonBridge'],
       )
