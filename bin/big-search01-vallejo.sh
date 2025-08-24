#!/bin/bash
#
# Title: big-search01-vallejo.sh
# Description: mastodon collection
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
HOME_DIR="/home/gsc/Documents/github/mellow-mastodon"
#HOME_DIR="/Users/gsc/Documents/github/mellow-mastodon"
VARMEL_DIR=/var/mellow/mastodon
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
RTL_POWER="/usr/local/bin/rtl_power"
#
DATA_FILE_NAME="${UUID}.gz"
KIT_FILE_NAME="${UUID}.json"
#
if test -f "$HOME_DIR/bin/$1"; then
    echo "$1 noted."
else 
    echo "$1 not found."
    exit(1)
fi
#
time $RTL_POWER -f $FREQ_LOW:$FREQ_HIGH:$BIN_SIZE -i $REPORT -e $DURATION | gzip > /tmp/$DATA_FILE_NAME
#
mv /tmp/$DATA_FILE_NAME $VARMEL_DIR/fresh/$DATA_FILE_NAME
cp $HOME_DIR/bin/$1 $VARMEL_DIR/fresh/$KIT_FILE_NAME
#
