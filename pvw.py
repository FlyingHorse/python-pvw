#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-14 18:44:40
# @Author  : liu yangyang (yangliucs07@163.com)
# @Link    : https://github.com/FlyingHorse
# @Version : $Id$

import os,logging
import socket

from docker import Client
from docker import errors

from docker_util import get_container_stats
from docker_util import get_current_state

logging.basicConfig(level=logging.INFO)
DOCKER_CLI =  Client(base_url = 'tcp://10.0.0.24:2375')
HOST_IP = '10.0.0.24'
USED_PORTS = set()

class NoPortError(StandardError):
     pass

def Is_open(ip,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((ip,int(port)))
        s.shutdown(2)
        logging.info( '%d is open' % port)
        return True
    except:
        logging.exception('sockect connet error')
        logging.info( '%d is down' % port)
        return False

def find_port():
    for port in range(9000,10000):
        if not port in USED_PORTS and not Is_open(HOST_IP, port):
            USED_PORTS.add(port)
            return port
    raise NoPortError()

class ParaviewApp(object):
    """docstring for ParaviewApp"""
    def __init__(self, filename):
        super(ParaviewApp, self).__init__()
        self.filename = filename
        self._url = None
        self._stats_generator = None

    @property
    def url(self):
        return self._url

    def start(self):
        try:
            port = find_port()
            self._container = DOCKER_CLI.create_container(
                                          image='paraviewweb',
                                          ports=[port],
                                          environment=["use_port=%d" % port],
                                          host_config = DOCKER_CLI.create_host_config(port_bindings={
                                                                                      port:port
                                                                                      },
                                                                                      binds=['/home/tools/paraview/import/:/import/','/home/tools/paraview/export/:/export/' ])
                                          )
            print self._container
            self._container_id = self._container.get('Id')
            print self._container_id
            DOCKER_CLI.start(container = self._container_id)
        except errors.NotFound, e:
            logging.exception('not found error when create container')
        except errors.APIError, e:
            logging.exception('api error when create container')
        except Exception, e:
            logging.exception('unkonwn error when create container')
        else:
            logging.info('container created sucessful. resp:%s' % self._container)
            self._url = 'http://10.0.0.24:%d/apps/Visualizer/' % port


    def _stop(self):
        try:
            DOCKER_CLI.stop(container = self._container_id)
            self._stats_generator = None
        except Exception, e:
            logging.exception('stop container failed, id: %s' % self._container_id)


    def _remove(self):
        try:
            DOCKER_CLI.remove_container(container=self._container_id)
            self._container_id = None
            self._container = None
        except Exception, e:
            logging.exception('remove container failed, id: %s' % self._container_id)


    def state(self):
        if self._container_id is None:
            return
        if self._stats_generator is None:
            self._stats_generator = get_container_stats(DOCKER_CLI, self._container_id)
        return get_current_state(self._stats_generator.next())

    def is_running(self):
        try:
            ins = DOCKER_CLI.inspect_container(self._container_id)
            return ins.get('State').get('Running')
        except Exception, e:
            logging.exception('check container running error. container_id:%s' % self._container_id)
            return False


    def close(self):
        self._stop()
        self._remove()
