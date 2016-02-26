import linkbot
import asyncio

async def task():
    l = await linkbot.AsyncLinkbot.create('DGKR')
    fut = await l.accelerometer.values()
    print('Accelerometer values are: ', await fut)

loop = asyncio.get_event_loop()
loop.run_until_complete(task())
loop.close()

