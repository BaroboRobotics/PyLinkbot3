#!/usr/bin/env python3

import asyncio
from . import _util as util

from .async import *
from .peripherals import *
import websockets

__all__ = ['FormFactor', 'Linkbot', ]
__all__ += [async.__all__, ]

class Daemon():
    def __init__(self):
        self.__io_core = util.IoCore()
        self._loop = self.__io_core.get_event_loop()
    
        fut = util.run_coroutine_threadsafe(
                AsyncDaemon.create(), self._loop)
        try:
            self._proxy = fut.result()
        except:
            raise Exception("Could not connect to daemon.")

    def cycle(self, seconds):
        util.run_coroutine_threadsafe(
            self._proxy.cycle(seconds),
            self._loop)


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
    
        fut = util.run_coroutine_threadsafe(
                AsyncLinkbot.create(serial_id), self._loop)
        self._proxy = fut.result()
       
        self._accelerometer = Accelerometer(self)
        self._battery = Battery(self)
        self._button = Button(self)
        self._buzzer = Buzzer(self)
        self._eeprom_obj = Eeprom(self)
        self._led = Led(self)
        self._motors = Motors(self)

    @property
    def accelerometer(self):
        '''
        The robot accelerometer.

        See :class:`linkbot3.peripherals.Accelerometer`
        '''
        return self._accelerometer

    @property
    def battery(self):
        '''
        The robot battery.

        See :class:`linkbot3.peripherals.Battery`
        '''
        return self._battery

    @property
    def buttons(self):
        '''
        Access to the robot's buttons.

        See :class:`linkbot3.peripherals.Button`
        '''
        return self._button

    @property
    def buzzer(self):
        '''
        Control the Linkbot's buzzer.

        See :class:`linkbot3.peripherals.Buzzer`
        '''
        return self._buzzer

    def disconnect(self):
        '''
        Disconnect from the Linkbot.
        '''
        util.run_coroutine_threadsafe(self._proxy.disconnect(), self._loop)

    @property
    def _eeprom(self):
        """
        Access the robot's EEPROM memory.

        Warning: Improperly accessing the robot's EEPROM memory may yield
        unexpected results. The robot uses EEPROM memory to store information
        such as its serial ID, calibration data, etc.
        """
        return self._eeprom_obj

    def form_factor(self):
        '''
        Get the form factor of the Linkbot. See :class:`linkbot3.FormFactor`.
        '''
        return util.run_linkbot_coroutine(self._proxy.form_factor(), self._loop)

    @property
    def led(self):
        '''
        Access to the robot's multi-color LED.

        See :class:`linkbot3.peripherals.Led`.
        '''
        return self._led

    @property
    def motors(self):
        """
        The motors of the Linkbot.

        See :class:`linkbot3.peripherals.Motors` . To access individual motors,
        you may do::

            Linkbot.motors[0].is_moving()

        or similar. Also see :class:`linkbot3.peripherals.Motor`
        """
        return self._motors

    def reboot(self):
        util.run_linkbot_coroutine(
            self._proxy.reboot(),
            self._loop)
       

    def version(self):
        '''
        Get the firmware version

        :rtype: (int, int, int)
        '''
        return util.run_linkbot_coroutine(
                self._proxy.version(),
                self._loop)

def scatter_plot(xs, ys):
    ''' A helper function to generate and display graphical plots.

    :param xs: A list of x axis values, like [0, 3, 4]
    :param ys: A list of y axis values, like [2, -1, 3]
    '''
    import io
    import matplotlib
    import os
    port = None
    try:
        port = os.environ['PREX_IPC_PORT']
    except KeyError as e:
        pass
    if port:
        matplotlib.use('SVG')

    import matplotlib.pyplot as plt

    fig = matplotlib.pyplot.figure()
    ax = fig.add_subplot(111)
    ax.plot(xs, ys)
    plt.show()

    if port:
        fstream = io.BytesIO()
        fig.savefig(fstream)
        coro = __send_image('ws://localhost:'+str(port), fstream.getvalue())
        asyncio.get_event_loop().run_until_complete(coro)

@asyncio.coroutine
def __send_image(uri, data):
    websocket = yield from websockets.connect(uri)
    yield from websocket.send(data)
    yield from websocket.close()

