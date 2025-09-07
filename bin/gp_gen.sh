#!/bin/bash
#
# Title: gp_gen.sh
# Description: gnuplot generator script invoke as gp_gen.sh filename (without extension)
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
#PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
if [[ $# -eq 0 ]] ; then
    echo "missing file name argument"
    exit 1
fi
#
DATA_FILE="$1.gp"
IMAGE_FILE="$1.png"
#
gnuplot <<-EOFMarker
set title "mastodon $1"
set xlabel 'frequency'
set ylabel 'dbm'
set grid
#
set terminal png size 1200,800
set output "$IMAGE_FILE"
set key outside
#
plot '$DATA_FILE' using 1:2 with points title 'dbm', '' using 1:3 with line title 'average' lw 3
#
EOFMarker
#