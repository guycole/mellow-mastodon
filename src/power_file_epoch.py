#
# Title: power_file_epoch.py
# Description:
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#
import csv
import datetime
import os
import sys

from power_file_row import PowerFileRow


class PowerFileEpoch:
    def __init__(self, epoch_time: int):
        self.time_stamp_epoch = epoch_time
        self.pfr_map = {}

    def __str__(self):
        return f"{self.time_stamp_epoch}"

    def add_sample(self, pfr: PowerFileRow) -> None:
        """add a sample for this epoch time"""

        if (self.time_stamp_epoch != pfr.meta_map["time_stamp_epoch"]):  # all samples share same epoch time
            raise Exception(
                f"epoch time mismatch {self.time_stamp_epoch} {pfr.meta_map['time_stamp_epoch']}"
            )
        
        self.pfr_map[pfr.meta_map["freq_low_hz"]] = pfr

    def peakers(
        self, half_window_size: int, cooked_dir: str
    ) -> list[tuple[int, float, float]]:
        """ return list of all rows this epoch """

        peaker_list = []

        # collect all peakers into single list sorted by frequency
        sorted_keys = sorted(self.pfr_map.keys())
        for key in sorted_keys:
            # print(f"  key {key} {self.pfr_map[key]}")
            self.pfr_map[key].moving_window(half_window_size) # compute moving window
            self.pfr_map[key].json_writer(cooked_dir) # write all values for row
            self.pfr_map[key].gnuplot_writer(cooked_dir) 

            peaker_list.extend(self.pfr_map[key].peakers()) # collect all peakers
            # print(f" peakers {len(peaker_list)}")

        return peaker_list


# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
