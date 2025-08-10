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
import uuid

import yaml
from yaml.loader import SafeLoader

class CsvJson:

    def __init__(self, configuration: dict[str, str]):
        self.archive_dir = configuration["archiveDir"]
        self.cooked_dir = configuration["cookedDir"]
        self.failure_dir = configuration["failureDir"]
        self.fresh_dir = configuration["freshDir"]

    def parse_file_name(self, file_name: str) -> dict[str, any]:
        # file name has form project-uuid.site #
        # big-search-d25fbdd2-4445-4d4c-bebc-bbbb4d4122d8.vallejo1

        tokens = file_name.split(".")
        if len(tokens) != 2:
            print("skipping bad file name")
            return {}

        return {
            "file_name": file_name,
            "project": tokens[0][:-37],
            "site": tokens[1],
            "meta": {}           
        }
 
    def parse_row_meta(self, row: list[str]) -> dict[str, any]:
        # ['2025-05-16', ' 04:16:20', ' 966482608', ' 969275710', ' 2727.64']
        # "\tdate, time, Hz low, Hz high, Hz step, samples, dbm, dbm, ...

        row_date = row[0].split('-')
        yy = int(row_date[0])
        mm = int(row_date[1])
        dd = int(row_date[2])

        row_time = row[1].split(':')
        hour = int(row_time[0])
        minute = int(row_time[1])
        second = int(row_time[2])

        results = {
            "freq_low": int(row[2]),
            "freq_high": int(row[3]),
            "freq_step": float(row[4]),
            "sample_quantity": int(row[5]),
            "time_stamp": datetime.datetime(yy, mm, dd, hour, minute, second),
            "bin_samples": []
        }

        return results

    def parse_samples(self, row: list[str]) -> list[float]:
        results = []

        for ndx in range(6, len(row)):
            results.append(float(row[ndx]))

        return results

    def json_writer(self, payload:dict[str, any]) -> None:
        bin_seconds = int(payload["meta"]["time_stamp"].timestamp())
        freq_low = payload["meta"]["freq_low"]
        project = payload["project"]
        site = payload["site"]

        file_name = f"{self.cooked_dir}/{bin_seconds}-{freq_low}-{project}.{site}"
        print(file_name)

        # datetime is not json serializable
        payload["meta"]["time_stamp"] = bin_seconds

        try:
            with open(file_name, "w") as out_file:
                json.dump(payload, out_file, indent=4)
        except Exception as error:
            print(error)

    def csv_file_converter(self, file_name: str) -> bool:
        try:
            with open(file_name, "r") as in_file:
                csv_file = csv.reader(in_file)
                
                for row in csv_file:
                    result = self.parse_file_name(file_name)
                    if len(result) < 1:
                        print(f"skipping bad file name {file_name}")
                    else:
                        result["meta"] = self.parse_row_meta(row[0:6])
                        result["meta"]["bin_samples"] = self.parse_samples(row)
                        self.json_writer(result)
        except Exception as error:
            print(error)
            return False

        return True

    def execute(self) -> None:
        print(f"fresh dir:{self.fresh_dir}")
        os.chdir(self.fresh_dir)
        
        targets = os.listdir(".")
        print(f"{len(targets)} files noted")

        for target in targets:
            print(f"processing {target}")
            
            if os.path.isfile(target) is True:
                retflag = self.csv_file_converter(target)
            else:
                print(f"skipping {target}")
                continue


print("start csv2json")

#
# argv[1] = configuration filename
#
if __name__ == "__main__":
    if len(sys.argv) > 1:
        config_name = sys.argv[1]
    else:
        config_name = "config.yaml"

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
