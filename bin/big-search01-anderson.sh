#!/bin/bash
#
# Title: big-search01-anderson.sh
# Description: 
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
BIN_SIZE=5k
DURATION=19m
#DURATION=5m
FREQ_LOW=117.975M
FREQ_HIGH=960M
REPORT=1m 
#
HOST_NAME=$(hostname)
SCRIPT_NAME=$0
TODAY=$(date '+%Y-%m-%d')
UUID=$(uuidgen)
#
FILE_NAME="big-search-${UUID}.anderson1"
#
#rtl_power -f $FREQ_LOW:$FREQ_HIGH:$BIN_SIZE -i $REPORT -e $DURATION /var/mellow/mastodon/fresh/$FILE_NAME 
rtl_power -f $FREQ_LOW:$FREQ_HIGH:$BIN_SIZE -i $REPORT -e $DURATION /mnt/pp1/mellow/mastodon/fresh/$FILE_NAME 
#
