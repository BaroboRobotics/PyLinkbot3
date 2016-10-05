import linkbot3 as linkbot
import time

# My Linkbot's ID is 'ZRG6'
l = linkbot.Linkbot('ZRG6')

# Emit a tone at 440 Hz for 1 second
l.buzzer.set_frequency(440)
time.sleep(1)
l.buzzer.set_frequency(0)
