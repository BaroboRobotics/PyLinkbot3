#!/usr/bin/env python3

import linkbot 
import logging
import asyncio
#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
async def bcast_handler(payload):
    print(payload)

async def task():
    l = await linkbot.AsyncLinkbot.create('LOCL')

    fut = await l.motors.angles()
    print(await fut)

    #fut = await l.motors.set_angles([90, 90, 90], 7, relative=True)
    #await fut
    fut = await l.motors[0].omega()
    print('Omega: ', await fut)
    fut = await l.motors[0].accel()
    print('AlphaI: ', await fut)

    fut = await l.accelerometer.values()
    print('Accel: ', await fut)
    fut = await l.accelerometer.x()
    print('x: ', await fut)
    fut = await l.accelerometer.y()
    print('y: ', await fut)
    fut = await l.accelerometer.z()
    print('z: ', await fut)
    fut = await l.led.color()
    print('led: ', await fut)
    fut = await l.led.set_color(255, 255, 0)
    await fut
    fut = await l.led.color()
    print('led: ', await fut)

    await l.motors[0].set_accel(20)
    await l.motors[0].set_decel(20)
    await l.motors[0].set_controller(linkbot.Motor.Controller.SMOOTH)
    #await l.motors.set_angles([90, 90, 90], 7, relative=True)
    #await fut
    #fut = await l.motors[0].move_wait()
    #await fut
    #fut = await l.motors[0].move_accel(5, state_on_timeout=linkbot.Motor.State.HOLD)
    #await fut
    await l.motors[0].begin_move(timeout=5)
    fut = await l.motors[0].move_wait()
    await fut

    l.rb_add_broadcast_handler('buttonEvent', bcast_handler)
    fut = await l.enableButtonEvent(enable=True)
    await fut
    print('Try pressing some buttons.')
    await asyncio.sleep(5)
    l.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(task())
import time
time.sleep(3)
