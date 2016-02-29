import asyncio
import linkbot._util as util

__all__ = ['Motor', 'Motors']

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
        return util.run_linkbot_coroutine(
                self._amotor.set_event_handler(callback, granularity),
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

    def angles(self):
        ''' Get the current joint angles and a timestamp from the robot.

        :returns: (a1, a2, a3, timestamp) where the three angles are in degrees
            and the timestamp is an integer representing the number of
            milliseconds the Linkbot has been online when this function was
            executed.
        :rtype: (float, float, float, int)
        '''
        return util.run_linkbot_coroutine(self._amotors.angles(), self._loop)

    def moveNB(self, angles, mask=0x07, relative=True, timeouts=None,
            states_on_timeout = None):
        ''' Move a Linkbot's joints. 

        This function returns as soon as it receives confirmation from the robot
        that the joints have begun moving. Use
        :func:`linkbot.peripherals.Motors.move_wait` or the non "NB" version of
        this function to wait for the motors to finish moving.

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
        return util.run_linkbot_coroutine(
                self._amotors.move(angles, mask, relative, timeouts, 
                    states_on_timeout),
                self._loop)

    def move(self, *args, **kwargs):
        ''' Move a Linkbot's joints.

        This function takes the same arguments as
        :func:`linkbot.peripherals.Motors.moveNB` . However, this function only
        returns after the movement has finished. For example, the following two
        code examples result in identical robot behavior::

            robot = linkbot.Linkbot('ABCD')
            robot.motors.moveNB([90, 0, 90])
            robot.motors.move_wait()

        and::
         
            robot = linkbot.Linkbot('ABCD')
            robot.motors.move([90, 0, 90])

        '''
            
        self.moveNB(*args, **kwargs)
        if 'mask' in kwargs:
            self.move_wait(kwargs['mask'])
        else:
            self.move_wait()

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
