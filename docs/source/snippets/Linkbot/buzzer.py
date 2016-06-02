import linkbot3 as linkbot
import time

# My Linkbot's ID is '7944'
l = linkbot.Linkbot('7944')

# Emit a tone at 440 Hz for 1 second
l.buzzer.set_frequency(440)
time.sleep(1)
l.buzzer.set_frequency(0)
