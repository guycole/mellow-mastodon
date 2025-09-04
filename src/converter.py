#
# Title: converter.py
# Description:
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#

import csv
import datetime
import json
import sys
import time
import uuid

#from sql_table import BinSample, LoadLog, RowHeader

class Converter:

    def __init__(self, file_name: str):
        self.file_name = file_name

    def json_reader(self, file_name: str) -> dict[str, any]:
        results = {}

        try:
            with open(file_name, "r") as in_file:
                results = json.load(in_file)
        except Exception as error:
            print(error)

        return results
    
    def meta(self, raw_json: dict[str, any]) -> dict[str, any]:
        meta = raw_json['meta']
        meta['file_type'] = 'mastodon-v1'
        meta['time_stamp_dt'] = datetime.datetime.fromisoformat(meta['time_stamp_iso8601'])
        meta['time_stamp_epoch'] = int(meta['time_stamp_dt'].timestamp())
        return meta
    
    def peakers(self, raw_json: dict[str, any]) -> list[dict[str, any]]:
        return raw_json['peakers']

    def converter(self) -> bool:
        raw_json = self.json_reader(self.file_name)
        self.meta(raw_json['meta'])
        self.peakers(raw_json['peakers'])
        return True

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
