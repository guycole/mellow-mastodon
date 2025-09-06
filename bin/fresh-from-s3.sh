#!/bin/bash
#
# Title: fresh-from-s3.sh
# Description: move fresh s3 files to local for database import
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
DST_BUCKET=s3://mellow-mastodon-uw2-m7766.braingang.net/archive/
SRC_BUCKET=s3://mellow-mastodon-uw2-m7766.braingang.net/fresh/
#
ARCHIVE_DIR="/var/mellow/mastodon/archive"
FRESH_DIR="/var/mellow/mastodon/fresh"
WORK_DIR="/var/mellow/mastodon"
#
S3_LIST="/tmp/s3list.txt"
PP1_ARCHIVE_DIR="/mnt/pp1/gsc/mellow/mastodon/archive"
#
echo "start move"
cd $WORK_DIR
#
rm $S3_LIST
aws s3 ls $SRC_BUCKET --profile wombat03rw | cut -c 32-80 > /tmp/s3list.txt
#
while IFS= read -r file_name; do
  if [[ -z "$file_name" ]]; then
    echo "skipping empty string"
  else
    aws s3 cp $SRC_BUCKET$file_name . --profile=wombat03rw
    aws s3 mv $SRC_BUCKET$file_name $DST_BUCKET$file_name --profile=wombat03rw
    tar -xzf $file_name
    mv $file_name $PP1_ARCHIVE_DIR
  fi
done < "$S3_LIST"
#
echo "end move"
#
