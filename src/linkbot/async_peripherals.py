import asyncio
import functools
import linkbot
import linkbot._util as util
import linkbot.peripherals as peripherals
import weakref

class Accelerometer():
    @classmethod
    async def create(cls, proxy):
        self = cls()
        self._proxy = proxy
        self._event_callback = None
        return self

    async def values(self):
        '''
        Get the current accelerometer values.

        :rtype: asyncio.Future . The future's result type is (float, float,
            float) representing the x, y, and z axes, respectively. The 
            units of each value are in Earth gravitational units (a.k.a. G's).
        '''
        fut = await self._proxy.getAccelerometerData()
        user_fut = asyncio.Future()
        fut.add_done_callback(
                functools.partial(
                    self.__values,
                    user_fut )
                )
        return user_fut

    def __values(self, user_fut, fut):
        user_fut.set_result(
                ( fut.result().x, fut.result().y, fut.result().z )
                )

    async def x(self):
        '''
        Get the current x axis value.

        :rtype: asyncio.Future. The future's result type is "float", in units of
            Earth gravitational units (a.k.a. G's)
        '''
        fut = await self.values()
        user_fut = asyncio.Future()
        fut.add_done_callback(
                functools.partial(
                    self.__get_index,
                    0,
                    user_fut )
                )
        return user_fut

    async def y(self):
        '''
        Get the current y axis value.

        :rtype: asyncio.Future. The future's result type is "float", in units of
            Earth gravitational units (a.k.a. G's)
        '''
        fut = await self.values()
        user_fut = asyncio.Future()
        fut.add_done_callback(
                functools.partial(
                    self.__get_index,
                    1,
                    user_fut )
                )
        return user_fut

    async def z(self):
        '''
        Get the current z axis value.

        :rtype: asyncio.Future. The future's result type is "float", in units of
            Earth gravitational units (a.k.a. G's)
        '''
        fut = await self.values()
        user_fut = asyncio.Future()
        fut.add_done_callback(
                functools.partial(
                    self.__get_index,
                    2,
                    user_fut )
                )
        return user_fut

    def __get_index(self, index, user_fut, fut):
        user_fut.set_result( fut.result()[index] )

    async def set_event_handler(self, callback=None, granularity=0.05):
        '''
        Set a callback function to be executed when the accelerometer
        values on the robot change.

        :param callback: async func(x, y, z, timestamp) -> None
        :param granularity: float . The callback will only be called when any
            axis of the accelerometer changes by this many G's of acceleration.
        '''
        if not callback:
            # Remove the event
            try:
                fut = await self._proxy.enableAccelerometerEvent(
                        enable=False,
                        granularity=granularity)
                await fut
                self._proxy.rb_remove_broadcast_handler('accelerometerEvent')
                self._event_callback = callback
                return fut
            except KeyError:
                # Don't worry if the bcast handler is not there.
                pass

        else:
            self._event_callback = callback
            self._proxy.rb_add_broadcast_handler( 'accelerometerEvent', 
                                                  self.__event_handler )
            return await self._proxy.enableAccelerometerEvent(
                    enable=True,
                    granularity=granularity )

    async def __event_handler(self, payload):
        await self._event_callback( payload.x, 
                                    payload.y, 
                                    payload.z, 
                                    payload.timestamp)

