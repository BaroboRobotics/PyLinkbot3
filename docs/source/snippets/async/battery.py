import linkbot
import asyncio
import time
import math

async def task(serial_id):
    l = await linkbot.AsyncLinkbot.create(serial_id)
    fut = await l.battery.voltage()
    print('Battery voltage is: ', await fut)

loop = asyncio.get_event_loop()
loop.run_until_complete(task('DGKR'))
loop.close()

