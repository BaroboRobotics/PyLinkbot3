#!/usr/bin/env python3

import asyncio
import collections
import functools
import logging
import math
import os
import threading
import time
from . import peripherals
from . import _util as util

from .async import *

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
        
        self._motors = peripherals.Motors(self._alinkbot.motors, self._loop)

    @property
    def motors(self):
        """
        The motors of the Linkbot.

        See :class:`linkbot.peripherals.Motors` . To access individual motors,
        you may do::

            Linkbot.motors[0].is_moving()

        or similar. Also see :class:`linkbot.peripherals.Motor`
        """
        return self._motors

