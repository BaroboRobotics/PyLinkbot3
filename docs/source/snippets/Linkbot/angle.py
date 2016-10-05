import linkbot3 as linkbot

# My Linkbot's ID is 'ZRG6'
l = linkbot.Linkbot('ZRG6')

for i in range(3):
    print(l.motors[i].angle())
