#!/bin/bash
#
# Title: csv2json.sh
# Description: read CSV files and convert to JSON
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
HOME_DIR="/home/gsc/Documents/github"
#HOME_DIR="/Users/gsc/Documents/github"
#
COOKED_DIR="cooked"
PROCESSED_DIR="processed"
WORK_DIR="/var/mellow/mastodon"
#
echo "begin csv2json"
cd $HOME_DIR/mellow-mastodon/src/collector 
source venv/bin/activate
time python3 ./csv2json.py
#
if [ $# -ne 0 ]; then
  if [[ "$1" == "retain" ]]; then
    echo "skipping directory delete"
  else
    cd $WORK_DIR

    # cleanup of json and gnuplot
    rm -rf ${COOKED_DIR}
    mkdir ${COOKED_DIR}

    # cleanup of processed CSV files
    rm -rf ${PROCESSED_DIR}
    mkdir ${PROCESSED_DIR}
  fi
fi
 
echo "end csv2json"
#
