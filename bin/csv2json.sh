#!/bin/bash
#
# Title: csv2json.sh
# Description: read from fresh and write to cooked
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
HOME_DIR="/home/gsc/Documents/github"
#HOME_DIR="/Users/gsc/Documents/github"
#
PROCESSED_DIR="processed"
WORK_DIR="/var/mellow/mastodon"
#
echo "begin csv2json"
cd $HOME_DIR/mellow-mastodon/src
source venv/bin/activate
time python3 ./csv2json.py
#
cd $WORK_DIR
#
rm -rf ${PROCESSED_DIR}
mkdir ${PROCESSED_DIR}
#
echo "end csv2json"
#
