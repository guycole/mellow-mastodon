#!/bin/bash
#
# Title: band10a.sh
# Description: commercial FM broadcast
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
BIN_SIZE=200k
DURATION=3m
FREQ_LOWER=88M
FREQ_HIGHER=108M
REPORT=25
#
HOST_NAME=$(hostname)
SCRIPT_NAME=$0
UUID=$(uuidgen)
#
FILE_NAME="band10a-${UUID}.sfo1"
#
rtl_power -f $FREQ_LOWER:$FREQ_HIGHER:$BIN_SIZE -e $DURATION -i $REPORT /var/mellow/mastodon/fresh/$FILE_NAME 
#
