#!/bin/bash
#
# Title: validator.sh
# Description: verify collection files and write stats
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
echo "start validate"
#
docker rm mastodon-validate;docker run -v /var/wombat:/mnt/wombat --name mastodon-validate mastodon:latest
#
#docker rm mastodon-koala;docker run -e stuntbox=koala -v /var/wombat:/mnt/wombat --name mastodon-koala mastodon:latest
#
#$HOME/github/mellow-wombat/bin/mastodon-koala-import.sh
#
echo "end validate"
#
