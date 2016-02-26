import linkbot

# My Linkbot's ID is 'DGKR'
l = linkbot.Linkbot('DGKR')

# move forward by rotating wheels 90 degrees
l.motors.move([90, 0, -90])

# Now move back the same distance
l.motors.move([-90, 0, 90])
