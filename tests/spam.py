#!/usr/bin/env python3

''' Test robots:
    linkbots = [ 'ZVT7',
                 'DGKR',
                 'T552',
                 '7ST7',
                 'F7JD',
                 '8Z77',
                 'HFDJ',
                 'HBLV',
                 'ZRG6',
                 '958T',
                 'ZK53',
                 '1ZH6',
                 'ABCD',
                 'TV98',
                 'L5WM',
                 '1175',
                 'QBL4',
                 'R277',
                 'T81H',
                 'CTN3',
                 ]
'''

import asyncio
import concurrent
import functools
import linkbot
import sys
import random
import collections
import logging
import signal

#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

async def task(serialid):

    def done(fut):
        print(serialid)

    async def cb(*args):
        print('{} encoder event.'.format(serialid))

    try:
        l = await linkbot.AsyncLinkbot.create(serialid)
    except:
        print('Could not connect to Linkbot: {}'.format(serialid))
        return

    for i in range(100):
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
    linkbots = [ 'ZVT7',
                 'DGKR',
                 'T552',
                 '7ST7',
                 'F7JD',
                 '8Z77',
                 'HFDJ',
                 'HBLV',
                 'ZRG6',
                 '958T',
                 'ZK53',
                 '1ZH6',
                 'ABCD',
                 'TV98',
                 'L5WM',
                 '1175',
                 'QBL4',
                 'R277',
                 'T81H',
                 'CTN3',
                 ]
    '''
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
    '''
    tasks = []
    for l in linkbots:
        tasks.append( asyncio.ensure_future(task(l)) )

    #tasks.append( asyncio.ensure_future(consumer(q)) )
    
    rc = loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    sys.exit(rc)
