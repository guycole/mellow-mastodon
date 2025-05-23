#!/bin/bash
#
# Title: uhf-search-vallejo.sh
# Description: 
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
BIN_SIZE=5k
DURATION=57m
#DURATION=5m
FREQ_LOW=88M
FREQ_HIGH=512M
REPORT=7m
#
HOST_NAME=$(hostname)
SITE_NAME="vallejo1"
SCRIPT_NAME=$0
TODAY=$(date '+%Y-%m-%d')
UUID=$(uuidgen)
#
FILE_NAME="uhf-search-${UUID}.${SITE_NAME}"
#
rtl_power -f $FREQ_LOW:$FREQ_HIGH:$BIN_SIZE -i $REPORT -e $DURATION /var/mellow/mastodon/fresh/$FILE_NAME 
#
# gsc@rpi4d:1615>./uhf-search-vallejo.sh
# Number of frequency hops: 152
# Dongle bandwidth: 2789473Hz
# Downsampling by: 1x
# Cropping by: 0.00%
# Total FFT bins: 155648
# Logged FFT bins: 155648
# FFT bin size: 2724.09Hz
# Buffer size: 16384 bytes (2.94ms)
# Reporting every 660 seconds
# Found 1 device(s):
#   0:  Realtek, RTL2838UHIDIR, SN: 00000001
#
# Using device 0: Generic RTL2832U OEM
# Found Rafael Micro R820T tuner
# Tuner gain set to automatic.
# Exact sample rate is: 2789473.062902 Hz
# 
# User cancel, exiting...
#
