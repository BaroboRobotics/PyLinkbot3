#!/usr/bin/env python3

# Tested functions:

import asyncio
import concurrent
import functools
import linkbot
import sys
import random
import collections
import logging
import signal

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class CoroPool():
    def __init__(self, maxsize=4):
        self._maxsize = maxsize
        self._pool = set()
        self._putters = collections.deque()
        self._getters = collections.deque()

    async def put(self, coro):
        try:
            if len(self._pool) >= self._maxsize:
                putter = asyncio.Future()
                self._putters.append(putter)
                print('Putter waiting...')
                await putter
                print('Putter waiting...done')
            fut = await coro
            self._pool.add(fut)
            self._wake_next(self._getters)
        except Exception as e:
            print('Exception in put(): ', str(e))

    async def consume(self):
        if len(self._pool) == 0:
            getter = asyncio.Future()
            self._getters.append(getter)
            await getter

        print('Waiting for futures...', len(self._pool))
        try:
            done, pending = await asyncio.wait(self._pool, return_when=concurrent.futures.FIRST_COMPLETED)
            print('{} done.'.format(len(done)))
            self._pool = pending
            for _ in range(len(done)):
                self._wake_next(self._putters)

        except Exception as e:
            print('EXCEPTION!!!!!!!!!!!!!!!!!', str(e))
            raise
        return done

    def _wake_next(self, q):
        print('{} items in wake queue.'.format(len(q)))
        while q:
            item = q.popleft()
            if not item.done():
                print('Wake one.')
                item.set_result(None)
                break
        print('wake done.')
                

async def task(serialid, queue):

    def done(fut):
        print(serialid)

    async def cb(*args):
        print('{} encoder event.'.format(serialid))

    l = await linkbot.AsyncLinkbot.create(serialid)
    #await l.motors[0].set_power(128)
    #fut = await l.motors[0].set_event_handler(cb)
    #await fut

    for i in range(100):
        print(serialid, 'ping: ', i)
        #fut = await l.motors.angles() 
        '''
        await queue.put(
                l.led.set_color(
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255))
                )
        '''
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
    #await l.motors[0].set_event_handler()
    #await l.motors.stop()

    return None

async def consumer(queue):
    while True:
        futs = await queue.consume()
        print('Consumed ', len(futs))

def stop_everything(loop):
    print('Stopping event loop. These tasks are not yet complete:')
    for task in asyncio.Task.all_tasks(loop):
        task.print_stack()
    loop.stop()

if __name__ == '__main__':
    q = CoroPool(maxsize=4)
    serialId = 'LOCL'
    if len(sys.argv) ==  2:
        serialId = sys.argv[1]

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
                 #'2DPF',
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
        tasks.append( asyncio.ensure_future(task(l, q)) )

    #tasks.append( asyncio.ensure_future(consumer(q)) )
    
    rc = loop.run_until_complete(asyncio.wait(tasks))
    sys.exit(rc)
