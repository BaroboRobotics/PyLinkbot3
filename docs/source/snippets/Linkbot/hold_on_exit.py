#!/usr/bin/env python3

import linkbot

l = linkbot.Linkbot('ZRG6')
l.motors.set_hold_on_exit(True)
l.motors.move(90, 90, 90)
