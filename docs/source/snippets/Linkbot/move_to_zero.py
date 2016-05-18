import linkbot3 as linkbot

# My Linkbot's ID is 'DGKR'
l = linkbot.Linkbot('DGKR')

l.motors.reset()
l.motors.move([0, 0, 0], relative=False)
