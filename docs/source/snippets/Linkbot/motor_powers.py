import linkbot3 as linkbot
import time

l = linkbot.Linkbot('ZRG6')
l.motors.set_powers([128, 128, 128])
time.sleep(2)
l.motors.stop()
