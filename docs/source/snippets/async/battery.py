import linkbot3 as linkbot
import asyncio
import time
import math

async def task(serial_id):
    l = await linkbot.AsyncLinkbot.create(serial_id)
    fut = await l.battery.voltage()
    print('Battery voltage is: ', await fut)
    fut = await l.battery.percentage()
    print('Battery percentage: ', await fut)
    await l.disconnect()

loop = asyncio.get_event_loop()
loop.run_until_complete(task('7944'))
loop.close()

