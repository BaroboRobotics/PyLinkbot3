#!/usr/bin/env python3

# Tested functions:

import asyncio
import linkbot
import sys
import random

async def task(serialid, queue):

    def done(fut):
        print(serialid)

    l = await linkbot.AsyncLinkbot.create(serialid)

    for i in range(100):
        print('ping: ', i)
        #fut = await l.motors.angles() 
        fut = await l.led.set_color(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255))
        fut.add_done_callback(done)
        await queue.put(fut)

async def consumer(queue):
    while True:
        fut = await queue.get()
        print(queue.qsize())
        await fut

if __name__ == '__main__':
    q = asyncio.Queue(maxsize=6)
    serialId = 'LOCL'
    if len(sys.argv) ==  2:
        serialId = sys.argv[1]

    loop = asyncio.get_event_loop()
    linkbots = [ 'ZVT7',
                 'DGKR',
                 'X9Q5',
                 'SC9J',
                 'SMFV',
                 'XR6D',
                 'DP5T',
                 '57NQ',
                 'W13Z',
                 '71FR',
                 ]
    tasks = []
    for l in linkbots:
        tasks.append( asyncio.ensure_future(task(l, q)) )

    tasks.append( asyncio.ensure_future(consumer(q)) )
    
    rc = loop.run_until_complete(asyncio.wait(tasks))
    sys.exit(rc)
