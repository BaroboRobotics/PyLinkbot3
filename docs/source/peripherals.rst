The Linkbot Peripherals
-----------------------

This section describes how to access all of the Linkbots peripherals, such as its 
its motors, LED, buzzer, buttons, accelerometer, and I2C expansion port.

.. automodule:: linkbot3

Accelerometer
+++++++++++++

A Linkbot's accelerometer object can be accessed via the "accelerometer" member
of the AsyncLinkbot class. For instance,

.. literalinclude:: snippets/Linkbot/accelerometer.py
   :language: python

.. autoclass:: linkbot3.peripherals.Accelerometer
   :members:

Battery
+++++++
Get a Linkbot's current battery voltage or percentage level.

.. literalinclude:: snippets/Linkbot/battery.py
   :language: python

.. autoclass:: linkbot3.peripherals.Battery
   :members:

Buttons
+++++++

A Linkbot's button functions can be overridden from their default functions. The
power button can also be overridden, but the robot will still turn off if the
button is held for more than 2 seconds. The power-off button functionality
cannot be overridden. For example,

.. literalinclude:: snippets/Linkbot/buttons.py
   :language: python

.. autoclass:: linkbot3.peripherals.Button
   :members:

Buzzer
++++++

The Linkbot's buzzer can play tones ranging from low buzzes to frequencies
higher than most humans can perceive. 

.. literalinclude:: snippets/Linkbot/buzzer.py

.. autoclass:: linkbot3.peripherals.Buzzer
   :members:

Multi-Color LED
+++++++++++++++

Control a Linkbot's LED color through this interface.

.. literalinclude:: snippets/Linkbot/led.py
   :language: python

.. autoclass:: linkbot3.peripherals.Led
   :members:

Motor
+++++

.. autoclass:: linkbot3::peripherals.Motor.Controller
   :members: 
   :undoc-members:

.. autoclass:: linkbot3::peripherals.Motor.State
   :members: 
   :undoc-members:

.. autoclass:: linkbot3::peripherals.Motor
   :members: 

Motors
++++++

.. autoclass:: linkbot3::peripherals.Motors
   :members:

Peripheral
++++++++++

The parent class for (most) Linkbot peripherals.

.. autoclass:: linkbot3.peripherals.Peripheral
   :members:

