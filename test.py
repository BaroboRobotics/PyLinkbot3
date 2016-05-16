#!/usr/bin/env python3

import linkbot3 as linkbot
import logging
import asyncio
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
#async def bcast_handler(payload):
#    print(payload)

@asyncio.coroutine
def accel_handler(x, y, z, timestamp):
    print("Accel event: ", x, y, z, timestamp)

@asyncio.coroutine
def button_handler(button, down, timestamp):
    print('Button: ', button, down, timestamp)

@asyncio.coroutine
def task(serial_id):
    l = yield from linkbot.AsyncLinkbot.create(serial_id)

    fut = yield from l.motors.angles()
    angles = yield from fut
    print(angles)

    #fut = yield from l.motors.set_angles([90, 90, 90], 7, relative=True)
    #yield from fut
    fut = yield from l.motors[0].omega()
    omega = yield from fut
    print('Omega: ', omega )
    fut = yield from l.motors[0].accel()
    alpha = yield from fut
    print('AlphaI: ', alpha )

    fut = yield from l.accelerometer.values()
    values = yield from fut
    print('Accel: ', values)
    fut = yield from l.accelerometer.x()
    values = yield from  fut
    print('x: ', values)
    fut = yield from l.accelerometer.y()
    values = yield from fut
    print('y: ', values)
    fut = yield from l.accelerometer.z()
    values = yield from fut
    print('z: ', values)
    fut = yield from l.led.color()
    values = yield from fut
    print('led: ', values)
    fut = yield from l.led.set_color(255, 255, 0)
    yield from fut
    fut = yield from l.led.color()
    values = yield from fut
    print('led: ', values)
    fut = yield from l.button.values()
    values = yield from fut
    print('buttons: ', values)
    fut = yield from l.button.pwr()
    values = yield from fut
    print('PWR: ', values)
    fut = yield from l.button.a()
    values = yield from fut
    print('A: ', values)
    fut = yield from l.button.b()
    values = yield from fut
    print('B: ', values)

    yield from l.motors[0].set_accel(20)
    yield from l.motors[0].set_decel(20)
    yield from l.motors[0].set_controller(linkbot.Motor.Controller.SMOOTH)
    #yield from l.motors.set_angles([90, 90, 90], 7, relative=True)
    #yield from fut
    #fut = yield from l.motors[0].move_wait()
    #yield from fut
    #fut = yield from l.motors[0].move_accel(5, state_on_timeout=linkbot.Motor.State.HOLD)
    #yield from fut
    yield from l.motors[0].begin_move(timeout=5)
    fut = yield from l.motors[0].move_wait()
    yield from fut

    fut = yield from l.button.set_event_handler(button_handler)
    yield from fut
    print('Try pressing some buttons.')
    yield from asyncio.sleep(5)
    fut = yield from l.button.set_event_handler(None)
    yield from fut

    fut = yield from l.accelerometer.set_event_handler(accel_handler)
    yield from fut
    print('Accelerometer event handler activated')
    yield from asyncio.sleep(5)
    yield from l.accelerometer.set_event_handler(None)
    print('Accelerometer event handler deactivated')
    yield from asyncio.sleep(3)
    l.close()

loop = asyncio.get_event_loop()
loop.set_debug(True)
serial_id = input('Please enter robot serial ID:')
loop.run_until_complete(task(serial_id))
import time
time.sleep(3)
