import linkbot3 as linkbot
import math
import time
import logging

logging.basicConfig(level=logging.DEBUG)

# My Linkbot's ID is 'ZRG6'
l = linkbot.Linkbot('ZRG6')

start_time = time.time()
# Run a loop for 10 seconds
while (time.time()-start_time) < 10:
    # Modulate each color channel using a sin wave
    r = 127+128*math.sin(2*time.time())
    g = 127+128*math.sin(2*time.time() + 2*math.pi/3)
    b = 127+128*math.sin(2*time.time() + 4*math.pi/3)
    l.led.set_color(int(r), int(g), int(b))

