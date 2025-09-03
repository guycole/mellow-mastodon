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
PROCESSED_DIR="/var/mellow/mastodon/processed"
WORK_DIR="/var/mellow/mastodon"
#
echo "start move"
cd $WORK_DIR
#
counter=0
for file_name in $(aws s3 ls $SRC_BUCKET --profile wombat03rw); 
do
  if (( counter % 6 == 0 )); then
    if (( counter > 0 )); then
      aws s3 cp $SRC_BUCKET$file_name . --profile=wombat03rw
      aws s3 mv $SRC_BUCKET$file_name $DST_BUCKET$file_name --profile=wombat03rw
      tar -xzf $file_name
      mv $file_name $PROCESSED_DIR
    fi
  fi

  ((counter++))
done

echo "end move"
#
