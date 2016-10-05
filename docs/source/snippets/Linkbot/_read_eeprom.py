import linkbot3 as linkbot

# My Linkbot's ID is 'ZRG6'
l = linkbot.Linkbot('ZRG6')

print(l._eeprom.read(0x430, 3))
