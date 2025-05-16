#!/bin/bash 
#
# Title: wombat04-to-s3.sh
# Description: move mastodon files from local file system to s3
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
DEST_BUCKET=s3://mellow-mastodon-uw2-m7766.braingang.net/fresh/
#
echo "start move"
cd /var/mellow/mastodon/fresh; gzip *
aws s3 mv . $DEST_BUCKET --recursive --profile=wombat04
echo "end move"
