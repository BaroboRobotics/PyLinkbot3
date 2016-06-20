import linkbot3 as linkbot
import logging

def cb(*args, **kwargs):
    print('Callback!')
    print(args)

l = linkbot.Linkbot('2KDV')
l.motors.set_event_handler(cb)
input('Press Enter to continue')
l.motors.set_event_handler()
