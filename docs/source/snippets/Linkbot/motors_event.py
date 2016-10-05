import linkbot3 as linkbot
import logging

def cb(*args, **kwargs):
    print('Callback!')
    print(args)

l = linkbot.Linkbot('ZRG6')
l.motors.set_event_handler(cb)
input('Press Enter to continue')
l.motors.set_event_handler()
