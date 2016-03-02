import asyncio
import functools
import linkbot._util as util

__all__ = [ 'Accelerometer', 
            'Battery', 
            'Button',
            'Motor', 
            'Motors']

class Accelerometer():
    def __init__(self, async_accelerometer, loop):
        self._proxy = async_accelerometer
        self._loop = loop

    def values(self):
        '''
        Get the current accelerometer values.

        :returns: The x, y, and z axis accelererations in units of standard
            Earth G's, as well as a timestamp in milliseconds from the robot.
        :rtype: (float, float, float, int)
        '''
        return util.run_linkbot_coroutine(
                self._proxy.values(),
                self._loop )

    def x(self):
        '''
        Get the current x axis value.

        :rtype: float
        :returns: The acceleration along the "X" axis in units of Earth
            gravitational units (a.k.a. G's)
        '''
        return util.run_linkbot_coroutine(
                self._proxy.x(),
                self._loop )

    def y(self):
        '''
        Get the current y axis value.

        :rtype: float
        :returns: The acceleration along the "Y" axis in units of Earth
            gravitational units (a.k.a. G's)
        '''
        return util.run_linkbot_coroutine(
                self._proxy.y(),
                self._loop )

    def z(self):
        '''
        Get the current y axis value.

        :rtype: float
        :returns: The acceleration along the "Z" axis in units of Earth
            gravitational units (a.k.a. G's)
        '''
        return util.run_linkbot_coroutine(
                self._proxy.z(),
                self._loop )

    def set_event_handler(self, callback=None, granularity=0.05):
        self.__event_handler = callback
        if callback:
            util.run_linkbot_coroutine(
                    self._proxy.set_event_handler(self.__event_cb, granularity),
                    self._loop)
        else:
            util.run_linkbot_coroutine(
                    self._proxy.set_event_handler(),
                    self._loop)

    async def __event_cb(self, *args, **kwargs):
        if asyncio.iscoroutinefunction(self.__event_handler):
            await self.__event_handler(*args, **kwargs)
        else:
            self.__event_handler(*args, **kwargs)

class Battery():
    def __init__(self, async_battery, loop):
        self._proxy = async_battery
        self._loop = loop

    def voltage(self):
        ''' Get the current battery voltage. 

        :returns: The battery voltage.
        :rtype: float
        '''
        return util.run_linkbot_coroutine(
                self._proxy.voltage(),
                self._loop )

class Button():
    PWR = 0
    A = 1
    B = 2

    UP = 0
    DOWN = 1

    def __init__(self, async_button, loop):
        self._proxy = async_button
        self._loop = loop

    def values(self):
        '''
        Get the current button values

        :rtype: Return type is (int, int, int), indicating the
            button state for the power, A, and B buttons, respectively. The button
            state is one of either Button.UP or Button.DOWN.
        '''
        return util.run_linkbot_coroutine(
                self._proxy.values(),
                self._loop)

    def pwr(self):
        '''
        Get the current state of the power button.

        :rtype: int
        :returns: either :const:`linkbot.peripherals.Button.UP` or
                  :const:`linkbot.peripherals.Button.DOWN`
        '''
        return util.run_linkbot_coroutine(
                self._proxy.pwr(),
                self._loop )

    def a(self):
        '''
        Get the current state of the 'A' button.

        :rtype: int
        :returns: either :const:`linkbot.peripherals.Button.UP` or
                  :const:`linkbot.peripherals.Button.DOWN`
        '''
        return util.run_linkbot_coroutine(
                self._proxy.a(),
                self._loop )

    def b(self):
        '''
        Get the current state of the 'B' button.

        :rtype: int
        :returns: either :const:`linkbot.peripherals.Button.UP` or
                  :const:`linkbot.peripherals.Button.DOWN`
        '''
        return util.run_linkbot_coroutine(
                self._proxy.b(),
                self._loop )

    def set_event_handler(self, callback=None):
        self.__event_handler = callback
        if callback:
            return util.run_linkbot_coroutine(
                    self._proxy.set_event_handler(self.__event_cb),
                    self._loop)
        else:
            return util.run_linkbot_coroutine(
                    self._proxy.set_event_handler(),
                    self._loop)

    async def __event_cb(self, *args, **kwargs):
        if asyncio.iscoroutinefunction(self.__event_handler):
            await self.__event_handler(*args, **kwargs)
        else:
            self.__event_handler(*args, **kwargs)

