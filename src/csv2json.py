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

    def json_writer(self, payload: MastodonRow) -> None: 
        bin_seconds = payload.header['meta']['time_stamp_epoch']
        freq_low_hz = payload.header['meta']['freq_low_hz']        
        project = payload.header['project']
        site = payload.header['site']

        file_name = f"{self.cooked_dir}/{bin_seconds}-{freq_low_hz}-{project}.{site}"
      
        del(payload.header['meta']['time_stamp_dt']) # datetime is not json serializable

        try:
            with open(file_name, "w") as out_file:
                json.dump(payload.header, out_file, indent=4)
        except Exception as error:
            print(error)

    def csv_file_converter(self, file_name: str) -> None:
        helper = MastodonHelper()
        buffer = helper.csv_file_reader(file_name)

        file_name = "big-search-fc4cc836-b05b-4725-b07b-632afbc47d52.anderson1"

        for current in buffer:
            row = MastodonRow(file_name)
            row.row_meta(current[0:6])
            row.row_samples(current)
            self.json_writer(row)

    def execute(self) -> None:
        print(f"fresh dir:{self.fresh_dir}")
        os.chdir(self.fresh_dir)
        os.chdir("/Users/gsc/Documents/github/mellow-mastodon/test")
        
        targets = os.listdir(".")
        print(f"{len(targets)} files noted")
        self.csv_file_converter("testaroo")

print("start csv2json")#

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
