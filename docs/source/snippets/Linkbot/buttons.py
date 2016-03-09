import linkbot

# This is my accelerometer event callback. Whenever the Linkbot detects that
# the accelerometer has moved, this callback is executed.
def cb(*args):
    print('Button event: ', args)

l = linkbot.Linkbot('XJLL')
l.buttons.set_event_handler(cb)
input('Button events enabled. Try moving pressing some buttons. Press "Enter" to '
      'continue.')
print('Disabling button events...')
l.buttons.set_event_handler()
