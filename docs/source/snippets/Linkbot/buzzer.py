import linkbot
import time

# My Linkbot's ID is 'DGKR'
l = linkbot.Linkbot('DGKR')

# Emit a tone at 440 Hz for 1 second
l.buzzer.set_frequency(440)
time.sleep(1)
l.buzzer.set_frequency(0)
