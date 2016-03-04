import linkbot

# My Linkbot's ID is 'DGKR'
l = linkbot.Linkbot('DGKR')

# move forward by rotating wheels 90 degrees
l.motors.move([90, 0, -90])

# Now move back the same distance
l.motors.move([-90, 0, 90])

# Now set the motion controll to a smooth controller
for motor in l.motors:
    motor.set_controller(linkbot.Motor.Controller.SMOOTH)
    motor.set_accel(30)
    motor.set_decel(30)

# move forward by rotating wheels 90 degrees
l.motors.move([90, 0, -90])

# Now move back the same distance
l.motors.move([-90, 0, 90])

