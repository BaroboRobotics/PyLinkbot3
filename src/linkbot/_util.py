import asyncio
import functools
import math

DEFAULT_TIMEOUT=10

def rad2deg(rad):
    return rad*180/math.pi

def deg2rad(deg):
    return deg*math.pi/180

def chain_futures(fut1, fut2, conv=lambda x: x):
    def done(fut2, conv, fut1):
        if fut1.cancelled():
            fut2.cancel()
        else:
            fut2.set_result( conv(fut1.result()) )

    fut1.add_done_callback(
            functools.partial(
                done,
                fut2,
                conv)
            )

def run_linkbot_coroutine(coro, loop):
    fut = loop.run_until_complete(
            asyncio.wait_for(
                asyncio.ensure_future(coro),
                DEFAULT_TIMEOUT ) )
    result = loop.run_until_complete(asyncio.wait_for(fut, DEFAULT_TIMEOUT))
    return result
