import linkbot3 as linkbot
import asyncio

# This is my accelerometer event callback. Whenever the Linkbot detects that
# the accelerometer has moved, this callback is executed.
async def async_cb(x, y, z, timestamp):
    print('Accel event: ', x, y, z, timestamp)
    await asyncio.sleep(2)
    print('Event handler completed.')

l = linkbot.Linkbot('7944')
print('Current accelerometer values: ', l.accelerometer.values())
print('Current X axis value: ', l.accelerometer.x())
print('Current Y axis value: ', l.accelerometer.y())
print('Current Z axis value: ', l.accelerometer.z())
print('Enabling accelerometer events...')
l.accelerometer.set_event_handler(async_cb)
input('Accelerometer events enabled. Try moving the Linkbot. Press "Enter" to '
      'continue.')
print('Disabling accelerometer events...')
l.accelerometer.set_event_handler()
