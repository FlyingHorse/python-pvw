#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-14 19:58:08
# @Author  : liu yangyang (yangliucs07@163.com)
# @Link    : https://github.com/FlyingHorse
# @Version : $Id$

import time

from pvw import ParaviewApp

pv1 = ParaviewApp('')
pv1.start()
print pv1.url


time.sleep(200)
pv1.close()
print 'test finish, close and remove app'