class Button():
    PWR = 0
    A = 1
    B = 2

    UP = 0
    DOWN = 1

    @classmethod
    async def create(cls, proxy):
        self = cls()
        self._proxy = proxy
        self._event_callback = None
        return self

    async def values(self):
        '''
        Get the current button values

        :rtype: asyncio.Future . Result type is (int, int, int), indicating the
            button state for the power, A, and B buttons, respectively. The button
            state is one of either Button.UP or Button.DOWN.
        '''
        fut = await self._proxy.getButtonState()
        user_fut = asyncio.Future()
        fut.add_done_callback(
                functools.partial(
                    self.__values,
                    user_fut
                    )
                )
        return user_fut

    def __values(self, user_fut, fut):
        pwr = fut.result().mask & 0x01
        a = (fut.result().mask>>1) & 0x01
        b = (fut.result().mask>>2) & 0x01
        user_fut.set_result( (pwr, a, b) )

    async def pwr(self):
        '''
        Get the current state of the power button.

        :rtype: either Button.UP or Button.DOWN
        '''
        fut = await self._proxy.getButtonState()
        user_fut = asyncio.Future()
        fut.add_done_callback(
                functools.partial(
                    self.__button_values,
                    0,
                    user_fut
                    )
                )
        return user_fut

    async def a(self):
        '''
        Get the current state of the 'A' button.

        :rtype: either Button.UP or Button.DOWN
        '''
        fut = await self._proxy.getButtonState()
        user_fut = asyncio.Future()
        fut.add_done_callback(
                functools.partial(
                    self.__button_values,
                    1,
                    user_fut
                    )
                )
        return user_fut

    async def b(self):
        '''
        Get the current state of the 'B' button.

        :rtype: either Button.UP or Button.DOWN
        '''
        fut = await self._proxy.getButtonState()
        user_fut = asyncio.Future()
        fut.add_done_callback(
                functools.partial(
                    self.__button_values,
                    2,
                    user_fut
                    )
                )
        return user_fut

    def __button_values(self, index, user_fut, fut):
        user_fut.set_result((fut.result().mask>>index) & 0x01)

    async def set_event_handler(self, callback=None):
        '''
        Set a callback function to be executed when there is a button press or
        release.

        :param callback: func(buttonNo(int), buttonDown(bool), timestamp) -> None
        '''
        self._event_callback = callback
        if not callback:
            # Remove the event
            try:
                fut = await self._proxy.enableButtonEvent(
                        enable=False)
                await fut
                self._proxy.rb_remove_broadcast_handler('buttonEvent')
                return fut
            except KeyError:
                # Don't worry if the bcast handler is  not there.
                pass

        else:
            self._proxy.rb_add_broadcast_handler( 'buttonEvent', 
                                                  self.__event_handler )
            return await self._proxy.enableButtonEvent(
                    enable=True)

    async def __event_handler(self, payload):
        await self._event_callback( payload.button, 
                                    payload.state, 
                                    payload.timestamp)

class Led():
    @classmethod
    async def create(cls, proxy):
        self = cls()
        self._proxy = proxy
        return self

    async def color(self):
        '''
        Get the current LED color.

        :rtype: (int, int, int) indicating the intensity of the red, green,
            and blue channels. Each intensity is a value between [0,255].
        '''
        fut = await self._proxy.getLedColor()
        user_fut = asyncio.Future()
        fut.add_done_callback(
                functools.partial(
                    self.__color,
                    user_fut
                    )
                )
        return user_fut
        
    def __color(self, user_fut, fut):
        word = fut.result().value
        r = (word&0xff0000) >> 16
        g = (word&0x00ff00) >> 8
        b = word&0x0000ff
        user_fut.set_result( (r,g,b) )

    async def set_color(self, r, g, b):
        '''
        Set the current LED color.

        :type r: int [0,255]
        :type g: int [0,255]
        :type b: int [0,255]
        '''
        word = b | (g<<8) | (r<<16)
        fut = await self._proxy.setLedColor(value=word)
        return fut

class Buzzer():
    @classmethod
    async def create(cls, proxy):
        self = cls()
        self._proxy = proxy
        return self

    async def frequency(self):
        '''
        Get the current buzzer frequency.

        :returns: Frequency in Hz
        :rtype: float
        '''
        fut = await self._proxy.getBuzzerFrequency()
        return fut

    async def set_frequency(self, hz):
        '''
        Set the buzzer frequency.

        :param hz: A frequency in Hz.
        :type hz: float
        '''
        fut = await self._proxy.setBuzzerFrequency(value=hz)
        return fut

