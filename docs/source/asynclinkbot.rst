
The AsyncLinkbot Class
======================

.. toctree::
   :maxdepth: 2
   
   async_peripherals.rst

The :class:`linkbot3.AsyncLinkbot` class is an asynchronous handle to a remote Linkbot.
It is meant to be used in an :mod:`asyncio` coroutine. The class itself
contains several child classes that represent various peripherals on the
Linkbot, such as the motors, buttons, accelerometer, and LED. 

Here is a small piece of sample code showing how to move a Linkbot's motors 
using the asynchronous :class:`linkbot3.AsyncLinkbot` object. 

.. literalinclude:: snippets/demo1.py
   :language: python

AsyncLinkbot API Documentation
------------------------------

.. autoclass:: linkbot3.AsyncLinkbot
   :members:

