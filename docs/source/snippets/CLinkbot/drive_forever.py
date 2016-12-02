import linkbot3 as linkbot
import time

l = linkbot.CLinkbot('ZRG6')
l.drive_forever_nb()
time.sleep(5)
l.stop()

