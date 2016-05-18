import linkbot3 as linkbot

# My Linkbot's ID is 'DGKR'
l = linkbot.Linkbot('DGKR')

print(l._eeprom.read(0x430, 3))
