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

logging.basicConfig(level=logging.INFO)
DOCKER_CLI =  Client(base_url = 'tcp://10.0.0.24:2375')
HOST_IP = '10.0.0.24'

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
        logging.info( '%d is down' % port)
        return False

def find_port():
    for port in range(9000,10000):
        if not Is_open(HOST_IP, port):
            return port
    raise NoPortError()

class ParaviewApp(object):
    """docstring for ParaviewApp"""
    def __init__(self, filename):
        super(ParaviewApp, self).__init__()
        self.filename = filename

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


    def stop(self):
        DOCKER_CLI.stop(container = self._container_id)

    def remove(self):
        DOCKER_CLI.remove_container(container=self._container_id)

    def close(self):
        self.stop()
        self.remove()
