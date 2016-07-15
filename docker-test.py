#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-14 19:36:09
# @Author  : liu yangyang (yangliucs07@163.com)
# @Link    : https://github.com/FlyingHorse
# @Version : $Id$

import os

from docker import Client

DOCKER_CLI =  Client(base_url = 'tcp://10.0.0.24:2375')

container = DOCKER_CLI.create_container(image='hello-world')
print container

container = DOCKER_CLI.create_container(image='hello-world1')
print container

