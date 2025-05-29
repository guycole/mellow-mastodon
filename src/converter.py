#
# Title: converter.py
# Description:
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#

import csv
import datetime
import sys
import time
import uuid

from sql_table import BinSample, LoadLog, RowHeader

class Converter:

    converted = {}

#    date, time, Hz low, Hz high, Hz step, samples, dbm, dbm, ...

    def parse_file_name(self, file_name: str) -> bool:
        # file name has form project-uuid.site #
        # big-search-d25fbdd2-4445-4d4c-bebc-bbbb4d4122d8.vallejo1

        tokens = file_name.split(".")
        if len(tokens) != 2:
            print("skipping bad file name")
            return False

        self.converted = {
            "file_name": file_name,
            "project": tokens[0][:-37],
            "site": tokens[1],
            "rows": []
        }

        return True

    def process_row_meta(self, row: list[str]) -> dict[str, any]:
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

    def process_row(self, row: list[str]) -> dict[str, any]:
        row_meta = self.process_row_meta(row[0:6])

        mean_array_length = 63
        rolling_mean_values = [-23]*mean_array_length

        current_freq = row_meta["freq_low"]
        for ndx in range(6, len(row)):
            bin_value = float(row[ndx])

            rolling_mean_values.pop(0)
            rolling_mean_values.append(bin_value)

            mean_value = sum(rolling_mean_values)/mean_array_length
            peaker_flag = True if abs(bin_value) > abs(mean_value)  else False
            
            # iterate for each bin and convert to sql_table.BinSample dictionary
            bin_sample = {
                "bin_ndx": ndx, # note origin is six not zero
                "freq_hz": current_freq,
                "peaker_flag": peaker_flag,
                "rolling_mean": mean_value,
                "row_head_id": 0,
                "signal_dbm": bin_value
            }

            row_meta["bin_samples"].append(bin_sample)

            current_freq += row_meta["freq_step"]

        # shift moving average (to fix lagging value)
#        bin_samples = row_meta["bin_samples"]
#        lag_ndx = 0

#        for lead_ndx in range(mean_array_length//2, len(bin_samples)):
#            leading = bin_samples[lead_ndx]
#            lagging = bin_samples[lag_ndx]

#            lagging["rolling_mean"] = leading["rolling_mean"]

#            bin_value = lagging["signal_dbm"]
#            threshold_value = abs(lagging["rolling_mean"]) * 1.11
 
#            lagging["peaker_flag"] = True if abs(bin_value) > threshold_value else False

#            lag_ndx += 1

        return row_meta

    def csv_file_reader(self, file_name: str) -> bool:
        try:
            with open(file_name, "r") as in_file:
                csv_file = csv.reader(in_file)
                for row in csv_file:
                    self.converted["rows"].append(self.process_row(row))
        except Exception as error:
            print(error)
            return False

        return True

    def get_converted(self) -> dict[str, any]:
        return self.converted

    def get_load_log(self) -> LoadLog:
        if len(self.converted) < 1:
            raise Exception("empty converted dictionary")

        if len(self.converted["rows"]) < 1:
            raise Exception("zero converted rows")

        time_stamp = self.converted["rows"][0]["time_stamp"]

        freq_low = sys.maxsize
        freq_high = 0

        # discover min max freq
        for row in self.converted["rows"]:
            for element in row["bin_samples"]:
                freq_low = min(freq_low, element["freq_hz"])
                freq_high = max(freq_high, element["freq_hz"])

        return {
            "file_name": self.converted["file_name"],
            "file_type": "mastodon_v1",
            "freq_mhz_low": round(freq_low),
            "freq_mhz_high": round(freq_high),
            "first_row_time": time_stamp,
            "project": self.converted["project"],
            "site": self.converted["site"],
        }

    def get_bin_sample(self, args, row_id: int) -> BinSample:
        return {
            "bin_ndx": args[0],
            "freq_hz": round(args[2]),
            "parent_id": row_id,
            "signal_dbm": args[1]
        }

    def get_row_header(self, args: dict[str, any], load_log_id: int) -> RowHeader:
        return {
            "bin_quantity": len(args["bin_samples"]),
            "freq_hz_low": args["freq_low"],
            "freq_hz_high": args["freq_high"],
            "freq_hz_step": args["freq_step"],
            "load_log_id": load_log_id,
            "row_time": args["time_stamp"],
            "sample_quantity": args["sample_quantity"]
        }

    def converter(self, file_name: str) -> bool:
        """ main entry point """

        if self.parse_file_name(file_name) is False:
            print("file name parse failure")
            return False

        if self.csv_file_reader(file_name) is False:
            print("file reader failure")
            return False

        print(f"rows converted {len(self.converted['rows'])}")

        return True

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
