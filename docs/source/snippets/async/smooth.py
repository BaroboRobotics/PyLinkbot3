import linkbot3 as linkbot
import asyncio

async def task(serial_id):
    l = await linkbot.AsyncLinkbot.create(serial_id)
    accel = await l.motors[0].accel()
    decel = await l.motors[0].decel()
    print('Current accel, decel values: ', await accel, await decel)
    print('Setting to a slow value of 30 deg/s/s')
    fut = await l.motors[0].set_accel(30)
    await fut
    fut = await l.motors[0].set_decel(30)
    await fut
    fut = await l.motors[0].set_omega(180)
    await fut
    print('Testing a series of smooth movements...')
    fut = await l.motors[0].set_controller(linkbot.Motor.Controller.SMOOTH)
    await fut
    angle = 360

    for i in range(5):
        fut = await l.motors[0].move(angle)
        await fut
        fut = await l.motors[0].move_wait()
        await fut

        fut = await l.motors[0].move(-angle)
        await fut
        fut = await l.motors[0].move_wait()
        await fut

        angle /= 2

    print('Testing again with faster accel/decel of 120 deg/s/s')
    fut = await l.motors[0].set_accel(120)
    await fut
    fut = await l.motors[0].set_decel(120)
    await fut
    angle = 360

    for i in range(5):
        fut = await l.motors[0].move(angle)
        await fut
        fut = await l.motors[0].move_wait()
        await fut

        fut = await l.motors[0].move(-angle)
        await fut
        fut = await l.motors[0].move_wait()
        await fut

        angle /= 2


loop = asyncio.get_event_loop()
loop.run_until_complete(task('DGKR'))
loop.close()

