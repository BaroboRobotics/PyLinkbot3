#!/usr/bin/env python3

# Tested functions:

import asyncio
import linkbot
import math
import sys

def mag(xs):
    return math.sqrt(math.fsum(map(lambda x: x**2, xs)))

class AccelTest:
    def __init__(self):
        self._accel_count = 0

    async def accel_handler(self, x, y, z, timestamp):
        assert( (mag([x,y,z])-1.0) < 0.1 )
        assert( (z - 1.0) < 0.1 )
        self._accel_count += 1

async def task(serialid):
    a = AccelTest()
    l = await linkbot.AsyncLinkbot.create(serialid)
    fut = await l.accelerometer.set_event_handler(a.accel_handler, 0.01)
    await fut
    await l.motors[0].set_power(128)
    await asyncio.sleep(2)
    await l.motors.stop()
    fut = await l.accelerometer.set_event_handler()
    await fut
    print('Got {} accel events.'.format(a._accel_count))
    if a._accel_count > 15:
        return 0
    else:
        print('Test failed. Expected to get at least 15 accelerometer events.')
        return -1

if __name__ == '__main__':
    serialId = 'LOCL'
    if len(sys.argv) ==  2:
        serialId = sys.argv[1]

    loop = asyncio.get_event_loop()
    rc = loop.run_until_complete(task(serialId))
    sys.exit(rc)
