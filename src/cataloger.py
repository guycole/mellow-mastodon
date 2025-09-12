#
# Title: cataloger.py
# Description: update catalog files
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#
import datetime
import json
import os
import shutil
import sys
import uuid

import yaml
from yaml.loader import SafeLoader

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import postgres

from mastodon_file import MastodonFile

from sql_table import Equipment, LoadLog, Observation, Population, Site

class Loader:
    default_case_uuid = '10514480-5caf-4a41-98f2-a57eb24c2f9b'
    
    def __init__(self, configuration: dict[str, str]):
        self.db_conn = configuration["dbConn"]
        self.archive_dir = configuration["archiveDir"]
        self.catalog_dir = configuration["catalogDir"]
        self.failure_dir = configuration["failureDir"]
        self.fresh_dir = configuration["freshDir"]
        self.sql_echo = configuration["sqlEchoEnable"]

        self.population_threshold = configuration['populationThreshold']

        connect_dict = {"options": "-csearch_path={}".format("mastodon_v1")}
        db_engine = create_engine(
            self.db_conn, echo=self.sql_echo, connect_args=connect_dict
        )

        self.postgres = postgres.PostGres(
            sessionmaker(bind=db_engine, expire_on_commit=False)
        )

    def full_file_name(self, file_name: str) -> str:
        return f"{self.catalog_dir}/{file_name}.json"

    def json_reader(self, file_name: str) -> dict[str, any]:
        results = {}

        try:
            with open(file_name, "r") as in_file:
                results = json.load(in_file)
        except Exception as error:
            print(error)

        return results

    def json_writer(self, payload: dict[str, any]) -> None:
        file_name = self.full_file_name(payload['case_id'])

        try:
            with open(file_name, "w") as out_file:
                json.dump(payload, out_file, indent=4)
        except Exception as error:
            print(error)
        
    def catalog_entry(self, case_uuid: str, bin: Population, site_name: str) -> dict[str, any]:
        result = {
            "project": "big-search01",
            "case_id": case_uuid,
            "freq_bins": [bin.freq_hz],
            "freq_hz": bin.freq_hz,
            "modulation": "unknown",
            "name": "unknown",
            "note": bin.note,
            "obsFirstEpochTime": int(bin.obs_first.timestamp()),
            "obsLastEpochTime": int(bin.obs_last.timestamp()),
            "obsSite": site_name,
            "samples": []
        }

        return result
        
    def create_fresh_case(self, bin: Population, site: Site) -> None:
        case_uuid = str(uuid.uuid4())
        payload = self.catalog_entry(case_uuid, bin, site.name)
        self.json_writer(payload)

    def update_existing_case(self, bin: Population) -> None:
        pass

    def process_site_population(self, site: Site) -> None:
        print(f"process {site}")

        below_threshold = 0
        existing_case = 0
        fresh_case = 0

        population_list = self.postgres.population_select_all_by_site(site.id)
        for bin in population_list:
            if bin.population < self.population_threshold:
                below_threshold = below_threshold + 1
                continue

            if bin.case_uuid == self.default_case_uuid:
                fresh_case = fresh_case + 1
                self.create_fresh_case(bin, site)
            else:
                existing_case = existing_case + 1
                # self.update_existing_case(bin)

        print(f"site {site.name} below {below_threshold} existing {existing_case} fresh {fresh_case}")

    def execute(self) -> None:
        site_list = self.postgres.site_select_all()

        for site in site_list:
            self.process_site_population(site)
            
print("start loader")

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

    loader = Loader(configuration)
    loader.execute()

print("stop loader")

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
