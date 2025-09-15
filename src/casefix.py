#
# Title: casefix.py
# Description: read a case from the catalog and update the database
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


from jsonschema import validate

schema = {
    "type": "object",

    "properties": {
        "project": {"type": "string"},
        "schemaVersion": {"type": "number"},
        "caseId": {"type": "string", "format": "uuid"},
        "freqBins": {
            "type": "array",
            "items": {"type": "number"}
        },
        "freqHz": {"type": "number"},
        "modulation": {"type": "string"},
        "name": {"type": "string"},
        "note": {"type": "string"},
        "obsFirstEpochTime": {"type": "number"},
        "obsLastEpochTime": {"type": "number"},
        "obsSite": {"type": "string"},
        "samples": {
            "type": "array",
            "items": {"type": "string", "format": "uuid"},
        }  
    },

    "required": ["project", "schemaVersion", "caseId", "freqBins", "freqHz",
                 "modulation", "name", "note", "obsFirstEpochTime",
                 "obsLastEpochTime", "obsSite"],
    "additionalProperties": False
}

class CaseFix:
    default_case_uuid = '10514480-5caf-4a41-98f2-a57eb24c2f9b'
    
    def __init__(self, configuration: dict[str, str]):
        self.db_conn = configuration["dbConn"]
        self.catalog_dir = configuration["catalogDir"]
        self.population_threshold = configuration['populationThreshold']
        self.sql_echo = configuration["sqlEchoEnable"]

        connect_dict = {"options": "-csearch_path={}".format("mastodon_v1")}
        db_engine = create_engine(
            self.db_conn, echo=self.sql_echo, connect_args=connect_dict
        )

        self.postgres = postgres.PostGres(
            sessionmaker(bind=db_engine, expire_on_commit=False)
        )

    def full_file_name(self, case_uuid: str) -> str:
        return f"{self.catalog_dir}/{case_uuid}.json"

    def json_reader(self, case_uuid: str) -> dict[str, any]:
        file_name = self.full_file_name(case_uuid)
        results = {}

        if os.path.isfile(file_name) is False:
            print(f"missing {file_name}")
            return {}

        try:
            with open(file_name, "r") as in_file:
                results = json.load(in_file)
                validate(instance=results, schema=schema)
        except Exception as error:
            print(error)
            return {}

        return results
    
    def population_update(self, freq_hz: int, case_card: dict[str, any]) -> None:
        print(f"updating {freq_hz}")

        site_id = 2

        population_select = self.postgres.population_select_by_frequency_site_id(freq_hz, site_id)
        if population_select is None:
            print(f"no population entry for {freq_hz} {site_id}")
            return
        
        # update population and write to database


    def execute(self, case_uuid: str) -> None:
        print(f"casefix {case_uuid}")
        # read case card
        case_card = self.json_reader(case_uuid)
        print(case_card)
        if len(case_card) < 1:
            print(f"case {case_uuid} not found")
            return
        
        # select population entry for each freq bin
        for bin in case_card['freqBins']:
            self.population_update(bin, case_card)
            
print("start loader")

#
# argv[1] = case uuid
# argv[2] = configuration filename
#
if __name__ == "__main__":
    print(len(sys.argv))

    case_uuid = sys.argv[1]

    if len(sys.argv) > 2:
        config_name = sys.argv[2]
    else:
        config_name = "config.yaml"

    with open(config_name, "r", encoding="utf-8") as in_file:
        try:
            configuration = yaml.load(in_file, Loader=SafeLoader)
        except yaml.YAMLError as error:
            print(error)

    casefix = CaseFix(configuration)
    casefix.execute(case_uuid)

print("stop loader")

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
