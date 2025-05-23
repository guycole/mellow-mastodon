#!/bin/bash
#
# Title: band23a.sh
# Description: 
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
BIN_SIZE=200k
DURATION=3m
FREQ_LOWER=470M
FREQ_HIGHER=512M
REPORT=25
#
HOST_NAME=$(hostname)
SITE_NAME="vallejo1"
SCRIPT_NAME=$0
UUID=$(uuidgen)
#
FILE_NAME="band23a-${UUID}.${SITE_NAME}"
#
rtl_power -f $FREQ_LOWER:$FREQ_HIGHER:$BIN_SIZE -e $DURATION -i $REPORT /var/mellow/mastodon/fresh/$FILE_NAME 
#
