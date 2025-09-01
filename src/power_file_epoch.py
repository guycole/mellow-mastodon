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
        self.pfr_map = {}

        self.meta_map = {
            "freq_low_hz": None,
            "freq_high_hz": None,
            "freq_step_hz": None,
            "time_stamp_epoch": epoch_time,
        }

    def __str__(self):
        return f"{self.meta_map['time_stamp_epoch']} {self.meta_map['freq_low_hz']} {self.meta_map['freq_high_hz']}"

    def add_sample(self, pfr: PowerFileRow) -> None:
        """add a sample for this epoch time"""

        epoch_key = self.meta_map["time_stamp_epoch"]
        if (
            epoch_key != pfr.meta_map["time_stamp_epoch"]
        ):  # all samples share same epoch time
            raise Exception(
                f"epoch time mismatch {epoch_key} {pfr.meta_map['time_stamp_epoch']}"
            )

        self.pfr_map[pfr.meta_map["freq_low_hz"]] = pfr

    def peakers(
        self, half_window_size: int, dirname: str
    ) -> list[tuple[int, float, float]]:
        peaker_list = []

        # collect all peakers into single list
        sorted_keys = sorted(self.pfr_map.keys())
        for key in sorted_keys:
            # print(f"  key {key} {self.pfr_map[key]}")
            self.pfr_map[key].moving_window(half_window_size)
            self.pfr_map[key].json_writer(dirname)
            self.pfr_map[key].gnuplot_writer(dirname)

            peaker_list.extend(self.pfr_map[key].peakers())
            # print(f" peakers {len(peaker_list)}")

        return peaker_list


# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
