import linkbot3 as linkbot

# My Linkbot's ID is '7944'
l = linkbot.Linkbot('7944')

for i in range(3):
    print(l.motors[i].angle())
