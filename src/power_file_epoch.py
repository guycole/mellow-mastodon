#
# Title: power_file_epoch.py
# Description:
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#
import csv
import datetime
import json
import os
import sys

from power_file_row import PowerFileRow

class PowerFileEpoch:
    def __init__(self, epoch_time: int, meta_map: dict[str, any]):
        self.epoch_time = epoch_time
        self.meta_map = meta_map
        self.meta_map["epoch_time"] = epoch_time

        self.pfr_map = {}

    def __str__(self):
        return f"{self.epoch_time}"

    def add_sample(self, pfr: PowerFileRow) -> None:
        """add a sample for this epoch time"""

        if (self.epoch_time != pfr.meta_map["time_stamp_epoch"]):
            # all samples share same epoch time
            raise Exception(f"epoch time mismatch {self.epoch_time} {pfr.meta_map['time_stamp_epoch']}")

        self.pfr_map[pfr.meta_map["freq_low_hz"]] = pfr

    def write_gnuplot_and_json(self, cooked_dir:str) -> None:
        for key in self.pfr_map.keys():
            #print(f"  key {key} {self.pfr_map[key]}")
            self.pfr_map[key].json_writer(cooked_dir)
            self.pfr_map[key].gnuplot_writer(cooked_dir)

    def write_peakers(self, peaker_dir: str) -> None:
        file_name = f"{peaker_dir}/{self.meta_map['project']}-{self.meta_map['epoch_time']}-{self.meta_map['site']}.json"
        print(file_name)

        self.json_meta_map = {
            "antenna": self.meta_map["antenna"],
            "peakerAlgorithm": self.meta_map["peaker_algorithm"],
            "peakerThreshold": self.meta_map["peaker_threshold"],
            "project": self.meta_map["project"],
            "receiver": self.meta_map["receiver"],
            "site": self.meta_map["site"],
            "schemaVersion": 1,
            "timeStampEpoch": self.meta_map["epoch_time"],
        }

        payload = {
            "meta": self.json_meta_map,
            "peakers": self.peaker_list,
        }

        try:
            with open(file_name, "w") as out_file:
                json.dump(payload, out_file, indent=4)
        except Exception as error:
            print(error)

    def peakers_1(self) -> None:
        self.peaker_list = []

        # collect all peakers into single list sorted by frequency
        sorted_keys = sorted(self.pfr_map.keys())
        for key in sorted_keys:
            print(f"  key {key} {self.pfr_map[key]}")
            self.peaker_list.extend(self.pfr_map[key].peakers_1())

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
