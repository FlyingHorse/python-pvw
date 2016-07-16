#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-16 19:55:43
# @Author  : liu yangyang (yangliucs07@163.com)
# @Link    : https://github.com/FlyingHorse
# @Version : $Id$

import time
from pvw_factory import PvwAppFactory

fac = PvwAppFactory()

print 'app num inital %d' % fac.app_num()

for i in range(0,5):
    app = fac.start_pvw()
    print 'start pvw %i, url: %s' %(i, app.url)

for i in range(0,10):
    for url,state in fac.states().items():
        print '%s : %s' % (url, state)
    time.sleep(1)

fac.destroy()
print 'test finish'


