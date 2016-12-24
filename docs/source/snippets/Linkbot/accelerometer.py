import linkbot3 as linkbot

# This is my accelerometer event callback. Whenever the Linkbot detects that
# the accelerometer has moved, this callback is executed.
i = 0
def cb(x, y, z, timestamp):
    global i
    print('Accel event: ', x, y, z, timestamp)
    print("Received {} events.".format(i))
    i += 1

l = linkbot.Linkbot('ZRG6')
print('Current accelerometer values: ', l.accelerometer.values())
print('Current X axis value: ', l.accelerometer.x())
print('Current Y axis value: ', l.accelerometer.y())
print('Current Z axis value: ', l.accelerometer.z())
print('Enabling accelerometer events...')
l.accelerometer.set_event_handler(cb)
input('Accelerometer events enabled. Try moving the Linkbot. Press "Enter" to '
      'continue.')
print('Disabling accelerometer events...')
l.accelerometer.set_event_handler()
