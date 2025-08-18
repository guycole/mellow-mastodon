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

from mastodon_helper import MastodonHelper
from mastodon_row import MastodonRow

class CsvJson:

    def __init__(self, configuration: dict[str, str]):
        self.archive_dir = configuration["archiveDir"]
        self.cooked_dir = configuration["cookedDir"]
        self.failure_dir = configuration["failureDir"]
        self.fresh_dir = configuration["freshDir"]
        self.raw_dir = configuration["rawDir"]

    def file_name(self, payload: MastodonRow) -> str:
        bin_seconds = payload.json_bag['meta']['time_stamp_epoch']
        freq_low_hz = payload.json_bag['meta']['freq_low_hz']        
        project = payload.json_bag['project']
        site = payload.json_bag['site']

        return f"{self.fresh_dir}/{bin_seconds}-{freq_low_hz}-{project}.{site}"

    def json_writer(self, payload: MastodonRow) -> None:
        file_name = f"{self.file_name(payload)}.json"

        del(payload.json_bag['meta']['time_stamp_dt']) # datetime is not json serializable

        try:
            with open(file_name, "w") as out_file:
                json.dump(payload.json_bag, out_file, indent=4)
        except Exception as error:
            print(error)

    # plot for [col=2:3] '1754987499-123569850-big-search.anderson1.gp' using 1:col
    def gnuplot_writer(self, payload: MastodonRow) -> None:
        file_name = f"{self.file_name(payload)}.gp"

        try:
            with open(file_name, "w") as out_file:
                for current in payload.json_bag['samples']:
                    out_file.write(f"{current[0]}\t{current[1]}\t{current[2]}\n")
        except Exception as error:
            print(error)

    def csv_file_converter(self, file_name: str) -> None:
        helper = MastodonHelper()
        buffer = helper.csv_file_reader(file_name)

        for current in buffer:
            row = MastodonRow(file_name)
            row.row_meta(current[0:6])
            row.row_samples(current)
            self.gnuplot_writer(row)
            self.json_writer(row)

    def execute(self) -> None:
        print(f"raw dir:{self.raw_dir}")
        os.chdir(self.raw_dir)

        targets = os.listdir(".")
        print(f"{len(targets)} files noted")

        for target in targets:
            print(f"processing {target}")
            
            if os.path.isfile(target) is False:
                print(f"skipping {target}")
                continue

            self.csv_file_converter(target)

            os.rename(target, self.cooked_dir + "/" + target)

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