class Motor():
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

    def __init__(self, amotor, loop):
        self._amotor = amotor
        self._loop = loop

    def accel(self):
        ''' Get the acceleration setting of a motor

        :rtype: float
        :returns: The acceleration setting in units of deg/s/s
        '''
        return util.run_linkbot_coroutine(
                self._amotor.accel(), self._loop)

    def controller(self):
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
        return util.run_linkbot_coroutine(
                self._amotor.controller(), self._loop)

    def decel(self):
        ''' Get the deceleration setting of a motor

        :rtype: float
        :returns: The deceleration setting in units of deg/s/s
        '''
        return util.run_linkbot_coroutine(
                self._amotor.decel(), self._loop)

    def omega(self):
        ''' Get the rotational velocity setting of a motor

        :rtype: float
        :returns: The speed setting of the motor in deg/s
        '''
        return util.run_linkbot_coroutine(
                self._amotor.omega(), self._loop)

    def set_accel(self, value):
        ''' Set the acceleration of a motor.
        
        See :func:`linkbot.peripherals.Motor.accel`
        '''
        return util.run_linkbot_coroutine(
                self._amotor.set_accel(value), self._loop)
    
    def set_controller(self, value):
        ''' Set the motor controller.

        See :func:`linkbot.peripherals.Motor.controller`
        '''
        return util.run_linkbot_coroutine(
                self._amotor.set_controller(value), self._loop)

    def set_decel(self, value):
        ''' Set the motor deceleration.

        See :func:`linkbot.peripherals.Motor.decel`
        '''
        return util.run_linkbot_coroutine(
                self._amotor.set_decel(value), self._loop)

    def set_omega(self, value):
        ''' Set the motor's velocity.

        See :func:`linkbot.peripherals.Motor.omega`
        '''
        return util.run_linkbot_coroutine(
                self._amotor.set_omega(value), self._loop)

    def set_event_handler(self, callback=None, granularity=2.0):
        self.__event_handler = callback
        if callback:
            return util.run_linkbot_coroutine(
                    self._amotor.set_event_handler(self.__event_cb, granularity),
                    self._loop)
        else:
            return util.run_linkbot_coroutine(
                    self._amotor.set_event_handler(),
                    self._loop)

    async def __event_cb(self, angle, timestamp):
        if asyncio.iscoroutinefunction(self.__event_handler):
            await self.__event_handler(angle, timestamp)
        else:
            self.__event_handler(angle, timestamp)

    def set_power(self, power):
        '''
        Set the motor's power.

        :type power: int [-255,255]
        '''
        return util.run_linkbot_coroutine(
                self.amotor.set_power(power),
                self._loop)

    def begin_accel(self, timeout, v0 = 0.0,
            state_on_timeout=State.COAST):
        ''' Cause a motor to begin accelerating indefinitely. 

        The joint will begin accelerating at the acceleration specified
        previously by :func:`linkbot.peripherals.Motor.accel`. If a 
        timeout is specified, the motor will transition states after the timeout
        expires. The state the motor transitions to is specified by the
        parameter ```state_on_timeout```. 

        If the robot reaches its maximum speed, specified by the function
        :func:`linkbot.peripherals.Motor.set_omega`, it will stop
        accelerating and continue at that speed until the timeout, if any,
        expires.

        :param timeout: Seconds to wait before robot transitions states.
        :type timeout: float
        :param v0: Initial velocity in deg/s
        :type v0: float
        :param state_on_timeout: End state after timeout
        :type state_on_timeout: :class:`linkbot.peripherals.Motor.State`
        '''
        return util.run_linkbot_coroutine(
                self.amotor.begin_accel(timeout, v0, state_on_timeout),
                self._loop)

    def begin_move(self, timeout = 0, forward=True,
            state_on_timeout=State.COAST):
        ''' Begin moving motor at constant velocity

        The joint will begin moving at a constant velocity previously set by
        :func:`linkbot.peripherals.Motor.set_omega`. 

        :param timeout: After ```timeout``` seconds, the motor will transition
            states to the state specified by the parameter
            ```state_on_timeout```.
        :type timeout: float
        :param forward: Whether to move the joint in the positive direction
            (True) or negative direction (False).
        :type forward: bool
        :param state_on_timeout: State to transition to after the motion
            times out.
        :type state_on_timeout: :class:`linkbot.peripherals.Motor.State`
        '''
        return util.run_linkbot_coroutine(
                self.amotor.begin_move(timeout, forward, state_on_timeout),
                self._loop)

    def move(self, angle, relative=True, wait=True):
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
        :param wait: Indicate whether the function should wait for the movement
            to finish before returning or not. For example, the following two
            snippets of code yield identical robot behavior::

                my_linkbot.motors[0].move(90, wait=True)

            and::

                my_linkbot.motors[0].move(90, wait=False)
                my_linkbot.motors[0].move_wait()

        :type wait: bool
        '''
        util.run_linkbot_coroutine(
                self.amotor.move(angle, relative),
                self._loop)
        if wait:
            self.move_wait()

    def move_wait(self):
        ''' Wait for the motor to stop moving.

        This function blocks until the motor is either in a ```COAST``` state or
        ```HOLD``` state.
        '''
        return util.run_linkbot_coroutine(
                self.amotor.move_wait(),
                self._loop)

class Motors():
    def __init__(self, async_motors, loop):
        self._amotors = async_motors
        self._loop = loop
        self.motors = []
        for i in range(3):
            self.motors.append( Motor(self._amotors[i], self._loop) )

    def __getitem__(self, index):
        return self.motors[index]

    def __len__(self):
        return 3

    def angles(self):
        ''' Get the current joint angles and a timestamp from the robot.

        :returns: (a1, a2, a3, timestamp) where the three angles are in degrees
            and the timestamp is an integer representing the number of
            milliseconds the Linkbot has been online when this function was
            executed.
        :rtype: (float, float, float, int)
        '''
        return util.run_linkbot_coroutine(self._amotors.angles(), self._loop)

    def move(self, angles, mask=0x07, relative=True, timeouts=None,
            states_on_timeout = None, wait=True):
        ''' Move a Linkbot's joints. 

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
        :param wait: Indicate whether this function should return when the
                motion starts or when the motion finishes. If this is set to
                ```True```, this function will block until the motion completely
                finishes. If set to ```False```, this function will return
                immediately after receiving confirmation from the robot that the
                joint has begun moving.
        '''
        util.run_linkbot_coroutine(
                self._amotors.move(angles, mask, relative, timeouts, 
                    states_on_timeout),
                self._loop)

        if wait:
            self.move_wait(mask)

    def move_wait(self, mask=0x07):
        ''' Wait for motors to stop moving.

        This function returns when the Linkbot's motors stop moving. The
        ``mask`` argument is similar to the ``mask`` argument in 
        :func:`linkbot.peripherals.Motors.moveNB`.
        '''
        return util.run_linkbot_coroutine(
                self._amotors.move_wait(mask=mask), self._loop)

    def stop(self, mask=0x07):
        ''' Immediately stop all motors.

        :param mask: See :func:`linkbot.peripherals.Motors.moveNB`
        '''
        return util.run_linkbot_coroutine(
                self._amotors.stop(mask=mask), self._loop)
