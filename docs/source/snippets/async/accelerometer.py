import linkbot
import asyncio

async def cb(*args):
    print(args)

async def task(serial_id):
    l = await linkbot.AsyncLinkbot.create(serial_id)
    r_fut = await l.accelerometer.values()
    print('Current accel values: ', await r_fut)

    r_fut = await l.accelerometer.x()
    print('Current X axis value: ', await r_fut)
    r_fut = await l.accelerometer.y()
    print('Current y axis value: ', await r_fut)
    r_fut = await l.accelerometer.z()
    print('Current z axis value: ', await r_fut)

    print('Enabling accelerometer events for 5 seconds...')
    await l.accelerometer.set_event_handler(cb)
    await asyncio.sleep(5)
    print('Done.')

loop = asyncio.get_event_loop()
loop.run_until_complete(task('DGKR'))
loop.close()

