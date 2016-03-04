import linkbot

l = linkbot.Linkbot('5H57')
print('Battery voltage: ', l.battery.voltage())
print('Battery level: ', l.battery.percentage())
