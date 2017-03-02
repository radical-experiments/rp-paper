#!/usr/bin/env python

import sys
import glob
import pprint
import radical.utils as ru

def main():
    for prof in sorted(glob.glob('*.json')):
        data  = ru.read_json(prof)
        flops = 0.0
        mem   = 0.0
        for time,entry in data['cpu']['sequence']:
            flops += entry['flops']
        for time,entry in data['mem']['sequence']:
            mem += entry['rss']
        print '%s,%.1f,%.1f' % (prof, flops, mem)

if __name__ == '__main__':
    main()