class Motor:
    '''
    The asynchronous representation of a Linkbot's motor.

    See also :class:`linkbot.peripherals.Motor` for the synchronous counterpart.
    '''
    @classmethod
    async def create(cls, index, proxy, motors_obj):
        self = cls()
        self._controller = peripherals.Motor.Controller.CONST_VEL
        self._index = index
        self._proxy = proxy
        self._state = peripherals.Motor.State.COAST
        await self._poll_state()
        # List of futures that should be set when this joint is done moving
        self._move_waiters = []
        #self._motors = weakref.ref(motors_obj)
        self._motors = motors_obj
        return self

    async def accel(self):
        ''' Get the acceleration setting of a motor

        :rtype: float
        :returns: The acceleration setting in units of deg/s/s
        '''
        return await self.__get_motor_controller_attribute(
                'getMotorControllerAlphaI',
                conv=util.rad2deg
                )

    async def controller(self):
        '''The movement controller.

        This property controls the strategy with which the motors are moved.
        Legal values are:

        * :const:`linkbot.peripherals.Motor.Controller.PID`: Move the motors directly with the
          internal PID controller. This is typically the fastest way to get a
          motor from one position to another. The motor may experience some
          overshoot and underdamped response when moving larger distances.
        * :const:`linkbot.peripherals.Motor.Controller.CONST_VEL`: Move the motor at a constant
          velocity. This motor controller attemts to accelerate and decelerate
          a motor infinitely fast to and from a constant velocity to move the
          motor from one position to the next. The velocity can be controlled
          by setting the property `omega`.
        * :const:`linkbot.peripherals.Motor.Controller.SMOOTH`: Move the motor with specified
          acceleration, maximum velocity, and deceleration. For this type of
          movement, access maximum velocity with property `omega`,
          acceleration with property `acceleration`, and deceleration with property
          `deceleration`.
        '''
        fut = asyncio.Future()
        fut.set_result(self._controller)
        return fut

    async def decel(self):
        ''' Get the deceleration setting of a motor

        :rtype: float
        :returns: The deceleration setting in units of deg/s/s
        '''
        return await self.__get_motor_controller_attribute(
                'getMotorControllerAlphaF',
                conv=util.rad2deg
                )

    async def omega(self):
        ''' Get the rotational velocity setting of a motor

        :rtype: float
        :returns: The speed setting of the motor in deg/s
        '''
        return await self.__get_motor_controller_attribute(
                'getMotorControllerOmega',
                conv=util.rad2deg
                )

    async def _poll_state(self):
        if (self._index == 1) and (self._proxy.form_factor == linkbot.FormFactor.I):
            self._state = peripherals.Motor.State.COAST
        elif (self._index == 2) and (self._proxy.form_factor == linkbot.FormFactor.L):
            self._state = peripherals.Motor.State.COAST
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
        if fut.cancelled():
            user_fut.cancel()
            return
        results_obj = fut.result()
        values = []
        for v in results_obj.values:
            values.append(conv(v))
        if self._proxy.form_factor == linkbot.FormFactor.I:
            values.append(0.0)
        elif self._proxy.form_factor == linkbot.FormFactor.L:
            values.insert(1, 0.0)
        user_fut.set_result(values[self._index])

    async def set_accel(self, value):
        ''' Set the acceleration of a motor.
        
        See :func:`linkbot.async_peripherals.Motor.accel`
        '''
        return await self.__set_motor_controller_attribute(
                'setMotorControllerAlphaI',
                util.deg2rad(value)
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
                util.deg2rad(value)
                )

    async def set_omega(self, value):
        # See :func:`omega`
        return await self.__set_motor_controller_attribute(
                'setMotorControllerOmega',
                util.deg2rad(value)
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
                getattr(args, name).granularity = util.deg2rad(granularty)
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
            getattr(args, name).granularity = util.deg2rad(granularity)
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
        getattr(args_obj,name).controller = peripherals.Motor.Controller.PID

        fut = await self._proxy.move(args_obj)
        return fut

    def __handle_set_attribute(self, user_fut, fut):
        user_fut.set_result( fut.result() )

    def is_moving(self):
        if self._state in [peripherals.Motor.State.COAST, 
                           peripherals.Motor.State.HOLD]:
            return False
        else:
            return True

    @property
    def state(self):
        # The current joint state. One of :class:`Motor.State`
        return self._state
    @state.setter
    def state(self, value):
        assert(value in peripherals.Motor.State.__dict__.values())
        self._state = value
        if not self.is_moving():
            for fut in self._move_waiters:
                fut.set_result(self._state)
            self._move_waiters.clear()

    async def begin_accel(self, timeout, v0 = 0.0,
            state_on_timeout=peripherals.Motor.State.COAST):
        mask = 1<<self._index
        args_obj = self._proxy.rb_get_args_obj('move')
        names = ['motorOneGoal', 'motorTwoGoal', 'motorThreeGoal']
        for i,name in enumerate(names):
            if mask&(1<<i):
                getattr(args_obj,name).type = self._MoveType.INFINITE
                getattr(args_obj,name).goal = v0
                getattr(args_obj,name).controller = peripherals.Motor.Controller.ACCEL
                getattr(args_obj,name).timeout = timeout
                getattr(args_obj,name).modeOnTimeout = state_on_timeout

        fut = await self._proxy.move(args_obj)
        return fut

    async def begin_move(self, timeout = 0, forward=True,
            state_on_timeout=peripherals.Motor.State.COAST):
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
                getattr(args_obj,name).controller = peripherals.Motor.Controller.CONST_VEL
                getattr(args_obj,name).timeout = timeout
                getattr(args_obj,name).modeOnTimeout = state_on_timeout

        fut = await self._proxy.move(args_obj)
        return fut

    async def move(self, angle, relative=True):
        ''' Move the motor.

        :param angle: The angle to move the motor.
        :type angle: float
        :param relative: Determines if the motor should move to an absolute
            position or perform a relative motion. For instance, if the motor is
            currently at a position of 45 degrees, performing a relative move of
            90 degrees will move the motor to 135 degrees, while doing an
            absolute move of 90 degrees will move the motor forward by 45
            degrees until it reaches the absolute position of 90 degrees.
        :type relative: bool
        '''
        self._motors.move(
                [angle, angle, angle],
                mask=1<<self._index,
                relative=relative)

    async def move_wait(self):
        '''
        Wait for a motor to stop moving.

        Returns an asyncio.Future(). The result of the future is set when the
        motor has stopped moving, either by transitioning into a "COAST" state
        or "HOLD" state.
        '''
        await self._poll_state()
        fut = asyncio.Future()
        user_fut = asyncio.Future()
        # If we are aready not moving, just return a completed future
        if not self.is_moving():
            user_fut.set_result(self.state)
        else:
            self._move_waiters.append(fut)
            poll_fut = asyncio.ensure_future(self.__poll_movewait())
            fut = asyncio.gather(poll_fut, fut)
            util.chain_futures(fut, user_fut, conv=lambda x: None)
        return user_fut

    async def __poll_movewait(self):
        '''
        This internal function is used to poll the state of the motors as long
        as there is a future waiting on :func:`linkbot.Motor.move_wait`. 
        '''
        while self._move_waiters:
            fut = self._move_waiters[0]
            try:
                await asyncio.wait_for(asyncio.shield(fut), 2)
            except asyncio.TimeoutError:
                await self._poll_state()
            else:
                continue

class Motors:
    ''' The Motors class.

    This class represents all of the motors on-board a Linkbot. To access an
    individual motor, this class may be indexed. For instance, the line::

        linkbot.motors[0] 

    accesses the first motor on a Linkbot.
    '''

    class _EncoderEventHandler():
        def __init__(self):
            self._handlers = [None, None, None]

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

    @classmethod
    async def create(cls, proxy):
        self = cls()
        self._proxy = proxy
        self.motors = []
        for i in range(3):
            self.motors.append( await Motor.create(i, proxy, self) )
        self._timeouts = linkbot._TimeoutCore(asyncio.get_event_loop())
        self._callback_handler = self._EncoderEventHandler()
        return self

    def __getitem__(self, key):
        return self.motors[key]

    async def angles(self):
        ''' Get the current joint angles.

        :returns: (angle1, angle2, angle3, timestamp) . These are the three
            robot joint angles and a timestamp from the robot which is the
            number of milliseconds the robot has been on.
        :rtype: (float, float, float, int)
        '''

        fut = await self._proxy.getEncoderValues()
        user_fut = asyncio.Future()
        await self._timeouts.chain_futures(fut, user_fut, self.__angles)
        return user_fut

    def __angles(self, fut):
        results_obj = fut.result()
        results = ()
        for angle in results_obj.values:
            results += (util.rad2deg(angle),)
        results += (results_obj.timestamp,)
        return results

    async def move(self, angles, mask=0x07, relative=True, timeouts=None,
            states_on_timeout = None):
        ''' Move a Linkbot's joints

        :param angles: A list of angles in degrees
        :type angles: [float, float, float]
        :param mask: Which joints to actually move. Valid values are:

            * 1: joint 1
            * 2: joint 2
            * 3: joints 1 and 2
            * 4: joint 3
            * 5: joints 1 and 3
            * 6: joints 2 and 3
            * 7: all 3 joints
            
        :param relative: This flag controls whether to move a relative distance
            from the motor's current position or to an absolute position.
        :type relative: bool
        :param timeouts: Sets timeouts for each motor's movement, in seconds. If
            the timeout expires while the motor is in motion, the motor will
            transition to the motor state specified by the ``states_on_timeout``
            parameter.
        :type timeouts: [float, float, float]
        :type states_on_timeout: [ linkbot.peripherals.Motor.State,
                                   linkbot.peripherals.Motor.State,
                                   linkbot.peripherals.Motor.State ]
        '''
        angles = list(map(util.deg2rad, angles))
        args_obj = self._proxy.rb_get_args_obj('move')
        names = ['motorOneGoal', 'motorTwoGoal', 'motorThreeGoal']
        if relative:
            move_type = peripherals.Motor._MoveType.RELATIVE
        else:
            move_type = peripherals.Motor._MoveType.ABSOLUTE
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

    async def move_wait(self, mask=0x07):
        futs = []
        for i in range(3):
            if mask & (1<<i):
                futs.append( await self.motors[i].move_wait() )
        user_fut = asyncio.Future()
        fut = asyncio.gather(*tuple(futs))
        util.chain_futures(fut, user_fut, conv=lambda x: None)
        return user_fut

    async def stop(self, mask=0x07):
        ''' Immediately stop all motors.

        :param mask: See :func:`linkbot.async_peripherals.Motors.move`
        '''
        fut = await self._proxy.stop(mask=mask)
        return fut

