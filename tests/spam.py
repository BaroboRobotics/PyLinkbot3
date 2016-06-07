#!/usr/bin/env python3

import asyncio
import concurrent
import functools
import linkbot3 as linkbot
import sys
import random
import collections
import logging
import signal

#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

async def task(serialid):
    try:
        l = await linkbot.AsyncLinkbot.create(serialid)
    except:
        print('Could not connect to Linkbot: {}'.format(serialid))
        return

    for i in range(10000):
        print(serialid, 'ping: ', i)
        fut = await l.led.set_color(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255))
        await fut
        if fut.cancelled():
            print('Future cancelled. Aborting...')
            return None

    fut = await l.led.set_color(0, 0, 255)
    await fut

    return None

def stop_everything(loop):
    print('Stopping event loop. These tasks are not yet complete:')
    for task in asyncio.Task.all_tasks(loop):
        task.print_stack()
    loop.stop()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, 
            functools.partial(stop_everything, loop) )
    loop.set_debug(enabled=True)
    linkbots = [ 'L9H3',
                 '6WW8',
                 '7944',
                 ]
    tasks = []
    for l in linkbots:
        tasks.append( asyncio.ensure_future(task(l)) )

    rc = loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    sys.exit(rc)
