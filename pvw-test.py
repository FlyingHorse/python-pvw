#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-14 19:58:08
# @Author  : liu yangyang (yangliucs07@163.com)
# @Link    : https://github.com/FlyingHorse
# @Version : $Id$

import time
import logging


from pvw import ParaviewApp

pv1 = ParaviewApp('')
pv1.start()

print pv1.url

print pv1.is_running()

try:
    for i in range(0,600):
        #print pv1.state()
        time.sleep(1)
except:
    logging.exception('error occurred')
finally:
    pv1.close()
    print 'test finish, close and remove app'

    print pv1.is_running()
    print pv1.state()
