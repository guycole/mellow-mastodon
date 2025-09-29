#!/bin/bash
#
# Title: pruner.sh
# Description: delete obsolete files
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
#WORK_DIR="/mnt/sda/gsc/mellow/mastodon"
#
echo "begin pruner"
#
cd $WORK_DIR
#
# cleanup of json and gnuplot
rm -rf ${COOKED_DIR}
mkdir ${COOKED_DIR}
#
# cleanup of processed CSV files
rm -rf ${PROCESSED_DIR}
mkdir ${PROCESSED_DIR}
# 
echo "end csv2json"
#
