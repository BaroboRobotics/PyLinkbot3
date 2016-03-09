
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

.. literalinclude:: snippets/async/accelerometer.py
   :language: python

.. autoclass:: linkbot.async.peripherals.Accelerometer
   :members:

Battery
+++++++
Get a Linkbot's current battery voltage or percentage level.

.. autoclass:: linkbot.async.peripherals.Battery
   :members:

Buttons
+++++++

A Linkbot's button functions can be overridden from their default functions. The
power button can also be overridden, but the robot will still turn off if the
button is held for more than 2 seconds. The power-off button functionality
cannot be overridden. For example,

.. literalinclude:: snippets/async/buttons.py
   :language: python

.. autoclass:: linkbot.async.peripherals.Button
   :members:

Buzzer
++++++

The Linkbot's buzzer can play tones ranging from low buzzes to frequencies
higher than most humans can perceive. 

.. autoclass:: linkbot.async.peripherals.Buzzer
   :members:

Multi-Color LED
+++++++++++++++

Control a Linkbot's LED color through this interface.

.. literalinclude:: snippets/async/led.py
   :language: python

.. autoclass:: linkbot.async.peripherals.Led
   :members:

Motor
+++++
Move and sense from individual motors.

.. literalinclude:: snippets/async/smooth.py
   :language: python 

.. autoclass:: linkbot.async.peripherals.Motor
   :members:

Motors
++++++

.. autoclass:: linkbot.async.peripherals.Motors
   :members:
