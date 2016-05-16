.. PyLinkbot3 documentation master file, created by
   sphinx-quickstart on Fri Feb 12 17:15:19 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyLinkbot3's documentation!
======================================

This package is used to control a Linkbot. Linkbots are small modular robots used
in classrooms to teach programming, math, and science.

This package includes two main interfaces to the Linkbot. One is an asynchronous
interface designed to be used with Python 3.5's :mod:`asyncio` module. This one is
called :class:`linkbot3.AsyncLinkbot`.

We also provide a synchronous interface called :class:`linkbot3.Linkbot` which is built
on top of the asynchronous interface. This one is arguably easier to use since
it hides all of the asynchronous details from the user. However, there are
certain tasks, such as sending commands to a fleet of Linkbots, which may be
better suited for the asynchronous interface.

Contents
========

.. toctree::
   :maxdepth: 3

   linkbot
   asynclinkbot


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

