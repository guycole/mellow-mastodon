#!/bin/bash
#
# Title: validator.sh
# Description: verify collection files and write stats
# Development Environment: Ubuntu 22.04.05 LTS
# Author: Guy Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
IMAGE="${IMAGE:-ghcr.io/guycole/wombat-mastodon:latest}"

echo "start validate"
#
docker pull "${IMAGE}"
docker rm mastodon-validate
docker run -v /var/wombat:/mnt/wombat --name mastodon-validate "${IMAGE}"
#
#docker rm mastodon-koala;docker run -e stuntbox=koala -v /var/wombat:/mnt/wombat --name mastodon-koala "${IMAGE}"
#
#$HOME/github/mellow-wombat/bin/mastodon-koala-import.sh
#
echo "end validate"
#
