import linkbot3 as linkbot

l = linkbot.Linkbot('DGKR')
print('Battery voltage: ', l.battery.voltage())
print('Battery level: ', l.battery.percentage())
