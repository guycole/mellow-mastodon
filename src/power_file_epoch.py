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

    def __init__(self, epoch_time: int):
        self.epoch_time = epoch_time

        self.pfe_pfr_map = {} # all rows w/freq_low_hz key

    def __str__(self):
        return f"{self.epoch_time}"

    def add_sample(self, pfr: PowerFileRow) -> None:
        """add a sample for this epoch time"""

        if (self.epoch_time != pfr.pfr_meta_map["time_stamp_epoch"]):
            # all samples share same epoch time
            raise Exception(f"epoch time mismatch {self.epoch_time} {pfr.meta_map['time_stamp_epoch']}")

        self.pfe_pfr_map[pfr.pfr_meta_map["freq_low_hz"]] = pfr

    def write_gnuplot_and_json(self, pf_args: dict[str, any]) -> None:
        for key in self.pfe_pfr_map.keys():
            #print(f"  key {key} {self.pfe_pfr_map[key]}")
            self.pfe_pfr_map[key].json_writer(pf_args)
            self.pfe_pfr_map[key].gnuplot_writer(pf_args['cooked_dir'])

    def write_peakers(self, pf_args: dict[str, any]) -> None:
        file_name = f"{pf_args['peaker_dir']}/{pf_args['project']}-{self.epoch_time}-{pf_args['site']}.json"

        self.json_meta_map = {
            "antenna": pf_args["antenna"],
            "application": pf_args["application"],
            "peakerAlgorithm": pf_args['peaker_algorithm'],
            "peakerThreshold": pf_args['peaker_threshold'],
            "project": pf_args["project"],
            "receiver": pf_args["receiver"],
            "site": pf_args["site"],
            "sourceFile": pf_args["source_file"],
            "schemaVersion": 1,
            "timeStampEpoch": self.epoch_time,
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
        sorted_keys = sorted(self.pfe_pfr_map.keys())
        for key in sorted_keys:
            self.peaker_list.extend(self.pfe_pfr_map[key].peakers_1())

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
