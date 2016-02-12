#!/usr/bin/env python3

import asyncio
import functools
import logging
import math
import os
import ribbonbridge as rb
import sfp.asyncio
import threading

_dirname = os.path.dirname(os.path.realpath(__file__))

def _rad2deg(rad):
    return rad*180/math.pi

def _deg2rad(deg):
    return deg*math.pi/180

class _Singleton(type):
    instance = None
    def __call__(cls, *args, **kw):
        if not cls.instance:
            cls.instance = super(_Singleton, cls).__call__(*args, **kw)
        return cls.instance

class _IoCore():
    __metaclass__ = _Singleton

    def __init__(self):
        self._initializing = True
        self._initializing_sig = threading.Condition()
        self.loop = None
        self._thread = threading.Thread(target=self._work)
        self._thread.start()

        self._initializing_sig.acquire()
        while self._initializing:
            self._initializing_sig.wait(timeout=1)
        self._initializing_sig.release()

    def get_event_loop(self):
        return self.loop

    def _work(self):
        self.loop = asyncio.new_event_loop()
        self._initializing_sig.acquire()
        self._initializing = False
        self._initializing_sig.notify_all()
        self._initializing_sig.release()
        logging.info('Starting event loop.')
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
        self.__daemon = _SfpProxy(
                os.path.join(_dirname, 'daemon_pb2.py'))

        loop = asyncio.get_event_loop()
        logging.info('Creating tcp connection to daemon...')
        (transport, protocol) = await loop.create_connection(
                functools.partial(
                    sfp.asyncio.SfpProtocol,
                    self.__daemon.rb_deliver,
                    loop),
                'localhost', '42000' )
        logging.info('Daemon TCP connection established.')

        logging.info('Setting daemon protocol...')
        self.__daemon.set_protocol(protocol)
        logging.info('Initiating daemon handshake...')
        await asyncio.sleep(0.5)
        await self.__daemon.rb_connect()
        logging.info('Daemon handshake finished.')

        logging.info('Resolving serial id...')
        args = self.__daemon.rb_get_args_obj('resolveSerialId')
        args.serialId.value = serial_id
        result_fut = await self.__daemon.resolveSerialId(args)
        tcp_endpoint = await result_fut
        logging.info('Connecting to robot endpoint...')
        (linkbot_transport, linkbot_protocol) = \
            await loop.create_connection(
                    functools.partial(
                        sfp.asyncio.SfpProtocol,
                        self.rb_deliver,
                        loop),
                    tcp_endpoint.endpoint.address,
                    str(tcp_endpoint.endpoint.port) )
        logging.info('Connected to robot endpoint.')
        self._linkbot_transport = linkbot_transport
        self._linkbot_protocol = linkbot_protocol
        logging.info('Sending connect request to robot...')
        await asyncio.sleep(0.5)
        await self.rb_connect()
        logging.info('Done sending connect request to robot.')

        #Get the form factor
        fut = await self.getFormFactor()
        result_obj = await fut
        self.form_factor = result_obj.value
        return self

    def close(self):
        self._linkbot_transport.close()

    async def rb_emit_to_server(self, bytestring):
        logging.info('Emitting bytestring to protocol layer...')
        self._linkbot_protocol.write(bytestring)

