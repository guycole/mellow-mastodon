mellow-mastodon
===============

RF Energy Survey using the rtl_power(1) utility from the [rtl-sdr](https://github.com/osmocom/rtl-sdr) library.  

rtl_power(1) will scan a range of spectrum (sliced into bins) and produce a value (for the bin) based upon observed signal strength.  I redirect this to a file which is eventually loaded into postgres.

Collecting samples over time allows discovery of frequencies in active use.

Collection scripts reside in bin, database loader in src.

Mastodon replaces the obsolete [Mellow Elephant](https://github.com/guycole/mellow-elephant)

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
