import linkbot3 as linkbot
import asyncio

async def cb(*args):
    print(args)

async def task(serial_id):
    l = await linkbot.AsyncLinkbot.create(serial_id)
    r_fut = await l.button.values()
    print('Current button values: ', await r_fut)

    r_fut = await l.button.pwr()
    print('Current power button value: ', await r_fut)
    r_fut = await l.button.a()
    print('Current "a" button value: ', await r_fut)
    r_fut = await l.button.b()
    print('Current "b" button value: ', await r_fut)

    print('Enabling button events for 5 seconds... This will override default '
          'button functionality')
    await l.button.set_event_handler(cb)
    await asyncio.sleep(5)
    print('Done. Removing button handler to restore button functionality...')
    await l.button.set_event_handler()

loop = asyncio.get_event_loop()
loop.run_until_complete(task('DGKR'))
loop.close()