class Motor:
    class Controller:
        PID = 1
        CONST_VEL = 2
        SMOOTH = 3

    class State:
        COAST = 0
        HOLD = 1
        MOVING = 2
        ERROR = 4

    def __init__(self, index, proxy):
        self._controller = self.Controller.CONST_VEL
        self._index = index
        self._proxy = proxy

    async def controller(self):
        '''The movement controller.

        This property controls the strategy with which the motors are moved.
        Legal values are:
        AsyncLinkbot.MoveController.PID: Move the motors directly with the
            internal PID controller. This is typically the fastest way to get a
            motor from one position to another. The motor may experience some
            overshoot and underdamped response when moving larger distances.
        AsyncLinkbot.MoveController.CONST_VEL: Move the motor at a constant
            velocity. This motor controller attemts to accelerate and decelerate
            a motor infinitely fast to and from a constant velocity to move the
            motor from one position to the next. The velocity can be controlled
            by setting the property "omega".
        AsyncLinkbot.MoveController.SMOOTH: Move the motor with specified
            acceleration, maximum velocity, and deceleration. For this type of
            movement, access maximum velocity with property "omega",
            acceleration with property "acceleration", and deceleration with property
            "deceleration".
        '''
        fut = asyncio.Future()
        fut.set_result(self._controller)
        return fut

    async def set_controller(self, value):
        if value < 1 or value > 3:
            raise RangeError('Motor controller must be a value in range [1,3]')
        self._controller = value
        fut = asyncio.Future()
        fut.set_result(None)
        return fut

    async def accel(self):
        # Get the acceleration setting of a motor
        return await self.__get_motor_controller_attribute(
                'getMotorControllerAlphaI',
                conv=_rad2deg
                )

    async def omega(self):
        # Get the rotational velocity setting of a motor
        return await self.__get_motor_controller_attribute(
                'getMotorControllerOmega',
                conv=_rad2deg
                )

    async def __get_motor_controller_attribute(self, name, conv=lambda x: x):
        # 'conv' is a conversion function, in case the returned values need to
        # be converted to/from radians. Use 'id' for null conversion
        fut = await getattr(self._proxy, name)()
        user_fut = asyncio.Future()
        fut.add_done_callback(
                functools.partial(
                    self.__handle_values_result, conv, user_fut)
                )
        return user_fut

    def __handle_values_result(self, conv, user_fut, fut):
        results_obj = fut.result()
        values = []
        for v in results_obj.values:
            values.append(conv(v))
        if self._proxy.form_factor == FormFactor.I:
            values.append(0.0)
        elif self._proxy.form_factor == FormFactor.L:
            values.insert(1, 0.0)
        user_fut.set_result(values[self._index])

    async def set_accel(self, value):
        return await self.__set_motor_controller_attribute(
                'setMotorControllerAlphaI',
                _deg2rad(value)
                )

    async def __set_motor_controller_attribute(self, name, value):
        args_obj = self._proxy.rb_get_args_obj(name)
        args_obj.mask = 1<<self._index
        args_obj.values.append(value)
        fut = await getattr(self._proxy, name)(args_obj)
        user_fut = asyncio.Future()
        fut.add_done_callback(
                functools.partial(
                    self.__handle_set_attribute,
                    user_fut
                    )
                )
        return user_fut

    def __handle_set_attribute(self, user_fut, fut):
        user_fut.set_result( fut.result() )

class Motors:
    def __init__(self, proxy):
        self._proxy = proxy
        self.motors = [Motor(i, proxy) for i in range(3)]

    def __getitem__(self, key):
        return self.motors[key]

    async def angles(self):
        fut = await self._proxy.getEncoderValues()
        user_fut = asyncio.Future()
        fut.add_done_callback(
                functools.partial(
                    self.__angles, user_fut)
                )
        return user_fut

    def __angles(self, user_fut, fut):
        results_obj = fut.result()
        results = (results_obj.timestamp,)
        for angle in results_obj.values:
            results = results + (_rad2deg(angle),)
        user_fut.set_result(results)

    async def set_angles(self, angles, mask, relative=False, timeouts=None,
            states_on_timeout = None):
        angles = list(map(_deg2rad, angles))
        args_obj = self._proxy.rb_get_args_obj('move')
        names = ['motorOneGoal', 'motorTwoGoal', 'motorThreeGoal']
        if relative:
            move_type = 2
        else:
            move_type = 1
        for i,name in enumerate(names):
            if mask&(1<<i):
                getattr(args_obj,name).type = move_type
                getattr(args_obj,name).goal = angles[i]
                fut = await self.motors[i].controller()
                getattr(args_obj,name).controller = await fut
                if timeouts:
                    getattr(args_obj,name).timeout = timeouts[i]
                if states_on_timeout:
                    getattr(args_obj,name).modeOnTimeout = states_on_timeout[i]

        fut = await self._proxy.move(args_obj)
        return fut

class FormFactor():
    I = 0
    L = 1
    T = 2
    DONGLE = 3

class AsyncLinkbot():
    @classmethod
    async def create(cls, serial_id):
        self = cls()
        self._proxy = await _AsyncLinkbot.create(serial_id)
        self.rb_add_broadcast_handler = self._proxy.rb_add_broadcast_handler
        self.close = self._proxy.close
        self.enableButtonEvent = self._proxy.enableButtonEvent
        self.motors = Motors(self._proxy)
        return self

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


