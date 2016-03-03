import linkbot

# My Linkbot's ID is 'DGKR'
l = linkbot.Linkbot('DGKR')

print(l._read_eeprom(0x430, 3))
