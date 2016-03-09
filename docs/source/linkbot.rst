
The Linkbot Class
=================
.. toctree::
   :maxdepth: 2
   
   peripherals

The :class:`linkbot.Linkbot` class is a handle to a remote Linkbot.
The class itself
contains several child classes that represent various peripherals on the
Linkbot, such as the motors, buttons, accelerometer, and LED. 

Here is a small piece of sample code showing how to move a Linkbot's motors 
using the asynchronous :class:`linkbot.Linkbot` object. 

.. literalinclude:: snippets/Linkbot/move.py
   :language: python

.. autoclass:: linkbot.Linkbot
   :members:

