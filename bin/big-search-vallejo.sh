#!/bin/bash
#
# Title: big-search-vallejo.sh
# Description: 
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
BIN_SIZE=5k
DURATION=57m
#DURATION=5m
FREQ_LOW=28M
FREQ_HIGH=1G
REPORT=19m # 3x19=57 duration
#
HOST_NAME=$(hostname)
SCRIPT_NAME=$0
TODAY=$(date '+%Y-%m-%d')
UUID=$(uuidgen)
#
FILE_NAME="big-search-${UUID}.vallejo1"
#
rtl_power -f $FREQ_LOW:$FREQ_HIGH:$BIN_SIZE -i $REPORT -e $DURATION /var/mellow/mastodon/fresh/$FILE_NAME 
#
# gsc@rpi4f:2020>./big-search-vallejo.sh
# Number of frequency hops: 348
# Dongle bandwidth: 2793103Hz
# Downsampling by: 1x
# Cropping by: 0.00%
# Total FFT bins: 356352
# Logged FFT bins: 356352
# FFT bin size: 2727.64Hz
# Buffer size: 16384 bytes (2.93ms)
# Reporting every 300 seconds
# Found 1 device(s):
#   0:  RTLSDRBlog, Blog V4, SN: 00000001
#
# Using device 0: Generic RTL2832U OEM
# Found Rafael Micro R828D tuner
# RTL-SDR Blog V4 Detected
# Tuner gain set to automatic.
# Exact sample rate is: 2793103.098090 Hz
# 
# User cancel, exiting...
#
