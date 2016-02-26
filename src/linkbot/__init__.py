#!/usr/bin/env python3

import asyncio
import collections
import functools
import logging
import math
import os
import ribbonbridge as rb
import sfp.asyncio
import threading
import time
import linkbot.async_peripherals as async_peripherals
import linkbot.peripherals as peripherals

_dirname = os.path.dirname(os.path.realpath(__file__))

DEFAULT_TIMEOUT = 10

class _Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class _SortedList():
    def __init__(self, key=None):
        self._members = []
        self._key = key
        self._waiters = collections.deque()

    async def add(self, item):
        self._members.append(item)
        self._members.sort(key=self._key)
        if len(self._waiters) > 0:
            waiter = self._waiters.popleft()
            waiter.set_result(None)

    async def popleft(self):
        while len(self._members) == 0:
            fut = asyncio.Future()
            self._waiters.append(fut)
            await fut
            if fut.cancelled():
                raise asyncio.QueueEmpty()
        return self._members.pop(0)

    async def close(self):
        for w in self._waiters:
            w.cancel()

class _TimeoutCore(metaclass=_Singleton):
    def __init__(self, loop):
        self._event = asyncio.Event()
        self._cancelled = False
        # Each timeout object will be a (timestamp, asyncio.Future()) object.
        self._timeouts = _SortedList(key=lambda x: x[0])
        loop.create_task(self._work())

    async def add(self, fut, timeout):
        timestamp = time.time() + timeout
        await self._timeouts.add( (timestamp, fut) )
        self._event.set()

    async def cancel(self):
        self._cancelled = True
        self._event.set()
    
    async def chain_futures(self, fut1, fut2, callback, timeout=DEFAULT_TIMEOUT):
        # Execute 'callback' when fut1 completes. fut2's result will be set to the
        # return value of 'callback'. If timeout is specified, fut2 will be
        # cancelled after the time specified by 'timeout' has lapsed.
        # Signature of callback should be callback(future) -> result

        def __handle_chain_futures(fut2, cb, fut1):
            if fut1.cancelled() and not fut2.done():
                fut2.cancel()
            else:
                fut2.set_result(cb(fut1))

        fut1.add_done_callback(
                functools.partial(__handle_chain_futures,
                                  fut2,
                                  callback
                                  )
                )
        if timeout:
            await self.add(fut2, timeout)

    async def _work(self):
        while True:
            next_timeout = await self._timeouts.popleft()
            if next_timeout[0] > time.time():
                self._event.clear()
                try:
                    await asyncio.wait_for( self._event.wait(), 
                                            next_timeout[0]-time.time() )
                    # If we get here, the event was signalled. Check the
                    # cancellation flag
                    if self._cancelled:
                        break
                    else:
                        continue
                except asyncio.TimeoutError:
                    # Cancel the future if it is not done
                    if not next_timeout[1].done():
                        next_timeout[1].set_exception(
                                asyncio.TimeoutError('Future timeout out waiting for result.')
                                )

class _IoCore(metaclass=_Singleton):
    _num_instances = 0

    def __init__(self):
        self._initializing = True
        self._initializing_sig = threading.Condition()
        self.loop = None
        self._thread = threading.Thread(target=self._work)

    def close(self):
        self._num_instances -= 1
        if self._num_instances == 0:
            self.stop_work()
    
    def start_work(self):
        self._num_instances += 1
        if self._thread.is_alive():
            return
        self._thread.start()

        self._initializing_sig.acquire()
        while self._initializing:
            self._initializing_sig.wait(timeout=1)
        self._initializing_sig.release()

    def stop_work(self):
        self.loop.stop()

    def get_event_loop(self):
        return self.loop

    def _work(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self._initializing_sig.acquire()
        self._initializing = False
        self._initializing_sig.notify_all()
        self._initializing_sig.release()
        self.loop.run_forever()

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
            await self._handlers[joint](_rad2deg(value), timestamp)
        except IndexError:
            # Don't care if the callback doesn't exist
            pass
        except TypeError:
            pass

    def set_event_handler(self, index, callback):
        assert(index >= 0 and index < 3)
        self._handlers[index] = callback

class FormFactor():
    I = 0
    L = 1
    T = 2
    DONGLE = 3

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
                                                  DEFAULT_TIMEOUT )
            self.rb_add_broadcast_handler = self._proxy.rb_add_broadcast_handler
            self.close = self._proxy.close
            self.enableButtonEvent = self._proxy.enableButtonEvent
            self._accelerometer = await async_peripherals.Accelerometer.create(self._proxy)
            self._button = await async_peripherals.Button.create(self._proxy)
            self._buzzer = await async_peripherals.Buzzer.create(self._proxy)
            self._led = await async_peripherals.Led.create(self._proxy)
            self._motors = await async_peripherals.Motors.create(self._proxy)
            self._timeouts = _TimeoutCore(asyncio.get_event_loop())
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

        See :class:`linkbot.async_peripherals.Accelerometer`.
        """
        return self._accelerometer

    @property
    def button(self):
        """
        Access to the Linkbot's buttons. 

        See :class:`linkbot.async_peripherals.Button`.
        """
        return self._button

    @property
    def buzzer(self):
        """
        Access to the Linkbot's buzzer.

        See :class:`linkbot.async_peripherals.Buzzer`.
        """
        return self._buzzer

    @property
    def led(self):
        """
        The Linkbot multicolor LED.

        See :class:`linkbot.async_peripherals.Led`.
        """
        return self._led

    @property
    def motors(self):
        """
        The motors of the Linkbot.

        See :class:`linkbot.async_peripherals.Motors` . To access individual motors, you may do:

            AsyncLinkbot.motors[0].is_moving()

        or similar. Also see :class:`linkbot.async_peripherals.Motor`
        """
        return self._motors

    async def __joint_event(self, payload):
        # Update the motor states
        self.motors[payload.joint].state = payload.event

    async def __debug_message_event(self, payload):
        logging.warning('Received DEBUG message from robot {}: {}'
                .format(self._serial_id, payload.bytestring))

class _Linkbot():
    def __init__(self, serial_id):
        self.__iocore = _IoCore()

        self._proxy = asyncio.run_coroutine_threadsafe(
                AsyncLinkbot.create(serial_id),
                self.__iocore.get_event_loop()
                )

    def __getattr__(self, name):
        if name not in self._proxy.rb_procedures():
            raise AttributeError('{} is not a Linkbot member function.'
                    .format(name) )
        return functools.partial(
                self._handle_rpc, name
                )

    def _handle_rpc(self, name, args_obj=None, **kw):
        if not args_obj:
            args_obj = self._proxy.rb_get_args_obj()
            for k,v in kw.items():
                setattr(args_obj, k, v)
        fut = asyncio.run_coroutine_threadsafe(
                getattr(self._proxy, name)(args_obj),
                self.__iocore.get_event_loop()
                )
        return fut

class Linkbot():
    def __init__(self, serial_id):
        #self.__iocore = _IoCore()
        #self.__iocore.start_work()
        #time.sleep(1)
        #self._loop = self.__iocore.get_event_loop()
        self._loop = asyncio.get_event_loop()
    
        '''
        fut = asyncio.run_coroutine_threadsafe(
                AsyncLinkbot.create(serial_id),
                self._loop)
        self._alinkbot = fut.result()
        '''
        self._alinkbot = self._loop.run_until_complete(
                AsyncLinkbot.create(serial_id))

        self.motors = peripherals.Motors(self._alinkbot.motors, self._loop)

