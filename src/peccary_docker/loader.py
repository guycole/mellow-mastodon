#
# Title: loader.py
# Description: load mastodon files
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#
import logging
import datetime
import json
import os

from helper.json_helper import JsonHelper, schema

from helper.postgres import PostGres

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("loader")


class Loader:

    def __init__(self, postgres: PostGres):
        self.postgres = postgres

        self.failure_dir = os.environ.get("FAILURE_DIR", "/var/peccary/mastodon/failure")
        self.fresh_dir = os.environ.get("FRESH_DIR", "/var/peccary/mastodon/mastodon-v1")

        self.failure = 0
        self.success = 0

        self.jh = JsonHelper()

    def file_failure(self, file_name: str):
        #        logger.info(f"file failure:{file_name}")

        self.failure += 1
        os.rename(file_name, self.failure_dir + "/" + file_name)

    def file_success(self, file_name: str):
        #        logger.info(f"file success:{file_name}")

        self.success += 1
        os.remove(file_name)

    def _job_task(self) -> str:
        task = self.jh.raw_json.get("job", {}).get("task")
        if isinstance(task, str):
            task = task.strip()

        if task:
            return task

        raise ValueError("job.task must be a non-empty string")

    def load_log_test(self, test_file_name: str) -> bool:
        logger.info(f"load_log_test for file: {test_file_name}")

        try:
            candidate = self.postgres.load_log_select_by_file_name(test_file_name)
            if candidate is None:
                logger.info(f"processing new file:{test_file_name}")
                task = self._job_task()

                geo_loc = self.postgres.geo_loc_select_by_site(self.jh.raw_json["geoLoc"]["siteName"])
                if len(geo_loc) == 0:
                    print("must insert geo_loc for site:", self.jh.raw_json["geoLoc"]["siteName"])
                    return False

                load_log = {
                    "crate_name": self.jh.raw_json["crateName"],
                    "epoch_seconds": self.jh.raw_json["timeStamp"]["epochSeconds"],
                    "file_name": test_file_name,
                    "geo_loc_id": geo_loc[0].id,
                    "host_name": self.jh.raw_json["equipment"]["hostName"],
                    "load_time": datetime.datetime.now(),
                    "mode": self.jh.raw_json["job"]["mode"],
                    "obs_time": self.jh.raw_json["timeStamp"]["iso8601"],
                    "peaker_quantity": len(self.jh.raw_json["peakers"]),
                    "site_name": self.jh.raw_json["geoLoc"]["siteName"],
                    "task": task,
                }

                self.load_log_id = self.postgres.load_log_insert(load_log).id

                daily_score = {
                    "crate_name": self.jh.raw_json["crateName"],
                    "file_quantity": 1,
                    "host_name": self.jh.raw_json["equipment"]["hostName"],
                    "peaker_quantity": len(self.jh.raw_json["peakers"]),
                    "score_date": datetime.date.fromisoformat(self.jh.raw_json["timeStamp"]["iso8601"][:10]),
                    "task": task,
                }

                self.postgres.daily_score_insert_or_update(daily_score)

                if len(self.jh.raw_json["peakers"]) < 1:
                    logger.info("skipping file with no peakers")
                    return False

                return True
        except Exception as error:
            logger.error(f"postgres insert failed for {test_file_name}: {error}")

        return False

    def load_obs(self) -> bool:
        if self.load_log_id is None or self.load_log_id < 1:
            logger.error("load_log_id is not set")
            return False

        task = self._job_task()
        
        try:
            for observation in self.jh.raw_json["peakers"]:
                obs = {
                    "baseline_dbm": observation[2],
                    "freq_hz": observation[0],
                    "load_log_id": self.load_log_id,
                    "power_dbm": observation[1],
                }

                self.postgres.observation_insert(obs)

                score = {
                    "crate_name": self.jh.raw_json["crateName"],
                    "freq_hz": observation[0],
                    "peaker_quantity": 1,
                    "task": task,
                }

                self.postgres.peaker_score_insert_or_update(score)

            return True
        except Exception as error:
            logger.error(f"observation insert failed for load_log_id {self.load_log_id}: {error}")

        return False


    def file_processor(self, file_name) -> None:
        if os.path.isfile(file_name) is False:
            logger.warning(f"skipping non-file:{file_name}")
            self.file_failure(file_name)
            return

        if os.path.getsize(file_name) < 1:
            logger.warning(f"skipping empty file:{file_name}")
            self.file_failure(file_name)
            return

        if not file_name.endswith(".json"):
            logger.warning(f"skipping non-json:{file_name}")
            self.file_failure(file_name)
            return

        if not self.jh.json_file_reader(file_name, True):
            logger.warning(f"json file read/verify failure for {file_name}")
            self.file_failure(file_name)
            return

        if self.jh.raw_json["fileName"] != file_name:
            logger.warning(
                f"mismatched file name: {self.jh.raw_json['fileName']} vs {file_name}"
            )
            self.file_failure(file_name)
            return

        if (
            self.jh.raw_json["version"] == 1
            and self.jh.raw_json["job"]["project"] == "mastodon-v1"
        ):
            pass
        else:
            logger.warning(f"invalid version or project for {file_name}")
            self.file_failure(file_name)
            return

        if self.load_log_test(file_name):
            pass
        else:
            self.file_failure(file_name)
            return

        if self.load_obs():
            pass
        else:
            self.file_failure(file_name)
            return

        self.file_success(file_name)

    def execute(self) -> None:
        logger.info(f"loader fresh dir:{self.fresh_dir}")

        os.chdir(self.fresh_dir)
        targets = sorted(os.listdir("."))
        logger.info(f"{len(targets)} files noted")

        for target in targets:
            self.file_processor(target)

        logger.info(f"loader success:{self.success} failure:{self.failure}")

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
