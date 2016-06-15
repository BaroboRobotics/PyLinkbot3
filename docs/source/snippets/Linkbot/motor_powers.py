import linkbot3 as linkbot
import time

l = linkbot.Linkbot('2KDV')
l.motors.set_powers([128, 128, 128])
time.sleep(2)
l.motors.stop()
