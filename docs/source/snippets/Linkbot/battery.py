import linkbot3 as linkbot

l = linkbot.Linkbot('ZRG6')
print('Battery voltage: ', l.battery.voltage())
print('Battery level: ', l.battery.percentage())
