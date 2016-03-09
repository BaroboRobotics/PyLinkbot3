import linkbot
import logging

def cb(*args, **kwargs):
    print('Callback!')
    print(args)

l = linkbot.Linkbot('DGKR')
l.motors[0].set_event_handler(cb)
input('Press Enter to continue')
l.motors[0].set_event_handler()
