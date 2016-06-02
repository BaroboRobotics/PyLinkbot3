import linkbot3 as linkbot
import asyncio
import time
import math

async def task(serial_id):
    l = await linkbot.AsyncLinkbot.create(serial_id)

    print('Playing buzzer siren for 5 seconds...')
    start_time = time.time()
    while time.time()-start_time < 5:
        freq = 440 + 110*math.sin(2*time.time())
        fut = await l.buzzer.set_frequency(freq)
        await fut

    fut = await l.buzzer.set_frequency(0)
    await fut

loop = asyncio.get_event_loop()
loop.run_until_complete(task('7944'))
loop.close()

