
Asynchronous Peripherals
------------------------

This section describes how to access some miscellaneous peripherals on the
Linkbot, such as the buttons, accelerometer, multicolor LED, and buzzer. The
functions described here are asynchronous in nature, designed to be used with
Python 3.5's new asyncio module.

Accelerometer
+++++++++++++

A Linkbot's accelerometer object can be accessed via the "accelerometer" member
of the AsyncLinkbot class. For instance,

.. literalinclude:: snippets/accelerometer1.py
   :language: python

.. autoclass:: linkbot.peripherals.Accelerometer
   :members:

Buttons
+++++++

.. autoclass:: linkbot.peripherals.Button
   :members:

Multi-Color LED
+++++++++++++++

.. autoclass:: linkbot.peripherals.Led
   :members:
