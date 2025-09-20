#
# Title: power_file_row.py
# Description: power file row domain class
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#
import datetime
import json


class PowerFileRow:
    def __init__(self, raw_row: list[str]):
        # ['2025-05-16', ' 04:16:20', ' 966482608', ' 969275710', ' 2727.64']
        # "\tdate, time, Hz low, Hz high, Hz step, samples, dbm, dbm, ...

        if len(raw_row) < 6:
            raise Exception("bad row len")

        self.raw_row = raw_row
        self.samples_list = []
        self.spectrum_list = []
        self.statistics_map = {}

        row_date = raw_row[0].split("-")
        yy = int(row_date[0])
        mm = int(row_date[1])
        dd = int(row_date[2])

        row_time = raw_row[1].split(":")
        hour = int(row_time[0])
        minute = int(row_time[1])
        second = int(row_time[2])

        dt = datetime.datetime(yy, mm, dd, hour, minute, second)

        self.pfr_meta_map = {
            "freq_low_hz": int(raw_row[2]),
            "freq_high_hz": int(raw_row[3]),
            "freq_step_hz": float(raw_row[4]),
            "sample_quantity": int(raw_row[5]),
            "time_stamp_dt": dt,
            "time_stamp_epoch": int(dt.timestamp()),
            "time_stamp_iso8601": dt.isoformat(),
        }

    def __str__(self):
        return f"{self.pfr_meta_map['time_stamp_epoch']} {self.pfr_meta_map['freq_low_hz']} {self.pfr_meta_map['freq_high_hz']} {self.pfr_meta_map['freq_step_hz']}"

    def convert_samples(self):
        # convert from string to float and discover basic row stats
        # produces self.samples_list = [(dbm, frequency), ...]
        # produces self.statistics_map = { avg_sample, min_sample, max_sample }

        avg_sample = 0
        min_sample = 0
        max_sample = -100
        total_samples = 0

        current_frequency = self.pfr_meta_map["freq_low_hz"]
        step_frequency = self.pfr_meta_map["freq_step_hz"]

        for ndx in range(6, len(self.raw_row)):  # start at 6 to skip row metadata
            current_value = float(self.raw_row[ndx])
            self.samples_list.append((int(current_frequency), current_value))
            current_frequency += step_frequency

            # collect row statistics
            total_samples += current_value

            if current_value < min_sample:
                min_sample = current_value

            if max_sample < current_value:
                max_sample = current_value

        avg_sample = 0
        if len(self.samples_list) > 0:
            avg_sample = total_samples / len(self.samples_list)

        self.statistics_map = {
            "avg_sample": avg_sample,
            "min_sample": min_sample,
            "max_sample": max_sample,
        }

    def moving_window(self, half_window_size: int) -> list[tuple[int, float, float]]:
        float_list = []  # convert sample tuples into list of floats
        for row in self.samples_list:
            float_list.append(row[1])  # sample[1] is dbm

        self.spectrum_list = []
        for ndx in range(len(float_list)):
            left_ndx = ndx - half_window_size
            right_ndx = ndx + half_window_size + 1

            if left_ndx < 0:
                left_ndx = 0

            if right_ndx >= len(float_list):
                right_ndx = len(float_list) - 1

            local_mean = sum(float_list[left_ndx:right_ndx]) / (right_ndx - left_ndx)

            sample_value = float_list[ndx]

            self.spectrum_list.append(
                (self.samples_list[ndx][0], sample_value, local_mean)
            )

    def file_name(self, cooked_dir: str) -> str:
        return f"{cooked_dir}/{self.pfr_meta_map['time_stamp_epoch']}-{self.pfr_meta_map['freq_low_hz']}"

    # plot for [col=2:3] '1756358045-154341525.gp' using 1:col
    # plot for [col=2:3] '1756358045-157138950.gp' using 1:col
    # plot for [col=2:3] '1756358045-159936375.gp' using 1:col
    def gnuplot_writer(self, cooked_dir: str) -> None:
        file_name = f"{self.file_name(cooked_dir)}.gp"

        try:
            with open(file_name, "w") as out_file:
                for current in self.spectrum_list:
                    out_file.write(f"{current[0]}\t{current[1]}\t{current[2]}\n")
        except Exception as error:
            print(error)

    # timestamp-frequency.json i.e. 1756358045-159936375.json
    def json_writer(self, pf_args: dict[str, any]) -> None:
        file_name = f"{self.file_name(pf_args['cooked_dir'])}.json"

        self.json_meta_map = {
            "antenna": pf_args["antenna"],
            "application": pf_args["application"],
            "freqHighHz": self.pfr_meta_map["freq_high_hz"],
            "freqLowHz": self.pfr_meta_map["freq_low_hz"],
            "freqStepHz": self.pfr_meta_map["freq_step_hz"],
            "halfWindowSize": pf_args["half_window_size"],
            "project": pf_args["project"],
            "receiver": pf_args["receiver"],
            "site": pf_args["site"],
            "sourceFile": pf_args["source_file"],
            "sampleQuantity": self.pfr_meta_map["sample_quantity"],
            "schemaVersion": 1,
            "timeStampEpoch": self.pfr_meta_map["time_stamp_epoch"],
            "timeStampIso8601": self.pfr_meta_map["time_stamp_iso8601"],
        }

        self.json_statistics_map = {
            "avgSample": self.statistics_map["avg_sample"],
            "minSample": self.statistics_map["min_sample"],
            "maxSample": self.statistics_map["max_sample"],
        }

        payload = {
            "meta": self.json_meta_map,
            "statistics": self.json_statistics_map,
            "samples": self.spectrum_list,
        }

        try:
            with open(file_name, "w") as out_file:
                json.dump(payload, out_file, indent=4)
        except Exception as error:
            print(error)

    def peakers_1(self) -> list[tuple[int, float]]:
        result = []

        for current in self.spectrum_list:
            if current[1] > 0.0:
                # append frequency, dbm, average
                result.append((current[0], current[1], current[2]))

        return result

    def validate_frequencies(self) -> bool:
        """ensure the promised frequency range matches calculated range"""

        actual_low = self.samples_list[0][0]
        actual_high = self.samples_list[-1][0]

        predicted_low = self.pfr_meta_map["freq_low_hz"]
        predicted_high = self.pfr_meta_map["freq_high_hz"]

        if actual_low != predicted_low or actual_high != predicted_high:
            print(f"actual low: {actual_low} predicted low: {predicted_low}")
            print(f"actual high: {actual_high} predicted high: {predicted_high}")
            return False
        else:
            # print("passed")
            return True


# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
