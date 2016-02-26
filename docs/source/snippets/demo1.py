import asyncio
import linkbot

async def task():
    # My Linkbot's ID is DGKR.
    l = await linkbot.AsyncLinkbot.create('DGKR') 
    await l.motors.move([0,0,0])
    # Wait for the motion to finish on motors 1 and 3
    fut = await l.motors[0].move_wait()
    fut2 = await l.motors[2].move_wait()
    await fut
    await fut2

loop = asyncio.get_event_loop()
loop.run_until_complete(task())
loop.close()

