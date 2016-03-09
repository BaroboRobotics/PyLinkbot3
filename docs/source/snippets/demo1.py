import asyncio
import linkbot

async def task():
    # My Linkbot's ID is DGKR.
    l = await linkbot.AsyncLinkbot.create('DGKR') 
    # Move the Linkbot's first motor 90 degrees positive from its current
    # location and third motor -90 degrees from its current location.
    await l.motors.move([90,0,-90], relative=True)
    # Wait for the motion to finish on all motors 
    fut = await l.motors.move_wait()
    await fut

loop = asyncio.get_event_loop()
loop.run_until_complete(task())
loop.close()

