#!/bin/bash 
#
# Title: wombat01-to-s3.sh
# Description: move mastodon files from local file system to s3
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin:/opt/homebrew/bin/aws; export PATH
#
if [[ $# -eq 0 ]] ; then
    echo "missing project-site argument"
    exit 1
fi
#
TODAY=$(date '+%Y-%m-%d')
FILE_NAME="$1-${TODAY}.tgz"
#
DEST_BUCKET=s3://mellow-mastodon-uw2-m7766.braingang.net/fresh/
#
ARCHIVE_DIR="archive"
COOKED_DIR="cooked"
PROCESSED_DIR="processed"
WORK_DIR="/var/mellow/mastodon"
#
echo "start archive for $FILE_NAME"
#
cd ${WORK_DIR}
#
tar -cvzf ${FILE_NAME} ${ARCHIVE_DIR}
#
echo "start s3 transfer" 
aws s3 mv ${FILE_NAME} $DEST_BUCKET --profile=wombat01
#
echo "cleanup"
rm -rf ${ARCHIVE_DIR}
mkdir ${ARCHIVE_DIR}
#
echo "end archive"
#
