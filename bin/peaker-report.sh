#!/bin/bash
#
# Title: peaker-report.sh
# Description: dump peakers from database
# Development Environment: OS X 10.15.2/postgres 12.12
# Author: G.S. Cole (guy at shastrax dot com)
#
PGDATABASE=mastodon
PGHOST=localhost
PGPASSWORD=batabat
PGUSER=mastodon_client
#
TODAY=$(date '+%Y-%m-%d')
#
REPORT_DIR=/var/mellow/mastodon/report
REPORT_FILE_NAME="$REPORT_DIR/peakers-${TODAY}.txt"
#
psql $PGDATABASE -c "select freq_hz, obs_first, obs_last, population, name from mastodon_v1.population inner join mastodon_v1.site on site_id = site.id order by freq_hz;" > $REPORT_FILE_NAME
#
