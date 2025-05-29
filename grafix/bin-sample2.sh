#!/bin/bash
#
# Title: bin-sample2.sh
# Description: create bin-sample2.png
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
gnuplot -p bin-sample2.gp
#
