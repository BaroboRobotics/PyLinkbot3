import linkbot

# My Linkbot's ID is 'DGKR'
l = linkbot.Linkbot('DGKR')

# move forward by rotating wheels 90 degrees
l.motors.move([90, 0, -90])

# Now move back the same distance
l.motors.move([-90, 0, 90])

# Now set the motion controll to a smooth controller
l.motors[0].set_controller(linkbot.Motor.Controller.SMOOTH)
l.motors[1].set_controller(linkbot.Motor.Controller.SMOOTH)
l.motors[2].set_controller(linkbot.Motor.Controller.SMOOTH)

# move forward by rotating wheels 90 degrees
l.motors.move([90, 0, -90])

# Now move back the same distance
l.motors.move([-90, 0, 90])

