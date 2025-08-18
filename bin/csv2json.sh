#!/bin/bash
#
# Title: csv2json.sh
# Description:
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
HOME_DIR="/home/gsc/Documents/github"
#HOME_DIR="/Users/gsc/Documents/github"
#
echo "start csv2json"
cd $HOME_DIR/mellow-mastodon/src
source venv/bin/activate
python3 ./csv2json.py
echo "end csv2json"
#
