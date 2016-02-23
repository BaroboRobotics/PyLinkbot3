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
import linkbot.peripherals as peripherals

_dirname = os.path.dirname(os.path.realpath(__file__))

DEFAULT_TIMEOUT = 10

def _rad2deg(rad):
    return rad*180/math.pi

def _deg2rad(deg):
    return deg*math.pi/180


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
        self._linkbot_protocol.write(bytestring)

class _EncoderEventHandler():
    def __init__(self):
        self._handlers = [None, None, None]

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

class Motor:
    class Controller:
        PID = 1
        CONST_VEL = 2
        SMOOTH = 3
        ACCEL = 4

    class State:
        COAST = 0
        HOLD = 1
        MOVING = 2
        ERROR = 4

    class _MoveType:
        ABSOLUTE = 1
        RELATIVE = 2
        INFINITE = 3

    @classmethod
    async def create(cls, index, proxy, motors_obj):
        self = cls()
        self._controller = self.Controller.CONST_VEL
        self._index = index
        self._proxy = proxy
        self._state = Motor.State.COAST
        await self._poll_state()
        # List of futures that should be set when this joint is done moving
        self._move_waiters = []
        self._motors = motors_obj
        return self

    async def accel(self):
        # Get the acceleration setting of a motor
        return await self.__get_motor_controller_attribute(
                'getMotorControllerAlphaI',
                conv=_rad2deg
                )

    async def controller(self):
        '''The movement controller.

        This property controls the strategy with which the motors are moved.
        Legal values are:
        * AsyncLinkbot.MoveController.PID: Move the motors directly with the
        internal PID controller. This is typically the fastest way to get a
        motor from one position to another. The motor may experience some
        overshoot and underdamped response when moving larger distances.
        * AsyncLinkbot.MoveController.CONST_VEL: Move the motor at a constant
        velocity. This motor controller attemts to accelerate and decelerate
        a motor infinitely fast to and from a constant velocity to move the
        motor from one position to the next. The velocity can be controlled
        by setting the property `omega`.
        * AsyncLinkbot.MoveController.SMOOTH: Move the motor with specified
        acceleration, maximum velocity, and deceleration. For this type of
        movement, access maximum velocity with property `omega`,
        acceleration with property `acceleration`, and deceleration with property
        `deceleration`.
        '''
        fut = asyncio.Future()
        fut.set_result(self._controller)
        return fut

    async def decel(self):
        # Get the deceleration setting of a motor
        return await self.__get_motor_controller_attribute(
                'getMotorControllerAlphaF',
                conv=_rad2deg
                )

    async def omega(self):
        # Get the rotational velocity setting of a motor
        return await self.__get_motor_controller_attribute(
                'getMotorControllerOmega',
                conv=_rad2deg
                )

    async def _poll_state(self):
        if (self._index == 1) and (self._proxy.form_factor == FormFactor.I):
            self._state = Motor.State.COAST
        elif (self._index == 2) and (self._proxy.form_factor == FormFactor.L):
            self._state = Motor.State.COAST
        else:
            fut = await self.__get_motor_controller_attribute(
                    'getJointStates' )
            self._state = await fut

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
        # See :func:`accel`
        return await self.__set_motor_controller_attribute(
                'setMotorControllerAlphaI',
                _deg2rad(value)
                )

    async def set_controller(self, value):
        # See "controller"
        if value < 1 or value > 3:
            raise RangeError('Motor controller must be a value in range [1,3]')
        self._controller = value
        fut = asyncio.Future()
        fut.set_result(None)
        return fut

    async def set_decel(self, value):
        # See :func:`decel`
        return await self.__set_motor_controller_attribute(
                'setMotorControllerAlphaF',
                _deg2rad(value)
                )

    async def set_omega(self, value):
        # See :func:`omega`
        return await self.__set_motor_controller_attribute(
                'setMotorControllerOmega',
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

    async def set_event_handler(self, callback=None, granularity=2.0):
        '''
        Set a callback function to be executed when the motor angle
        values on the robot change.

        :param callback: async func(joint, angle, timestamp) -> None
        :param granularity: float . The callback will only be called when a
            motor moves away from its current position by more than
            'granularity' degrees.
        '''
        if not callback:
            # Remove the event
            try:
                args = self._proxy.rb_get_args_obj('enableEncoderEvent')
                names = ['encoderOne', 'encoderTwo', 'encoderThree']
                name = names[self._index]
                getattr(args, name).enable = False
                getattr(args, name).granularity = _deg2rad(granularity)
                fut = await self._proxy.enableEncoderEvent(args)
                await fut
                self._event_callback = callback
                return fut
            except KeyError:
                # Don't worry if the bcast handler is not there.
                pass

        else:
            self._motors._callback_handler.set_event_handler(self._index, callback)
            self._proxy.rb_add_broadcast_handler( 'encoderEvent', 
                                                  self._motors._callback_handler.event_handler)
            args = self._proxy.rb_get_args_obj('enableEncoderEvent')
            names = ['encoderOne', 'encoderTwo', 'encoderThree']
            name = names[self._index]
            getattr(args, name).enable = True
            getattr(args, name).granularity = _deg2rad(granularity)
            fut = await self._proxy.enableEncoderEvent(args)
            return fut

    async def set_power(self, power):
        '''
        Set the motor's power.

        :type power: int [-255,255]
        '''
        
        args_obj = self._proxy.rb_get_args_obj('move')
        names = ['motorOneGoal', 'motorTwoGoal', 'motorThreeGoal']
        name = names[self._index]
        getattr(args_obj,name).type = Motor._MoveType.INFINITE
        getattr(args_obj,name).goal = power
        getattr(args_obj,name).controller = Motor.Controller.PID

        fut = await self._proxy.move(args_obj)
        return fut

    def __handle_set_attribute(self, user_fut, fut):
        user_fut.set_result( fut.result() )

    def is_moving(self):
        if self._state in [self.State.COAST, self.State.HOLD]:
            return False
        else:
            return True

    @property
    def state(self):
        # The current joint state. One of :class:`Motor.State`
        return self._state
    @state.setter
    def state(self, value):
        assert(value in self.State.__dict__.values())
        self._state = value
        if not self.is_moving():
            for fut in self._move_waiters:
                fut.set_result(self._state)
            self._move_waiters.clear()

    async def begin_accel(self, timeout, v0 = 0.0, state_on_timeout=State.COAST):
        mask = 1<<self._index
        args_obj = self._proxy.rb_get_args_obj('move')
        names = ['motorOneGoal', 'motorTwoGoal', 'motorThreeGoal']
        for i,name in enumerate(names):
            if mask&(1<<i):
                getattr(args_obj,name).type = self._MoveType.INFINITE
                getattr(args_obj,name).goal = v0
                getattr(args_obj,name).controller = self.Controller.ACCEL
                getattr(args_obj,name).timeout = timeout
                getattr(args_obj,name).modeOnTimeout = state_on_timeout

        fut = await self._proxy.move(args_obj)
        return fut

    async def begin_move(self, timeout = 0, forward=True, state_on_timeout=State.COAST):
        mask = 1<<self._index
        args_obj = self._proxy.rb_get_args_obj('move')
        names = ['motorOneGoal', 'motorTwoGoal', 'motorThreeGoal']
        if forward:
            goal = 1
        else:
            goal = -1
        for i,name in enumerate(names):
            if mask&(1<<i):
                getattr(args_obj,name).type = self._MoveType.INFINITE
                getattr(args_obj,name).goal = goal
                getattr(args_obj,name).controller = self.Controller.CONST_VEL
                getattr(args_obj,name).timeout = timeout
                getattr(args_obj,name).modeOnTimeout = state_on_timeout

        fut = await self._proxy.move(args_obj)
        return fut

    async def move_wait(self):
        '''
        Wait for a motor to stop moving.

        Returns an asyncio.Future(). The result of the future is set when the
        motor has stopped moving, either by transitioning into a "COAST" state
        or "HOLD" state.
        '''
        await self._poll_state()
        fut = asyncio.Future()
        # If we are aready not moving, just return a completed future
        if not self.is_moving():
            fut.set_result(self.state)
        else:
            self._move_waiters.append(fut)
        return fut

class Motors:
    @classmethod
    async def create(cls, proxy):
        self = cls()
        self._proxy = proxy
        self.motors = []
        for i in range(3):
            self.motors.append( await Motor.create(i, proxy, self) )
        self._timeouts = _TimeoutCore(asyncio.get_event_loop())
        self._callback_handler = _EncoderEventHandler()
        return self

    def __getitem__(self, key):
        return self.motors[key]

    async def angles(self):
        fut = await self._proxy.getEncoderValues()
        user_fut = asyncio.Future()
        await self._timeouts.chain_futures(fut, user_fut, self.__angles)
        return user_fut

    def __angles(self, fut):
        results_obj = fut.result()
        results = ()
        for angle in results_obj.values:
            results += (_rad2deg(angle),)
        results += (results_obj.timestamp,)
        return results

    async def set_angles(self, angles, mask=0x07, relative=False, timeouts=None,
            states_on_timeout = None):
        angles = list(map(_deg2rad, angles))
        args_obj = self._proxy.rb_get_args_obj('move')
        names = ['motorOneGoal', 'motorTwoGoal', 'motorThreeGoal']
        if relative:
            move_type = Motor._MoveType.RELATIVE
        else:
            move_type = Motor._MoveType.ABSOLUTE
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

    async def stop(self, mask=0x07):
        fut = await self._proxy.stop(mask=mask)
        return fut

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
            self._motors = await Motors.create(self._proxy)
            self._accelerometer = await peripherals.Accelerometer.create(self._proxy)
            self._led = await peripherals.Led.create(self._proxy)
            self._button = await peripherals.Button.create(self._proxy)
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
    def motors(self):
        """
        The motors of the Linkbot.

        See :class:`linkbot.Motors` . To access individual motors, you may do:

            AsyncLinkbot.motors[0].is_moving()

        or similar. Also see :class:`linkbot.Motor`
        """
        return self._motors

    @property
    def accelerometer(self):
        """
        The Linkbot accelerometer.

        See :class:`linkbot.peripherals.Accelerometer`.
        """
        return self._accelerometer

    @property
    def button(self):
        """
        Access to the Linkbot's buttons. 

        See :class:`linkbot.peripherals.Button`.
        """
        return self._button

    @property
    def led(self):
        """
        The Linkbot multicolor LED.

        See :class:`linkbot.peripherals.Led`.
        """
        return self._led

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


