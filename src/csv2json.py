#
# Title: csv2json.py
# Description: convert mastodon csv to json dictionary
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#

import csv
import datetime
import json
import os
import sys
import time

from unittest import result
import uuid

import yaml
from yaml.loader import SafeLoader

from power_file_helper import PowerFileHelper
from power_file_row import PowerFileRow

from power_file import PowerFile

class CsvJson:
    half_window_size = 33

    def __init__(self, configuration: dict[str, str]):
        self.cooked_dir = configuration["cookedDir"]
        self.fresh_dir = configuration["freshDir"]
        self.peaker_dir = configuration["peakerDir"]
        self.processed_dir = configuration["processedDir"]

        self.antenna = configuration["antenna"]
        self.project = configuration["project"]
        self.receiver = configuration["receiver"]
        self.site = configuration["site"]

        self.peaker_algorithm = configuration["peakerAlgorithm"]
        self.peaker_threshold = configuration["peakerThreshold"]

    def execute(self) -> None:
        print(f"fresh dir:{self.fresh_dir}")
        os.chdir(self.fresh_dir)

        targets = os.listdir(".")
        print(f"{len(targets)} files noted")

        pf_args = {
            "antenna": self.antenna,
            "peaker_algorithm": self.peaker_algorithm,
            "peaker_threshold": self.peaker_threshold,
            "project": self.project,
            "receiver": self.receiver,
            "site": self.site,
        }

        for target in targets:
            print(f"processing {target}")

            if os.path.isfile(target) is False:
                print(f"skipping {target}")
                continue

            if target.endswith(".csv") is False:
                print(f"skipping {target}")
                continue

            if target == "8e778934-5283-4d3e-9641-ccd8b33893c1.csv":
                print("skipping test file")
                continue

            power_file = PowerFile(pf_args)
            power_epoch_map = power_file.parser(target, self.half_window_size)
            for key in power_epoch_map.keys():
                power_epoch_map[key].write_gnuplot_and_json(self.cooked_dir)

                if self.peaker_algorithm == 1:
                    power_epoch_map[key].peakers_1()
                    power_epoch_map[key].write_peakers(self.peaker_dir)
                else:
                    print(f"unknown peaker algorithm {self.peaker_algorithm}")

#            os.rename(target, self.processed_dir + "/" + target)

print("start csv2json")

#
# argv[1] = configuration filename
#
if __name__ == "__main__":
    if len(sys.argv) > 1:
        config_name = sys.argv[1]
    else:
        config_name = "config.yaml"

    configuration = {}
    with open(config_name, "r", encoding="utf-8") as in_file:
        try:
            configuration = yaml.load(in_file, Loader=SafeLoader)
        except yaml.YAMLError as error:
            print(error)

    csv2json = CsvJson(configuration)
    csv2json.execute()

print("stop csv2json")

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
