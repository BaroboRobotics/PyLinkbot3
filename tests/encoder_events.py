#!/usr/bin/env python3

import asyncio
import linkbot
import math
import sys
async def m1(degrees, timestamp):
    print('m1: ', degrees, timestamp)

async def m3(degrees, timestamp):
    print('m3: ', degrees, timestamp)

async def task(serialid):
    l = await linkbot.AsyncLinkbot.create(serialid)
    # Enable encoder events for motor 1
    await l.motors[0].set_event_handler(m1)
    fut = await l.motors.set_angles([90, 90, 90], relative=True)
    await fut
    fut = await l.motors[0].move_wait()
    await fut
    # Enable encoder events for motor 3
    print('M3 encoder events enabled.')
    await asyncio.sleep(2)
    await l.motors[2].set_event_handler(m3)
    await l.motors.set_angles([90, 90, 90], relative=True)
    fut = await l.motors[2].move_wait()
    await fut
    # Enable encoder events for motor 3
    print('M1 encoder events disabled.')
    await asyncio.sleep(2)
    await l.motors[0].set_event_handler(None)
    await l.motors.set_angles([90, 90, 90], relative=True)
    fut = await l.motors[0].move_wait()
    await fut

    # Enable encoder events for motor 3
    print('M3 encoder events disabled.')
    await asyncio.sleep(2)
    await l.motors[2].set_event_handler(None)
    await l.motors.set_angles([90, 90, 90], relative=True)
    fut = await l.motors[0].move_wait()
    await fut

if __name__ == '__main__':
    serialId = 'LOCL'
    if len(sys.argv) ==  2:
        serialId = sys.argv[1]

    loop = asyncio.get_event_loop()
    rc = loop.run_until_complete(task(serialId))
    sys.exit(rc)
