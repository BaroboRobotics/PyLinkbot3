import asyncio
import functools
import logging
import os
import ribbonbridge as rb
import sfp.asyncio
from . import peripherals
from .. import _util as util

__all__ = ['AsyncLinkbot']

_dirname = os.path.dirname(os.path.realpath(__file__))

class _SfpProxy(rb.Proxy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_protocol(self, protocol):
        self._protocol = protocol

    async def rb_emit_to_server(self, bytestring):
        self._protocol.write(bytestring)

class _AsyncLinkbot(rb.Proxy):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    @classmethod
    async def create(cls, serial_id):
        logging.info('Creating async Linkbot handle to ID:{}'.format(serial_id))
        self = cls( os.path.join(_dirname, 'robot_pb2.py'))
        self._serial_id = serial_id
        self.__daemon = _SfpProxy(
                os.path.join(_dirname, 'daemon_pb2.py'))

        loop = asyncio.get_event_loop()
        self.__log('Creating tcp connection to daemon...')
        (transport, protocol) = await loop.create_connection(
                functools.partial(
                    sfp.asyncio.SfpProtocol,
                    self.__daemon.rb_deliver,
                    loop),
                'localhost', '42000' )
        self.__log('Daemon TCP connection established.')
        protocol.connection_lost = self.__connection_closed

        self.__log('Setting daemon protocol...')
        self.__daemon.set_protocol(protocol)
        self.__log('Initiating daemon handshake...')
        await asyncio.sleep(0.5)
        await self.__daemon.rb_connect()
        self.__log('Daemon handshake finished.')

        self.__log('Resolving serial id...')
        args = self.__daemon.rb_get_args_obj('resolveSerialId')
        args.serialId.value = serial_id
        result_fut = await self.__daemon.resolveSerialId(args)
        tcp_endpoint = await result_fut
        self.__log('Connecting to robot endpoint...')
        (linkbot_transport, linkbot_protocol) = \
            await loop.create_connection(
                    functools.partial(
                        sfp.asyncio.SfpProtocol,
                        self.rb_deliver,
                        loop),
                    tcp_endpoint.endpoint.address,
                    str(tcp_endpoint.endpoint.port) )
        self.__log('Connected to robot endpoint.')
        self._linkbot_transport = linkbot_transport
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

    def close(self):
        self._linkbot_transport.close()

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
        self._linkbot_protocol.write(bytestring)

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
            self._accelerometer = await peripherals.Accelerometer.create(self._proxy)
            self._button = await peripherals.Button.create(self._proxy)
            self._buzzer = await peripherals.Buzzer.create(self._proxy)
            self._led = await peripherals.Led.create(self._proxy)
            self._motors = await peripherals.Motors.create(self._proxy)
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
    def button(self):
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

    async def __joint_event(self, payload):
        # Update the motor states
        self.motors[payload.joint].state = payload.event

    async def __debug_message_event(self, payload):
        logging.warning('Received DEBUG message from robot {}: {}'
                .format(self._serial_id, payload.bytestring))

