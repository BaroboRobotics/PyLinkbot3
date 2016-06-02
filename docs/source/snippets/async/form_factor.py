import linkbot3 as linkbot
import asyncio
import time
import math

async def task(serial_id):
    l = await linkbot.AsyncLinkbot.create(serial_id)
    fut = await l.form_factor()
    print('The form factor is: ', await fut)

loop = asyncio.get_event_loop()
loop.run_until_complete(task('7944'))
loop.close()

