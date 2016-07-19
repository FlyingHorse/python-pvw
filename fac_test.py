#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-16 19:55:43
# @Author  : liu yangyang (yangliucs07@163.com)
# @Link    : https://github.com/FlyingHorse
# @Version : $Id$

import time,threading,logging
from multiprocessing.dummy import Pool
from pvw_factory import PvwAppFactory
from selenium_pvw import simu_pvw

logging.basicConfig(level= logging.INFO,
                    filename= 'test.log',
                    filemode='w')

fac = PvwAppFactory()

num = 40

urls = []

try:
    for i in range(0,num):
        app = fac.start_pvw()
        urls.append(app.url)
        print( 'start pvw %i, url: %s' %(i, app.url))


    for i in range(0,num):
        t = threading.Thread(target = simu_pvw, args=(urls[i],))
        t.start()

    for i in range(0,400):
        for url,state in fac.states().items():
            print( '%s : %s' % (url, state))
        time.sleep(1)
finally:
    fac.destroy()
    print( 'test finish')


