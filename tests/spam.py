#!/usr/bin/env python3

# Tested functions:

import asyncio
import linkbot
import sys


async def task(serialid, queue):

    def done(fut):
        print('.')

    l = await linkbot.AsyncLinkbot.create('ZVT7')

    for i in range(100):
        print('ping: ', i)
        fut = await l.motors.angles() 
        fut.add_done_callback(done)
        await queue.put(fut)

async def task2(serialid, queue):

    def done(fut):
        print('.2')

    l = await linkbot.AsyncLinkbot.create('DGKR')

    for i in range(100):
        print('ping: ', i)
        fut = await l.motors.angles() 
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
    tasks = [ 
            asyncio.ensure_future(task(serialId, q)), 
            asyncio.ensure_future(task2(serialId, q)), 
            asyncio.ensure_future(consumer(q)),
            ]
    
    rc = loop.run_until_complete(asyncio.wait(tasks))
    sys.exit(rc)
