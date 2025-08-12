#
# Title: domain.py
# Description: mastodon domain classes
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#
import csv
import datetime
import os
import sys

class MastodonRow:
    header = {}

    def __init__(self, file_name: str):
        # file name has form project-uuid.site 
        # big-search-d25fbdd2-4445-4d4c-bebc-bbbb4d4122d8.vallejo1

        tokens = file_name.split(".")
        if len(tokens) != 2:
            raise Exception("bad token len")

        min_size = len("-d25fbdd2-4445-4d4c-bebc-bbbb4d4122d8")
        if len(tokens[0]) < min_size:
            raise Exception("bad token 0 len") 

        self.header = {
            "file_name": file_name,
            "file_type": "mastodon_v1",
            "project": tokens[0][:-37],
            "site": tokens[1],
            "meta": {},
            "samples": [],
            "statistics": {}
        }

    def __str__(self):
        return f"self.header = {self.header['file_name']}"
    
    def row_energy(self) -> None:
        print(self.header)

    def row_meta(self, row: list[str]) -> None:
        # ['2025-05-16', ' 04:16:20', ' 966482608', ' 969275710', ' 2727.64']
        # "\tdate, time, Hz low, Hz high, Hz step, samples, dbm, dbm, ...

        if len(row) < 6:
            raise Exception("bad row len")

        row_date = row[0].split('-')
        yy = int(row_date[0])
        mm = int(row_date[1])
        dd = int(row_date[2])

        row_time = row[1].split(':')
        hour = int(row_time[0])
        minute = int(row_time[1])
        second = int(row_time[2])

        self.header['meta'] = {
            "freq_low_hz": int(row[2]),
            "freq_high_hz": int(row[3]),
            "freq_step_hz": float(row[4]),
            "sample_quantity": int(row[5]),
            "time_stamp_dt": datetime.datetime(yy, mm, dd, hour, minute, second),
            "time_stamp_epoch": int(datetime.datetime(yy, mm, dd, hour, minute, second).timestamp()),
            "time_stamp_iso8601": datetime.datetime(yy, mm, dd, hour, minute, second).isoformat()
        }

    def row_samples(self, row: list[str]) -> None:
        # dbm values

        if len(row) < 6:
            raise Exception("bad row len")

        samples = []
        current_frequency = self.header['meta']['freq_low_hz']
        step_frequency = self.header['meta']['freq_step_hz']

        avg_sample = 0
        min_sample = 0
        max_sample = -100
        total_samples = 0

        for ndx in range(6, len(row)):
            bin_value = float(row[ndx])
            samples.append((current_frequency, bin_value))

            current_frequency += step_frequency

            total_samples += bin_value

            if bin_value < min_sample:
                min_sample = bin_value

            if max_sample < bin_value:
                max_sample = bin_value

        avg_sample = total_samples / len(samples)

        self.header['samples'] = samples
        self.header['statistics'] = {
            "avg_sample": avg_sample,
            "min_sample": min_sample,
            "max_sample": max_sample
        }

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
