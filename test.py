#!/usr/bin/env python3

import linkbot as linkbotproxy
import logging
#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

l = linkbotproxy.Linkbot('LOCL')
print(l.getEncoderValues().result())

l2 = linkbotproxy.Linkbot('ZVT7')
print(l2.getEncoderValues().result())

