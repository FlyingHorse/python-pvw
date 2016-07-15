#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-15 14:43:06
# @Author  : liu yangyang (yangliucs07@163.com)
# @Link    : https://github.com/FlyingHorse
# @Version : $Id$

import time
import logging

from pvw import ParaviewApp

logging.basicConfig(level=logging.INFO)

pvs = []
for i in range(0,10):
    pv = ParaviewApp('')
    pv.start()
    print pv.url
    pvs.append(pv)

time.sleep(200)

for pv in pvs:
    pv.close()

print 'test finish, close and remove'
