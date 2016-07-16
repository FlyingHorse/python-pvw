#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-16 17:01:46
# @Author  : liu yangyang (yangliucs07@163.com)
# @Link    : https://github.com/FlyingHorse
# @Version : $Id$

import json,logging

from docker import Client


logging.basicConfig(level=logging.INFO)

def calculate_cpu_percent(stats):
    cpu1 = stats['precpu_stats']['cpu_usage']['total_usage']
    system1 = stats['precpu_stats']['system_cpu_usage']
    cpu2 = stats['cpu_stats']['cpu_usage']['total_usage']
    system2 = stats['cpu_stats']['system_cpu_usage']
    # Calculate deltas
    cpu_delta = float(cpu2 - cpu1)
    system_delta = float(system2 - system1)
    # Calculate percent
    if (system_delta > 0.0 and cpu_delta > 0.0):
        cpu_percent = (cpu_delta / system_delta) * len(stats['cpu_stats']['cpu_usage']['percpu_usage']) * 100.0
    else:
        cpu_percent = 0.0

    return cpu_percent

#    if cpu_percent < 150:
#        return cpu_percent
#   else:
#      return 0.0

def calculate_memory_percent(stats):
    memory_percent = (float(stats['memory_stats']['usage']) / float(stats['memory_stats']['limit'])) * 100
    return memory_percent, stats['memory_stats']['usage']

def calculate_network(stats):
    rx = stats['networks']['eth0']['rx_bytes']
    tx = stats['networks']['eth0']['tx_bytes']
    data_in = rx
    data_out = tx
    return data_in, data_out

def get_container_stats(cli, container_id):
    try:
        stats = cli.stats(container_id)
        return stats
    except Exception, error:
        return error

def get_current_state(stats_resp):
    # Get generator and two stats packets
    stats = json.loads(stats_resp)
    # Calculate curated stats
    cpu_percent = calculate_cpu_percent(stats)
    mem_percent, mem_usage = calculate_memory_percent(stats)
    net_in, net_out = calculate_network(stats)
    # Put stats into JSON
    monitoring_stats = {
        "cpu_percent": cpu_percent,
        "mem_percent": mem_percent,
        "mem_usage": mem_usage,
        "net_in": net_in,
        "net_out": net_out
    }
    return monitoring_stats

def get_all_containers(cli):
    containers = cli.containers()
    return containers

def main():
    pass

if __name__ == '__main__':
    main()
