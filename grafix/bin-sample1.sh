#!/bin/bash
#
# Title: bin-sample1.sh
# Description: create bin-sample1.png
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
gnuplot -p bin-sample1.gp
#
