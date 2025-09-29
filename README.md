mellow-mastodon
===============

Hello, [radio scanner](https://en.wikipedia.org/wiki/Radio_scanner) enthusiast.  Welcom to mellow-mastodon, an application which can handily operate on a [raspberry pi 4](https://en.wikipedia.org/wiki/Raspberry_Pi_4) using a [rtl-sdr](https://www.rtl-sdr.com/buy-rtl-sdr-dvb-t-dongles/) USB dongle at discover active radio frequencies near you.  

Why would you need to discover active radio frequencies for yourself?  Spectrum usage changes frequently, published scanner guides are grow stale or the scanner websites are not well curated.  Using a tool like mellow-mastodon enables you to focus your attention on radio frequencies that are active and you can actually hear.  

Some users might find the historical spectrum use interesting as well.  Long term historical results require a database for storage and analysis.  You might also want the results from multiple collection sites.  More about these topics later.

I will start simple w/single collector on a single rPi and then work up to multiple collectors writing to [AWS S3](https://en.wikipedia.org/wiki/Amazon_S3) and then loading into [PostgreSQL](https://www.postgresql.org/) for analysis.  Collecting samples over time allows discovery of seasonal usage, which can be revisted with other applications for further analysis or simply logged for continuity.

## Single Collector Operation
To use mellow mastodon in the simplest use case, you will need a a [Raspberry Pi](https://www.raspberrypi.org/) connected to a [rtl-sdr](https://osmocom.org/projects/rtl-sdr/wiki/rtl-sdr).

After acquiring the hardware, you need the rtl_power(1) utility from the [rtl-sdr](https://github.com/osmocom/rtl-sdr) library.  I always build my rtl-sdr from scratch, but there is a debian package ("rtl-sdr") which might work for you.  When everything works, you can invoke "rtl_test -t"
```
gsc@rpi4n:2012>rtl_test -t
Found 1 device(s):
  0:  Realtek, RTL2838UHIDIR, SN: 00000001

Using device 0: Generic RTL2832U OEM
Found Rafael Micro R820T tuner
Supported gain values (29): 0.0 0.9 1.4 2.7 3.7 7.7 8.7 12.5 14.4 15.7 16.6 19.7 20.7 22.9 25.4 28.0 29.7 32.8 33.8 36.4 37.2 38.6 40.2 42.1 43.4 43.9 44.5 48.0 49.6 
[R82XX] PLL not locked!
Sampling at 2048000 S/s.
No E4000 tuner found, aborting.
```

The [big-search01.sh](https://github.com/guycole/mellow-mastodon/blob/main/bin/big-search01.sh) provides an example of using thertl_power(1) to collect samples.  Note that big-search01 will write to /var/mellow/mastodon/fresh or update the script to suit your own designs.

big-search01 runs for 5 minutes and produces a comma separate values [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) file suitable for import into a spreadsheet.  Here is [simple example](https://github.com/guycole/mellow-mastodon/blob/main/test/8e778934-5283-4d3e-9641-ccd8b33893c1.csv) of a rtl-power(1) output file.  

Here is another example of a sample energy plot w/a loud emitter at 169.55 MHz.
![sample plot](https://github.com/guycole/mellow-mastodon/blob/main/test/1757222705-168328650.png).  You can see there are other emitters in the plot (note the peaks on the left and right sides).  In this graph, frequency is the x axis and power is the y axis.

rtl_power(1) will scan a range of spectrum (sliced into bins) and produce a value (for the bin) based upon observed signal strength.  big-search01 writes a energy value every minute.  Note that even a very strong, but brief emitter might have a low value because the bin was not active the entire period.  Also note that bin frequency is not the actual frequency you would use on your scanner.  bin is a bucket, so a signal might span multiple buckets or be within a single bucket depending on the emitter.

Once you have a CSV file of energy observations, you can now look for active emitters.  One mechanism would be to read the CSV file into a spreadsheet application like [Google Sheets](https://docs.google.com/spreadsheets).  Another route is to use the [csv2json.sh](https://github.com/guycole/mellow-mastodon/blob/main/bin/csv2json.sh) application for discovery.

[csv2json.sh](https://github.com/guycole/mellow-mastodon/blob/main/bin/csv2json.sh) is a utility which reads CSV files and produces a JSON list of peakers which represent stations.  I prefer the output of csv2json because the files are more compact compared to CSV output.  [Here](https://github.com/guycole/mellow-mastodon/blob/main/test/big-search01-1758588787-anderson1.json) is a sample csv2json output file.

To recap:
1. rtl_power(1) utility samples spectrum, [big-search01.sh](https://github.com/guycole/mellow-mastodon/blob/main/bin/big-search01.sh) is an example.
1. rtl_power(1) produces a CSV file which you can read as a spreadsheet
1. [csv2json.sh](https://github.com/guycole/mellow-mastodon/blob/main/bin/csv2json.sh) reads the CSV file and produces files usch as: 
    1. a JSON file containing the raw CSV values for that row
	1. a gnuplot data file from that row
	1. a consolidated peaker file, which contains bins w/energy levels above a specified threshold

Using these output files, you are ready to verify using a regular scanner or another RTL-SDR based application.

## Single Collector Installation
Create directories to hold the output, I consolidate these into "/var/mellow/mastodon" such as
1. /var/mellow/mastodon/archive (xxx)
1. /var/mellow/mastodon/cooked (output from csv2json.py)
1. /var/mellow/mastodon/export (collected peaker files for AWS S3)
1. /var/mellow/mastodon/fresh (CSV files collected from rtl_power to be parsed)
1. /var/mellow/mastodon/peaker (json list of collected energy peaks)
1. /var/mellow/mastodon/process (parsed CSV files from rtl_power)




Another mechanism to discover stations is to use 
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
