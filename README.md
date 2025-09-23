mellow-mastodon
===============

Hello, [radio scanner](https://en.wikipedia.org/wiki/Radio_scanner) enthusiast.  Welcom to mellow-mastodon, an application which can handily operate on a [raspberry pi 4](https://en.wikipedia.org/wiki/Raspberry_Pi_4) using a [rtl-sdr](https://www.rtl-sdr.com/buy-rtl-sdr-dvb-t-dongles/) USB dongle at discover all the active radio frequencies near you.  

Why would you need to discover active radio frequencies for yourself?  Spectrum usage changes frequently, published scanner guides are grow stale or the scanner websites are not well curated.  Using a tool like mellow-mastodon enables you to focus on radio frequencies that are active and you can actually hear.  

Some users might find the historical spectrum use interesting as well.  To capture history takes a more work to introduce a database.  I will start simple w/collection on a single rPi and then work up to multiple collectors writing to [AWS S3](https://en.wikipedia.org/wiki/Amazon_S3) and then loading into [PostgreSQL](https://www.postgresql.org/) for analysis.  Collecting samples over time allows discovery of frequencies in active use, which can be revisted with other applications for further analysis or simply logged for continuity.

## Single Collector Operation
To use mellow mastodon in the simplest use case, you will need a a [Raspberry Pi](https://www.raspberrypi.org/) connected to a [rtl-sdr](https://osmocom.org/projects/rtl-sdr/wiki/rtl-sdr).

After acquiring the hardware, you need the rtl_power(1) utility from the [rtl-sdr](https://github.com/osmocom/rtl-sdr) library.  I always build my rtl-sdr from scratch, but there is a debian package ("rtl-sdr") which might work for you.  When everything works, you can invoke "rtl_test -t" (need example).

Create directories to hold the output, i.e. /var/mellow/mastodon/fresh

At this point, you can invoke the rtl-power(1) utility.  The [big-search01.sh](https://github.com/guycole/mellow-mastodon/blob/main/bin/big-search01.sh) provides an example.  Note that big-search01 will write to /var/mellow/mastodon/fresh or update the script to suit your own designs.

big-search01 runs for 5 minutes and produces a comma separate values [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) file suitable for import into a spreadsheet.  Here is [simple example](https://github.com/guycole/mellow-mastodon/blob/main/test/8e778934-5283-4d3e-9641-ccd8b33893c1.csv) of a rtl-power(1) output file.  

Here is another example of a sample energy plot w/a loud emitter at 169.55 MHz.
![sample plot](https://github.com/guycole/mellow-mastodon/blob/main/test/1757222705-168328650.png).  You can see there are other emitters in the plot (note the peaks on the left and right sides).  In this graph, frequency is the x axis and power is the y axis.

rtl_power(1) will scan a range of spectrum (sliced into bins) and produce a value (for the bin) based upon observed signal strength.  big-search01 writes the signal strength value every minute.  Note that even a very strong, but brief emitter might have a low value because the bin was not active the entire period.  Also note that bin frequency is not the actual frequency you would use on your scanner.  bin is a bucket, so a signal might span multiple buckets or be within a single bucket depending on the emitter.

Another mechanism to discover stations is to use the csv2json.sh utility which reads CSV files and produces a JSON list of peakers which represent stations.  I prefer the output of csv2json because the files are more compact.  [Here](https://github.com/guycole/mellow-mastodon/blob/main/test/big-search01-1758588787-anderson1.json) is a sample csv2json output file.

Create directories to hold the csv2json output, i.e. /var/mellow/mastodon/processed, peaker, cooked.  csv2json can be configured via [config.yaml](https://github.com/guycole/mellow-mastodon/blob/main/src/collector/config.example).  The "cooked" direcctory will contain a json file which has all the rtl-power(1) values, and a gnuplot file in case you want to graph the output.  Use [gp_gen.sh](https://github.com/guycole/mellow-mastodon/blob/main/bin/gp_gen.sh) as an example with gnuplot(1).

## Multiple Collector Operation

You can run multiple instances of mastodon collectors to feed a single back end.  By invoking from cron(1) the collection and load cycles can be automated.

See [wombat01-to-s3.sh](https://github.com/guycole/mellow-mastodon/blob/main/bin/wombat01-to-s3.sh) for an example of writing a file to AWS S3.  [fresh-from-s3.sh](https://github.com/guycole/mellow-mastodon/blob/main/bin/fresh-from-s3.sh) reads from S3 and [loader.sh](https://github.com/guycole/mellow-mastodon/blob/main/bin/loader.sh) reads the file into postgresql.

## Artifacts
Samples of mastodon files
- [rtl_power CSV file (truncated)](https://github.com/guycole/mellow-mastodon/blob/main/test/8e778934-5283-4d3e-9641-ccd8b33893c1.csv)
- [rtl_power CSV file (full)](https://github.com/guycole/mellow-mastodon/blob/main/test/fresh.tgz)
- [mastodon csv2json row file](https://github.com/guycole/mellow-mastodon/blob/main/test/1757222705-162733800.json)
- [mastodon csv2json gnuplot data file](https://github.com/guycole/mellow-mastodon/blob/main/test/1757222705-162733800.gp)
- [mastodon csv2json gnuplot png file](https://github.com/guycole/mellow-mastodon/blob/main/test/1757222705-162733800.png)
- [mastodon peakers only file](https://github.com/guycole/mellow-mastodon/blob/main/test/big-search01-1757201231-anderson1.json)
- [mastodon database dump of population table](https://github.com/guycole/mellow-mastodon/blob/main/test/peakers-2025-09-06.txt)

## History
Mastodon replaces the obsolete [Mellow Elephant](https://github.com/guycole/mellow-elephant)

| Date       | Site      | Equipment | Note                |
| ---------- | --------- | --------- | ------------------- |
| 2025-09-01 | anderson1 | wombat01  | collection active   |
| 2025-09-02 | vallejo1  | wombat04  | collection active   |
| 2025-09-05 |           | wombat03  | database load cycle |

## rtl_power doc
```
rtl_power -help
rtl_power, a simple FFT logger for RTL2832 based DVB-T receivers

Use:	rtl_power -f freq_range [-options] [filename]
	-f lower:upper:bin_size [Hz]
	 (bin size is a maximum, smaller more convenient bins
	  will be used.  valid range 1Hz - 2.8MHz)
	[-i integration_interval (default: 10 seconds)]
	 (buggy if a full sweep takes longer than the interval)
	[-1 enables single-shot mode (default: off)]
	[-e exit_timer (default: off/0)]
	[-d device_index or serial (default: 0)]
	[-g tuner_gain (default: automatic)]
	[-p ppm_error (default: 0)]
	[-T enable bias-T on GPIO PIN 0 (works for rtl-sdr.com v3 dongles)]
	filename (a '-' dumps samples to stdout)
	 (omitting the filename also uses stdout)

Experimental options:
	[-w window (default: rectangle)]
	 (hamming, blackman, blackman-harris, hann-poisson, bartlett, youssef)
	[-c crop_percent (default: 0%, recommended: 20%-50%)]
	 (discards data at the edges, 100% discards everything)
	 (has no effect for bins larger than 1MHz)
	[-F fir_size (default: disabled)]
	 (enables low-leakage downsample filter,
	  fir_size can be 0 or 9.  0 has bad roll off,
	  try with '-c 50%')
	[-P enables peak hold (default: off)]
	[-D enable direct sampling (default: off)]
	[-O enable offset tuning (default: off)]

CSV FFT output columns:
	date, time, Hz low, Hz high, Hz step, samples, dbm, dbm, ...

Examples:
	rtl_power -f 88M:108M:125k fm_stations.csv
	 (creates 160 bins across the FM band,
	  individual stations should be visible)
	rtl_power -f 100M:1G:1M -i 5m -1 survey.csv
	 (a five minute low res scan of nearly everything)
	rtl_power -f ... -i 15m -1 log.csv
	 (integrate for 15 minutes and exit afterwards)
	rtl_power -f ... -e 1h | gzip > log.csv.gz
	 (collect data for one hour and compress it on the fly)

Convert CSV to a waterfall graphic with:
	 http://kmkeen.com/tmp/heatmap.py.txt 
```
