import linkbot3 as linkbot

l = linkbot.Linkbot('7944')
print('Battery voltage: ', l.battery.voltage())
print('Battery level: ', l.battery.percentage())
