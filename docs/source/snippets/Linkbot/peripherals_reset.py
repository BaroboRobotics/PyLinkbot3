#!/usr/bin/env python3

import linkbot

l = linkbot.Linkbot('ZRG6')
l.set_peripherals_reset(0xff)
l.buzzer.set_frequency(440)
l.led.set_color(255, 0, 0)
l.motors.move(90, 90, 90)
