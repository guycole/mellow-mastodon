#!/bin/bash
#
# Title: noaa-wx01.sh
# Description: test script for NOAA weather
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
set -euo pipefail
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
PYTHONPATH="$HOME/github/mellow-mastodon-v1/src"; export PYTHONPATH
#
hostname=$(hostname)
logger -p local3.info "mastodon noaa-wx01 $hostname"
#
FRESH_DIR=/var/wombat/fresh/mastodon
#
BIN_SIZE=2k
DURATION=60s
FREQ_LOW=162.400M
FREQ_HIGH=162.550M
REPORT=1s
RTL_GAIN=${RTL_GAIN:-auto}
#
HOST_NAME=$(hostname)
SCRIPT_NAME=$0
EPOCH_SECONDS=$(date '+%s')
TODAY=$(date '+%Y-%m-%d')
UUID=$(uuidgen)
#
RTL_POWER="/usr/local/bin/rtl_power"
POWER_FILE_NAME="${UUID}.csv"
#
# perform collection
logger -p local3.info "mastodon noaa-wx01 $HOST_NAME $SCRIPT_NAME $EPOCH_SECONDS $TODAY $UUID"
time $RTL_POWER -g $RTL_GAIN -f $FREQ_LOW:$FREQ_HIGH:$BIN_SIZE -i $REPORT -e $DURATION > /tmp/$POWER_FILE_NAME
#
# perform analysis
WORK_DIR="$HOME/github/mellow-mastodon-v1/src/collector"
#
cd $WORK_DIR
source venv/bin/activate
python3 ./collector.py "$UUID" "$EPOCH_SECONDS"
#
mv /tmp/$POWER_FILE_NAME $FRESH_DIR/$POWER_FILE_NAME
#