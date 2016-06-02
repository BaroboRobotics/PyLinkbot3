import linkbot3 as linkbot

# My Linkbot's ID is '7944'
l = linkbot.Linkbot('7944')

print(l._eeprom.read(0x430, 3))
