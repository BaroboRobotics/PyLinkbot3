import linkbot

# My Linkbot's ID is '2G7D'
l = linkbot.Linkbot('2G7D')

# move forward by rotating wheels 90 degrees
l.motors.move([90, 0, -90])

# Now move back the same distance
l.motors.move([-90, 0, 90])

# Now set the motion controll to a smooth controller
