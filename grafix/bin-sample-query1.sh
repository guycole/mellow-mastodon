#!/bin/bash
#
# Title: bin-sample-query1.sh
# Description: extract and plot bin-sample graph
# Development Environment: OS X 10.15.2/postgres 12.12
# Author: G.S. Cole (guy at shastrax dot com)
#
export PGDATABASE=mastodon
export PGHOST=localhost
export PGPASSWORD=batabat
export PGUSER=mastodon_client
#
psql $PGDATABASE -t -c "select freq_hz, signal_dbm from mastodon_v1.bin_sample where row_head_id < 5 order by freq_hz;" > bin-sample1.txt
tr -d '|' < bin-sample1.txt > bin-sample1.dat
gnuplot -p bin-sample1.gp
#
psql $PGDATABASE -t -c "select freq_hz, rolling_mean, signal_dbm from mastodon_v1.bin_sample where row_head_id < 5 order by freq_hz;" > bin-sample2.txt
tr -d '|' < bin-sample2.txt > bin-sample2.dat
gnuplot -p bin-sample2.gp
#
psql $PGDATABASE -t -c "select freq_hz, rolling_mean, signal_dbm from mastodon_v1.bin_sample where freq_hz > 400000000 order by freq_hz;" > bin-sample3.txt
tr -d '|' < bin-sample3.txt > bin-sample3.dat
gnuplot -p bin-sample3.gp
