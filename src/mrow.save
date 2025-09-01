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
    json_bag = {}

    def __init__(self, file_name: str, personality: dict[str, any]):
        self.json_bag = {
            "antenna": personality["antenna"],
            "file_name": file_name,
            "file_type": "mastodon-v1",
            "host_name": personality["host"],
            "project": personality["project"],
            "receiver": personality["receiver"],
            "site": personality["site"],
            "meta": {},
            "samples": [],
            "statistics": {}
        }

    def __str__(self):
        return f"self.json_bag = {self.json_bag['file_name']}"
    
    def row_energy(self) -> None:
        print(self.json_bag)

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

        dt = datetime.datetime(yy, mm, dd, hour, minute, second)

        self.json_bag['meta'] = {
            "freq_low_hz": int(row[2]),
            "freq_high_hz": int(row[3]),
            "freq_step_hz": float(row[4]),
            "sample_quantity": int(row[5]),
            "time_stamp_dt": dt,
            "time_stamp_epoch": int(dt.timestamp()),
            "time_stamp_iso8601": dt.isoformat()
        }

    def row_samples(self, row: list[str]) -> None:
        # dbm values and peakers

        if len(row) < 6:
            raise Exception("bad row len")
        
        # pass1 convert from string to float and discover basic row stats

        avg_sample = 0
        min_sample = 0
        max_sample = -100
        total_samples = 0

        pass1_samples = []

        for ndx in range(6, len(row)): # start at 6 to skip row metadata
            current_value = float(row[ndx])
            pass1_samples.append(current_value)
            
            total_samples += current_value

            if current_value < min_sample:
                min_sample = current_value

            if max_sample < current_value:
                max_sample = current_value

        avg_sample = total_samples / len(pass1_samples)

        self.json_bag['statistics'] = {
            "avg_sample": avg_sample,
            "min_sample": min_sample,
            "max_sample": max_sample
        }

        # pass2 discover peakers by walking a window through the sample array
        # highest value within the window is local maxima (peaker)

        pass2_samples = []
        current_frequency = self.json_bag['meta']['freq_low_hz']
        step_frequency = self.json_bag['meta']['freq_step_hz']
        window_edge = 33

        for ndx in range(len(pass1_samples)):
            current_value = pass1_samples[ndx]

            left_ndx = ndx - window_edge
            right_ndx = ndx + window_edge + 1

            if left_ndx < 0:
                left_ndx = 0
            
            if right_ndx >= len(pass1_samples):
                right_ndx = len(pass1_samples) - 1

            mean = sum(pass1_samples[left_ndx:right_ndx])/(right_ndx - left_ndx)
            if mean > current_value:
                peaker_flag = False
            else:
                local_maxima = max(pass1_samples[left_ndx:right_ndx])
                if local_maxima == current_value:
                    peaker_flag = True
                else:
                    peaker_flag = False

            pass2_samples.append((int(current_frequency), current_value, mean, peaker_flag))

            current_frequency += step_frequency

        self.json_bag['samples'] = pass2_samples

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
