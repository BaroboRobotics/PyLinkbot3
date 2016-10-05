import linkbot3 as linkbot

# My Linkbot's ID is 'ZRG6'
l = linkbot.Linkbot('ZRG6')

l.motors.reset()
l.motors.move([0, 0, 0], relative=False)
