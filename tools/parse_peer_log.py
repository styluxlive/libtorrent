#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from __future__ import print_function

import glob
import os
import sys

# usage: parse_peer_log <path-to-libtorrent-peer-logs>

log_files = []

for p in glob.iglob(os.path.join(sys.argv[1], '*.log')):
    name = os.path.split(p)[1]
    if name == 'main_session.log':
        continue
    print(name)
    with open(p, 'r') as f:
        out_file = f'{p}.dat'
        log_files.append(out_file)
        with open(out_file, 'w+') as out:
            uploaded_blocks = 0
            downloaded_blocks = 0

            for line in f:
                t = line.split(': ')[0].split('.')[0]
                log_line = False
                if ' ==> PIECE' in line:
                    uploaded_blocks += 1
                    log_line = True

                if ' <== PIECE' in line:
                    downloaded_blocks += 1
                    log_line = True

                if log_line:
                    print('%s\t%d\t%d' % (t, uploaded_blocks, downloaded_blocks), file=out)

with open('peers.gnuplot', 'wb') as out:
    print("set term png size 1200,700", file=out)
    print('set xrange [0:*]', file=out)
    print('set xlabel "time"', file=out)
    print('set ylabel "blocks"', file=out)
    print('set key box', file=out)
    print('set xdata time', file=out)
    print('set timefmt "%H:%M:%S"', file=out)
    print('set title "uploaded blocks"', file=out)
    print('set output "peers_upload.png"', file=out)
    print('plot', end=' ', file=out)
    first = True
    for n in log_files:
        if not first:
            print(',', end=' ', file=out)
        first = False
        print(
            f""" "{n}" using 1:2 title "{os.path.split(n)[1].split('.log')[0]}" with steps""",
            end=' ',
            file=out,
        )
    print('', file=out)

    print('set title "downloaded blocks"', file=out)
    print('set output "peers_download.png"', file=out)
    print('plot', end=' ', file=out)
    first = True
    for n in log_files:
        if not first:
            print(',', end=' ', file=out)
        first = False
        print(
            f""" "{n}" using 1:3 title "{os.path.split(n)[1].split('.log')[0]}" with steps""",
            end=' ',
            file=out,
        )
    print('', file=out)
os.system('gnuplot peers.gnuplot')
