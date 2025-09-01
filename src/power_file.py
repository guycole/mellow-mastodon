#
# Title: power_file.py
# Description: process a rtl_power CSV file
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#
import json

from power_file_epoch import PowerFileEpoch
from power_file_helper import PowerFileHelper
from power_file_row import PowerFileRow

class PowerFile:
    half_window_size = 33

    def __init__(self, antenna: str, project: str, receiver: str, site: str):
      
        self.meta_map = {
            "antenna": antenna,
            "file_type": "mastodon-v1",
            "project": project,
            "receiver": receiver,
            "site": site,
            "time_stamp_epoch": 0
        }

    def __str__(self):
        return f"PowerFile: {self.meta_map['time_stamp_epoch']}"

    def json_writer(self, fresh_dir: str, peakers_list: list[tuple [int, float, float]]) -> None:
        file_name = f"{fresh_dir}/{self.meta_map['project']}-{self.meta_map['time_stamp_epoch']}-{self.meta_map['site']}.json"
        print(file_name)

        payload = {
            "meta": self.meta_map,
            "peakers": peakers_list
        }

        try:
            with open(file_name, "w") as out_file:
                json.dump(payload, out_file, indent=4)
        except Exception as error:
            print(error)

    def peakers(self, pem: dict[int, PowerFileEpoch], dirname: str) -> None:
        """ write file for each epoch time """
        for key in pem.keys():
            self.meta_map['time_stamp_epoch'] = key
            peaker_list = pem[key].peakers(self.half_window_size, dirname)
            self.json_writer(dirname, peaker_list)

    def parser(self, file_name:str) -> dict[int, PowerFileEpoch]:
        """read csv file and convert each row"""

        # read all rows of csv file
        helper = PowerFileHelper()
        raw_buffer = helper.csv_file_reader(file_name)

        # convert each csv row into PowerFileRow object, store in power_epoch_map
        power_epoch_map = {}
        for current in raw_buffer:
            pfr = PowerFileRow(current)
            pfr.convert_samples()

            if pfr.validate_frequencies() is False:
                raise Exception("frequency validation failed")

            #
            epoch_key = pfr.meta_map["time_stamp_epoch"]
            if epoch_key not in power_epoch_map:
                power_epoch_map[epoch_key] = PowerFileEpoch(epoch_key)

            power_epoch_map[epoch_key].add_sample(pfr)

        print(f"power epoch map len: {len(power_epoch_map)}")
        for key in power_epoch_map.keys():
            print(f"key:{key} rows:{len(power_epoch_map[key].pfr_map)}")

        return power_epoch_map


# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
