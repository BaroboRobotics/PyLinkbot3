import asyncio
import functools
import logging
import os
import ribbonbridge as rb
import sfp
from . import peripherals
from .. import _util as util
import websockets

__all__ = ['AsyncLinkbot']

_dirname = os.path.dirname(os.path.realpath(__file__))

class _DaemonProxy(rb.Proxy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_protocol(self, protocol):
        self._protocol = protocol

    async def rb_emit_to_server(self, bytestring):
        await self._protocol.send(bytestring)

class _AsyncLinkbot(rb.Proxy):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def __del__(self):
        self.close()

    @classmethod
    async def create(cls, serial_id):
        logging.info('Creating async Linkbot handle to ID:{}'.format(serial_id))
        self = cls( os.path.join(_dirname, 'robot_pb2.py'))
        if os.environ.get('LINKBOT_USE_WEBSOCKETS'):
            self.__use_websockets = True
        else:
            self.__use_websockets = False
        self._serial_id = serial_id
        self._loop = asyncio.get_event_loop()

        self.__daemon = _DaemonProxy(
                os.path.join(_dirname, 'daemon_pb2.py'))

        if self.__use_websockets:
            self.__log('Creating Websocket connection to daemon...')
            protocol = await websockets.connect(
                    'ws://localhost:42000', loop=self._loop)
        else:
            self.__log('Creating tcp connection to daemon...')
            (transport, protocol) = await sfp.client.connect(
                    'localhost', '42000', loop=self._loop)

        self.__log('Daemon TCP connection established.')
        protocol.connection_lost = self.__connection_closed

        self.__daemon.set_protocol(protocol)
        daemon_consumer = asyncio.ensure_future(self.__daemon_consumer(protocol))
        self.__log('Initiating daemon handshake...')
        await asyncio.sleep(0.5)
        await self.__daemon.rb_connect()
        self.__log('Daemon handshake finished.')

        self.__log('Resolving serial id...')
        args = self.__daemon.rb_get_args_obj('resolveSerialId')
        args.serialId.value = serial_id
        result_fut = await self.__daemon.resolveSerialId(args)
        tcp_endpoint = await result_fut
        self.__log('Disconnecting from daemon.')
        await protocol.close()
        daemon_consumer.cancel()
        self.__log('Connecting to robot endpoint...')
        if self.__use_websockets:
            linkbot_protocol = await websockets.client.connect(
                    'ws://'+tcp_endpoint.endpoint.address+':'+str(tcp_endpoint.endpoint.port),
                    loop=self._loop)
        else:
            (_, linkbot_protocol) = \
                    await sfp.client.connect(
                            tcp_endpoint.endpoint.address,
                            tcp_endpoint.endpoint.port)
        self.__linkbot_consumer_handle = \
            asyncio.ensure_future(self.__linkbot_consumer(linkbot_protocol))
        self.__log('Connected to robot endpoint.')
        self._linkbot_protocol = linkbot_protocol
        self.__log('Sending connect request to robot...')
        await asyncio.sleep(0.5)
        await self.rb_connect()
        self.__log('Done sending connect request to robot.')

        #Get the form factor
        fut = await self.getFormFactor()
        result_obj = await fut
        self.form_factor = result_obj.value
        return self

    async def __daemon_consumer(self, protocol):
        while True:
            try:
                msg = await protocol.recv()
            except asyncio.CancelledError:
                return
            await self.__daemon.rb_deliver(msg)

    async def __linkbot_consumer(self, protocol):
        while True:
            try:
                msg = await protocol.recv()
            except asyncio.CancelledError:
                return
            await self.rb_deliver(msg)

    def close(self):
        self._linkbot_protocol.close()
        self.__linkbot_consumer_handle.cancel()

    def __connection_closed(self, exc):
        ''' Called when the connection is closed from the other end.
           
            :param exc: An exception or "None"
        '''
        if exc:
            self.__log('Remote closed connection: '+str(exc), 'warning')
        else:
            self.__log('Remote closed connection gracefully.')
        self.rb_close()

    async def rb_emit_to_server(self, bytestring):
        await self._linkbot_protocol.send(bytestring)

    def __log(self, msg, logtype='info'):
        getattr(logging, logtype)(self._serial_id + ': ' + msg)

    async def event_handler(self, payload):
        joint = payload.encoder
        value = payload.value
        timestamp = payload.timestamp
        try:
            await self._handlers[joint](util.rad2deg(value), timestamp)
        except IndexError:
            # Don't care if the callback doesn't exist
            pass
        except TypeError:
            pass

    def set_event_handler(self, index, callback):
        assert(index >= 0 and index < 3)
        self._handlers[index] = callback

class AsyncLinkbot():
    @classmethod
    async def create(cls, serial_id):
        """ Create a new asynchronous Linkbot object.

        :param serial_id: The robot to connect to
        :type serial_id: str
        :returns: AsyncLinkbot() object.
        """
        try:
            self = cls()
            self._proxy = await asyncio.wait_for( _AsyncLinkbot.create(serial_id), 
                                                  util.DEFAULT_TIMEOUT )
            self.rb_add_broadcast_handler = self._proxy.rb_add_broadcast_handler
            self.close = self._proxy.close
            self.enableButtonEvent = self._proxy.enableButtonEvent
            self._accelerometer = await peripherals.Accelerometer.create(self)
            self._battery = await peripherals.Battery.create(self)
            self._button = await peripherals.Button.create(self)
            self._buzzer = await peripherals.Buzzer.create(self)
            self._eeprom_obj = await peripherals.Eeprom.create(self)
            self._led = await peripherals.Led.create(self)
            self._motors = await peripherals.Motors.create(self)
            self._timeouts = util.TimeoutCore(asyncio.get_event_loop())
            self._serial_id = serial_id

            # Enable joint events
            await self._proxy.enableJointEvent(enable=True)
            self._proxy.rb_add_broadcast_handler('jointEvent', self.__joint_event)
            self._proxy.rb_add_broadcast_handler('debugMessageEvent',
                    self.__debug_message_event)
            return self
        except asyncio.TimeoutError:
            raise asyncio.TimeoutError(
                'Timed out trying to connect to remote robot. Please ensure '
                'that the remote robot is on and not currently connected to '
                'another computer.' )

    @property
    def accelerometer(self):
        """
        The Linkbot accelerometer.

        See :class:`linkbot.async.peripherals.Accelerometer`.
        """
        return self._accelerometer

    @property
    def battery(self):
        """
        The Linkbot battery.

        Access the Linkbot's battery voltage. See
        :class:`linkbot.async.peripherals.Battery`
        """
        return self._battery

    @property
    def buttons(self):
        """
        Access to the Linkbot's buttons. 

        See :class:`linkbot.async.peripherals.Button`.
        """
        return self._button

    @property
    def buzzer(self):
        """
        Access to the Linkbot's buzzer.

        See :class:`linkbot.async.peripherals.Buzzer`.
        """
        return self._buzzer

    @property
    def _eeprom(self):
        """
        Access the robot's EEPROM memory.

        Warning: Improperly accessing the robot's EEPROM memory may yield
        unexpected results. The robot uses EEPROM memory to store information
        such as its serial ID, calibration data, etc.
        """
        return self._eeprom_obj

    @property
    def led(self):
        """
        The Linkbot multicolor LED.

        See :class:`linkbot.async.peripherals.Led`.
        """
        return self._led

    @property
    def motors(self):
        """
        The motors of the Linkbot.

        See :class:`linkbot.async.peripherals.Motors` . To access individual motors, you may do:

            AsyncLinkbot.motors[0].is_moving()

        or similar. Also see :class:`linkbot.async.peripherals.Motor`
        """
        return self._motors

    async def version(self):
        '''
        Get the firmware version

        :returns: asyncio.Future with result (major, minor, patch)
        :rtype: asyncio.Future with result type: (int, int, int)
        '''
        def conv(payload):
            return (payload.major, payload.minor, payload.patch)

        fut = await self._proxy.getFirmwareVersion()
        user_fut = asyncio.Future()
        util.chain_futures(fut, user_fut, conv=conv)
        return user_fut

        
    async def __joint_event(self, payload):
        # Update the motor states
        self.motors[payload.joint].state = payload.event

    async def __debug_message_event(self, payload):
        logging.warning('Received DEBUG message from robot {}: {}'
                .format(self._serial_id, payload.bytestring))

