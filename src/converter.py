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

class Converter:

#    date, time, Hz low, Hz high, Hz step, samples, dbm, dbm, ...


    def process_row(self, row: list[str]) -> bool:
        print(len(row))
        print(row[0:9])
             
        return True

    def file_reader(self, file_name: str) -> bool:
        self.preamble = {}

        try:
            with open(file_name, "r") as in_file:
                csv_file = csv.reader(in_file)
                for row in csv_file:
                    self.process_row(row)

        except Exception as error:
            print(error)
            return False

        return True

    def converter(self, file_name: str) -> bool:
        if self.file_reader(file_name) is False:
            return False

        return True

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
