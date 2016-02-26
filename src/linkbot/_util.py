import asyncio
import functools
import math

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

