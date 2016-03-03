#!/usr/bin/env python3

import asyncio
import collections
import functools
import logging
import math
import os
import threading
import time
from . import _util as util

from .async import *
from .peripherals import *

__all__ = ['FormFactor', 'Linkbot', ]
__all__ += [async.__all__, ]

class FormFactor():
    I = 0
    L = 1
    T = 2
    DONGLE = 3

class Linkbot():
    def __init__(self, serial_id):
        ''' Create a new Linkbot handle.

        :param serial_id: The 4 digit alpha-numeric unique Linkbot identifier
            printed on the top of the Linkbot.
        :type serial_id: string
        :raises concurrent.futures._base.TimeoutError: if the remote robot
            cannot be be reached.
        '''
        self.__io_core = util.IoCore()
        self._loop = self.__io_core.get_event_loop()
    
        fut = asyncio.run_coroutine_threadsafe(
                AsyncLinkbot.create(serial_id), self._loop)
        self._alinkbot = fut.result()
       
        self._accelerometer = Accelerometer(
                self._alinkbot.accelerometer,
                self._loop )
        self._battery = Battery( self._alinkbot.battery,
                                 self._loop )
        self._button = Button( self._alinkbot.buttons,
                               self._loop )
        self._buzzer = Buzzer( self._alinkbot.buzzer,
                               self._loop )
        self._led = Led( self._alinkbot.led,
                         self._loop )
        self._motors = Motors(self._alinkbot.motors, self._loop)

    @property
    def accelerometer(self):
        '''
        The robot accelerometer.

        See :class:`linkbot.peripherals.Accelerometer`
        '''
        return self._accelerometer

    @property
    def battery(self):
        '''
        The robot battery.

        See :class:`linkbot.peripherals.Battery`
        '''
        return self._battery

    @property
    def buttons(self):
        '''
        Access to the robot's buttons.

        See :class:`linkbot.peripherals.Button`
        '''
        return self._button

    @property
    def buzzer(self):
        '''
        Control the Linkbot's buzzer.

        See :class:`linkbot.peripherals.Buzzer`
        '''
        return self._buzzer

    @property
    def led(self):
        '''
        Access to the robot's multi-color LED.

        See :class:`linkbot.peripherals.Led`.
        '''
        return self._led

    @property
    def motors(self):
        """
        The motors of the Linkbot.

        See :class:`linkbot.Motors` . To access individual motors,
        you may do::

            Linkbot.motors[0].is_moving()

        or similar. Also see :class:`linkbot.Motor`
        """
        return self._motors

    def _read_eeprom(self, address, size):
        '''
        Read ```size``` bytes from EEPROM address ```address``` on the robot.

        :param address: The start address to read from
        :type address: int
        :param size: The number of bytes to read
        :type size: int
        :rtype: bytestring
        '''
        return util.run_linkbot_coroutine(
            self._alinkbot._read_eeprom(address, size),
            self._loop)

    def _write_eeprom(self, address, bytestring):
        '''
        Write data to the EEPROM.

        WARNING: This function can overwrite important EEPROM data that the
        robot uses to function properly, such as its serial ID, calibration
        values, hardware versioning information, etc. 

        :param address: Start EEPROM address to write to
        :type address: int
        :param bytestring: Bytes to write to EEPROM
        :type bytestring: bytearray or bytes
        '''
        return util.run_linkbot_coroutine(
                self._alinkbot._write_eeprom(address, bytestring),
                self._loop)

    def version(self):
        '''
        Get the firmware version

        :rtype:(int, int, int)
        '''
        return util.run_linkbot_coroutine(
                self._alinkbot.version(),
                self._loop)

