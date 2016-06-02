import linkbot3 as linkbot

# My Linkbot's ID is '7944'
l = linkbot.Linkbot('7944')

l.motors.reset()
l.motors.move([0, 0, 0], relative=False)
