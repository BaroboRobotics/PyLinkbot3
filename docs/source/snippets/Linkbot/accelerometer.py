import linkbot

# This is my accelerometer event callback. Whenever the Linkbot detects that
# the accelerometer has moved, this callback is executed.
def cb(x, y, z, timestamp):
    print('Accel event: ', x, y, z, timestamp)

l = linkbot.Linkbot('DGKR')
print('Current accelerometer values: ', l.accelerometer.values())
print('Current X axis value: ', l.accelerometer.x())
print('Current Y axis value: ', l.accelerometer.y())
print('Current Z axis value: ', l.accelerometer.z())
print('Enabling accelerometer events...')
l.accelerometer.set_event_handler(cb)
input('Accelerometer events enabled. Try moving the Linkbot. Press "Enter" to '
      'quit.')
print('Disabling accelerometer events...')
l.accelerometer.set_event_handler()
