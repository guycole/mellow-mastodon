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
        self.archive_dir = configuration["archiveDir"]
        self.cooked_dir = configuration["cookedDir"]
        self.fresh_dir = configuration["freshDir"]
        self.processed_dir = configuration["processedDir"]

        self.antenna = configuration["antenna"]
        self.project = configuration["project"]
        self.receiver = configuration["receiver"]
        self.site = configuration["site"]

    def execute(self) -> None:
        print(f"fresh dir:{self.fresh_dir}")
        os.chdir(self.fresh_dir)

        targets = os.listdir(".")
        print(f"{len(targets)} files noted")

        for target in targets:
            print(f"processing {target}")

            if os.path.isfile(target) is False:
                print(f"skipping {target}")
                continue

            if target.endswith(".csv") is False:
                print(f"skipping {target}")
                continue

            power_file = PowerFile(self.antenna, self.project, self.receiver, self.site)
            power_epoch_map = power_file.parser(target)
            for key in power_epoch_map.keys():
                # peakers by epoch time sorted by frequency
                peaker_list = power_epoch_map[key].peakers(self.half_window_size, self.cooked_dir)
                power_file.json_writer(key, self.archive_dir, peaker_list)

            os.rename(target, self.processed_dir + "/" + target)

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
