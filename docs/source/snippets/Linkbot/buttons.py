import linkbot3 as linkbot

# This is my button event callback. Whenever the Linkbot detects that
# a button has been pressed or released, this callback is executed.
def cb(*args):
    print('Button event: ', args)

l = linkbot.Linkbot('ZRG6')
l.buttons.set_event_handler(cb)
input('Button events enabled. Try moving pressing some buttons. Press "Enter" to '
      'continue.')
print('Disabling button events...')
l.buttons.set_event_handler()
