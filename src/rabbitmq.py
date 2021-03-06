#!/usr/bin/env python
#
# igcollect - RabbitMQ stats
#
# Copyright (c) 2016, InnoGames GmbH
#

from argparse import ArgumentParser
from time import time
import json
import urllib2
import base64


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--prefix', default='rabbitmq')
    return parser.parse_args()


def main():
    args = parse_args()
    rabbit_url = 'http://localhost:15672/api'
    template = args.prefix + '.{} {} ' + str(int(time()))
    nodes_metrics = ['fd_used', 'fd_total', 'sockets_used', 'sockets_total',
                     'mem_used', 'mem_limit', 'disk_free', 'disk_free_limit',
                     'proc_used', 'proc_total', 'run_queue', 'processors']

    overview_object_totals_metrics = [
        'consumers',
        'queues',
        'exchanges',
        'connections',
        'channels',
    ]

    overview_queue_totals_metrics = [
    'messages',
    'messages_ready',
    'messages_unacknowledged',
    ]

    overview_message_stats_metrics = ['publish']

    # Overview data
    data = download(rabbit_url + '/overview')
    nodename = data['node']

    for metric in overview_object_totals_metrics:
        try:
            print(template.format(
                'object_totals.' + metric, data['object_totals'][metric]
            ))
        except KeyError:
            pass
    for metric in overview_message_stats_metrics:
        try:
            print(template.format(
                'message_stats.' + metric, data['message_stats'][metric]
            ))
        except KeyError:
            pass

    for metric in overview_queue_totals_metrics:
        try:
            print(template.format(
                'queue_totals.' + metric, data['queue_totals'][metric]
            ))
        except KeyError:
                pass

    # Node data
    data = download(rabbit_url + '/nodes/' + nodename)

    for metric in nodes_metrics:
        try:
            print(template.format(metric, data[metric]))
        except KeyError:
            pass

    # Shovels data
    try:
        data = download(rabbit_url + '/shovels')
    except urllib2.HTTPError:
        pass
    else:
        print(template.format('object_totals.shovels', str(len(data))))
        for shovel in data:
            state = 0
            if shovel['state'] == 'running':
                state = 1
            print(template.format('shovels.' + shovel['name'], state))


def download(url):
    base64string = base64.encodestring('%s:%s' % ('guest', 'guest'))[:-1]
    req = urllib2.Request(url)
    req.add_header("Authorization", "Basic %s" % base64string)
    r = urllib2.urlopen(req)
    return json.load(r)


if __name__ == '__main__':
    main()
