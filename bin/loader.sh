#!/bin/bash
#
# Title: loader.sh
# Description: parse files from s3 and load into database
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
FRESH_DIR="fresh"
HOME_DIR="/home/gsc/Documents/github"
#HOME_DIR="/Users/gsc/Documents/github"
WORK_DIR="/var/mellow/mastodon"
#
cd $WORK_DIR
#
if [[ -d "$fresh_dir" ]]; then
  rmdir fresh
fi
#
mv archive fresh
#
echo "start load"
cd $HOME_DIR/mellow-mastodon/src
source venv/bin/activate
time python3 ./loader.py
rmdir fresh
echo "end load"
#
