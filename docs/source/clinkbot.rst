
The CLinkbot Class
==================
( since version 3.1.0 )

( As of version 3.1.17, the Linkbot class is identical to the CLinkbot class )

.. toctree::
   :maxdepth: 2
   
The :class:`linkbot3.CLinkbot` class is an alternative to the
`linkbot3.Linkbot` class. The API style is more closely aligned to the API
style used by the C-STEM Ch Linkbot binding, popular in some schools which are
a part of the C-STEM program <http://c-stem.ucdavis.edu>.

Note that the documentation lists all of the member functions in a PEP8
compliant format, using all lower-case and underscores. However, there is an
internal mechanism that allows camel-humped member functions to be used too,
which is the style of the original C-STEM API. 

For instance, the documentation lists a function called::

    linkbot3.drive_to_nb()

For each function name like this, there also exists an undocumented member
function::

    linkbot3.driveToNB()

which is the original C-STEM naming style of the function.

Blocking versus Non-Blocking Movement Functions
-----------------------------------------------

The C-STEM API uses the suffix "nb" (or "NB") to denote a "non-blocking"
movement function. The non-blocking movement functions return before
the motion in question is finished. For instance, the following two snippets of 
code are identical::

    import linkbot3 as linkbot
    l = linkbot.CLinkbot('ABCD') # My robot's ID is "ABCD"
    l.move_nb(90, 90, 90) # Begin moving each motor 90 degrees
    l.move_wait()         # Wait for the motion to complete
    l.set_led_color(255, 0, 0)  # Change the LED color

and::

    import linkbot3 as linkbot
    l = linkbot.CLinkbot('ABCD') # My robot's ID is "ABCD"
    l.move(90, 90, 90) # Move each motor 90 degrees AND wait for motion to finish
    l.set_led_color(255, 0, 0) # Change the LED color

CLinkbot API Documentation
--------------------------

.. autoclass:: linkbot3.CLinkbot
   :members:
   :inherited-members:

