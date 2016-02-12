#!/usr/bin/env python3

import linkbot 
import logging
import asyncio
#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
async def bcast_handler(payload):
    print(payload)

async def task():
    l = await linkbot.AsyncLinkbot.create('LOCL')

    fut = await l.get_joint_angles()
    print(await fut)

    l.rb_add_broadcast_handler('buttonEvent', bcast_handler)
    fut = await l.enableButtonEvent(enable=True)
    await fut
    print('Try pressing some buttons.')
    await asyncio.sleep(5)
    l.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(task())
import time
time.sleep(3)
