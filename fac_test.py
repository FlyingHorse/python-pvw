#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-16 19:55:43
# @Author  : liu yangyang (yangliucs07@163.com)
# @Link    : https://github.com/FlyingHorse
# @Version : $Id$

import time,threading
import logging

from multiprocessing.dummy import Pool
from pvw_factory import PvwAppFactory
from selenium_pvw import simu_pvw

num = 2
logging.basicConfig(level= logging.INFO,
                    filename= 'test%d.log' % num,
                    format='%(asctime)s %(message)s')

fac = PvwAppFactory()


secs = 20

urls = []

try:
    for i in range(0,num):
        app = fac.start_pvw()
        urls.append(app.url)
        logging.info( 'start pvw %i, url: %s' %(i, app.url))


    for i in range(0,num):
        t = threading.Thread(target = simu_pvw, args=(urls[i],secs/2))
        t.start()

    for i in range(0,secs):
        states = fac.states()
        if states is None:
            break
        for url,state in fac.states().items():
            logging.info( '%s : %s' % (url, state))
        time.sleep(1)
finally:
    fac.destroy()
    logging.info( 'test finish')


