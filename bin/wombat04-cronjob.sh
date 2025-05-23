#!/bin/bash
#
# Title: wombat04-cronjob.sh
# Description: invoke once per hour
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
for ndx in {1..3}
do
  /home/gsc/Documents/github/mellow-mastodon/bin/uhf-search-vallejo.sh
done
#
/home/gsc/Documents/github/mellow-mastodon/bin/wombat04-to-s3.sh
#
