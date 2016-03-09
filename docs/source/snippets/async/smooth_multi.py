import linkbot
import asyncio

robots = [ '2G7D',
           '5H57',
           '61K9',
           '8DCN',
           'M76F',
           'V6SJ',
           'GWVC',
           'F4CM',
           'QCSF',
           '25CB',
           'ZRPZ' ]

async def task(serial_id, motor_index=0):
    l = await linkbot.AsyncLinkbot.create(serial_id)
    accel = await l.motors[motor_index].accel()
    decel = await l.motors[motor_index].decel()
    print('Current accel, decel values: ', await accel, await decel)
    print('Setting to a slow value of 30 deg/s/s')
    fut = await l.motors[motor_index].set_accel(30)
    await fut
    fut = await l.motors[motor_index].set_decel(30)
    await fut
    fut = await l.motors[motor_index].set_omega(180)
    await fut
    print('Testing a series of smooth movements...')
    fut = await l.motors[motor_index].set_controller(linkbot.Motor.Controller.SMOOTH)
    await fut
    angle = 360

    for i in range(5):
        fut = await l.motors[motor_index].move(angle)
        await fut
        fut = await l.motors[motor_index].move_wait()
        await fut

        fut = await l.motors[motor_index].move(-angle)
        await fut
        fut = await l.motors[motor_index].move_wait()
        await fut

        angle /= 2

    print('Testing again with faster accel/decel of 120 deg/s/s')
    fut = await l.motors[motor_index].set_accel(120)
    await fut
    fut = await l.motors[motor_index].set_decel(120)
    await fut
    angle = 360

    for i in range(5):
        fut = await l.motors[motor_index].move(angle)
        await fut
        fut = await l.motors[motor_index].move_wait()
        await fut

        fut = await l.motors[motor_index].move(-angle)
        await fut
        fut = await l.motors[motor_index].move_wait()
        await fut

        angle /= 2


tasks = []

for r in robots:
    tasks.append( asyncio.ensure_future(task(r, 2)))

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

