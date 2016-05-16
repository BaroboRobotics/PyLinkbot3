#!/usr/bin/env python3

import linkbot3
import sys
import logging

#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

if len(sys.argv) == 2:
    serial_id = sys.argv[1]
else:
    serial_id = input('Please enter robot serial id: ')

l = linkbot3.Linkbot(serial_id)
l.motors.move([90, 90, 90])
    
