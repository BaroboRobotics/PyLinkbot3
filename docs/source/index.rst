.. PyLinkbot3 documentation master file, created by
   sphinx-quickstart on Fri Feb 12 17:15:19 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyLinkbot3's documentation!
======================================

Contents:

.. toctree::
   :maxdepth: 2

   asynclinkbot
   motors
   peripherals

Introduction
============

This package is used to control a Linkbot. Linkbots are small modular robots used
in classrooms to teach programming, math, and science.

The :class:`AsyncLinkbot` class is an asynchronous handle to a remote Linkbot.
It is meant to be used in an :module:`asyncio` coroutine. The class itself
contains several child classes that represent various peripherals on the
Linkbot, such as the motors, buttons, accelerometer, and LED. 

Here is a small piece of sample code showing how to move a Linkbot's motors to
their zero positions using the asynchronous :class:`AsyncLinkbot` object. In
this example, the Linkbot's serial ID is 'ABCD':

.. literalinclude:: snippets/demo1.py
   :language: python


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

