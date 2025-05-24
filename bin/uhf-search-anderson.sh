#!/bin/bash
#
# Title: uhf-search-anderson.sh
# Description: 88 MHz to 512 MHz energy survey
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
BIN_SIZE=5k
DURATION=19m
#DURATION=5m
FREQ_LOW=88M
FREQ_HIGH=512M
REPORT=1m
#
HOST_NAME=$(hostname)
SITE_NAME="anderson1"
SCRIPT_NAME=$0
TODAY=$(date '+%Y-%m-%d')
UUID=$(uuidgen)
#
FILE_NAME="uhf-search-${UUID}.${SITE_NAME}"
#
rtl_power -f $FREQ_LOW:$FREQ_HIGH:$BIN_SIZE -i $REPORT -e $DURATION /tmp/$FILE_NAME 
# move to fresh directory after collection because s3 mv might interfere
mv /tmp/$FILE_NAME /var/mellow/mastodon/fresh
#
# gsc@rpi4k:224>./uhf-search-anderson.sh
# Number of frequency hops: 152
# Dongle bandwidth: 2789473Hz
# Downsampling by: 1x
# Cropping by: 0.00%
# Total FFT bins: 155648
# Logged FFT bins: 155648
# FFT bin size: 2724.09Hz
# Buffer size: 16384 bytes (2.94ms)
# Reporting every 60 seconds
# Found 1 device(s):
#  0:  RTLSDRBlog, Blog V4, SN: 00000001
#
# Using device 0: Generic RTL2832U OEM
# Found Rafael Micro R828D tuner
# RTL-SDR Blog V4 Detected
# Tuner gain set to automatic.
# Exact sample rate is: 2789473.062902 Hz
#
# User cancel, exiting...
#
