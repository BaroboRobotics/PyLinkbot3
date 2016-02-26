import asyncio
import linkbot._util as util

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


class Motors():
    def __init__(self, async_motors, loop):
        self._amotors = async_motors
        self._loop = loop

    def angles(self):
        return util.run_linkbot_coroutine(self._amotors.angles(), self._loop)

    def moveNB(self, angles, mask=0x07, relative=True, timeouts=None,
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
        return util.run_linkbot_coroutine(
                self._amotors.move(angles, mask, relative, timeouts, 
                    states_on_timeout),
                self._loop)

    def move(self, *args, **kwargs):
        self.moveNB(*args, **kwargs)
        if 'mask' in kwargs:
            self.move_wait(kwargs['mask'])
        else:
            self.move_wait()

    def move_wait(self, mask=0x07):
        return util.run_linkbot_coroutine(
                self._amotors.move_wait(mask=mask), self._loop)
