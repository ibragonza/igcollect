#!/usr/bin/env python
#
# igcollect - Linux CPU performance factors
#
# Copyright (c) 2016, InnoGames GmbH
#

from argparse import ArgumentParser
from time import time


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--prefix', default='linux.cpu')
    return parser.parse_args()


def main():
    args = parse_args()
    factors = {
        'Intel(R) Xeon(R) CPU           L5520  @ 2.27GHz': 0.8,
        'Intel(R) Xeon(R) CPU           L5640  @ 2.27GHz': 1.0,
        'Intel(R) Xeon(R) CPU E5-2660 0 @ 2.20GHz': 1.2,
        'Intel(R) Xeon(R) CPU E5-2660 v2 @ 2.20GHz': 1.44,
        'Intel(R) Xeon(R) CPU E5-2680 v3 @ 2.50GHz': 1.8,
        'Intel(R) Xeon(R) CPU E5-2680 v4 @ 2.40GHz': 1.8
    }
    cpufactor = 1.0

    with open('/proc/cpuinfo') as fd:
        cpu_data = fd.readlines(1024)

    for line in cpu_data:
        factor = line.split(':', 1)[1].strip()
        if factor in factors:
            cpufactor = factors[factor]
            break

    now = str(int(time()))
    print('{}.perffactor {} {}'.format(args.prefix, cpufactor, now))


if __name__ == '__main__':
    main()