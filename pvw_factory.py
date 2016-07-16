#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-16 19:42:57
# @Author  : liu yangyang (yangliucs07@163.com)
# @Link    : https://github.com/FlyingHorse
# @Version : $Id$

import os
from pvw import ParaviewApp

class PvwAppFactory(object):
    """docstring for PvwAppFactory
    """
    def __init__(self):
        super(PvwAppFactory, self).__init__()
        self._apps = []

    def start_pvw(self, filename = ''):
        app = ParaviewApp(filename)
        app.start()
        self._apps.append(app)
        return app

    def app_num(self):
        return len(self._apps)

    def close_app(self, app):
        app.close()
        self._apps.remove(app)

    def refresh_apps(self):
        if self.app_num() > 0:
            self._apps = filter(lambda x : x.is_running(), self._apps)

    def states(self):
        self.refresh_apps()
        if self._apps is None or len(self._apps) == 0:
            return
        states_map = {}
        for app in self._apps:
            states_map[app.url] = app.state()

        return states_map

    def destroy(self):
        self.refresh_apps()
        if self.app_num() > 0:
            for app in self._apps:
                app.close()
            self._apps = None

