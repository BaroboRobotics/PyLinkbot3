#!/usr/bin/env python3

import linkbot 
import logging
import asyncio
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

async def task():
    l = await linkbot.AsyncLinkbot.create('LOCL')
    fut = await l.getEncoderValues()
    print(await fut)

loop = asyncio.get_event_loop()
loop.run_until_complete(task())

