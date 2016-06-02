import linkbot3 as linkbot
import asyncio
import time
import math

async def task(serial_id):
    l = await linkbot.AsyncLinkbot.create(serial_id)
    fut = await l.led.color()
    print('Current led color: ', await fut)
    print('Morphing LED colors for 10 seconds...')
    start_time = time.time()
    while time.time()-start_time < 10:
        red = 128+128*math.sin(time.time())
        green = 128+128*math.sin(time.time() + 2*math.pi/3)
        blue = 128+128*math.sin(time.time() + 4*math.pi/3)
        print('Setting color to: ', red, green, blue)
        fut = await l.led.set_color(int(red), int(green), int(blue))
        await fut


loop = asyncio.get_event_loop()
loop.run_until_complete(task('7944'))
loop.close()

