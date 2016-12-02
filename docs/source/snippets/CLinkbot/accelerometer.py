import linkbot3 as linkbot

l = linkbot.CLinkbot('ZRG6')
print('Current accelerometer values: ', l.get_accelerometer() )
print('Current accelerometer values: ', l.get_accelerometer_data() )
