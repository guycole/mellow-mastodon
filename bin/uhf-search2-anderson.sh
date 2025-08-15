#!/bin/bash
#
# Title: uhf-search-anderson2.sh
# Description: 30 MHz to 960 MHz energy survey
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
BIN_SIZE=5k
DURATION=19m
#DURATION=5m
FREQ_LOW=30M
FREQ_HIGH=960M
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
# gsc@rpi4d:1722>./uhf-search2-anderson.sh
# Number of frequency hops: 333
# Dongle bandwidth: 2792792Hz
# Downsampling by: 1x
# Cropping by: 0.00%
# Total FFT bins: 340992
# Logged FFT bins: 340992
# FFT bin size: 2727.34Hz
# Buffer size: 16384 bytes (2.93ms)
# Reporting every 60 seconds
# Found 1 device(s):
#  0:  Realtek, RTL2838UHIDIR, SN: 00000001
#
# Using device 0: Generic RTL2832U OEM
# Found Rafael Micro R820T tuner
# Tuner gain set to automatic.
# Exact sample rate is: 2792792.098612 Hz
# [R82XX] PLL not locked!
#
