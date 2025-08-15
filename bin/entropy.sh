#!/bin/bash
#
# Title: wombat03-to-s3.sh
# Description: move mastodon files local file system to s3
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
TODAY=$(date '+%Y-%m-%d')
FILE_NAME="mastodon-${TODAY}.tgz"
#
DEST_BUCKET=s3://mellow-mastodon-uw2-m7766.braingang.net/archive/
#
SOURCE_DIR="archive"
WORK_DIR="/var/mellow/mastodon"
#
echo "start archive"
#
cd ${WORK_DIR}
tar -cvzf ${FILE_NAME} ${SOURCE_DIR}
#
echo "start s3 transfer" 
aws s3 mv ${FILE_NAME} $DEST_BUCKET --profile=cli_braingang
#
echo "cleanup"
rm -rf ${SOURCE_DIR}
mkdir ${SOURCE_DIR}
#
echo "end archive"
#
