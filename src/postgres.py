#
# Title: postgres.py
# Description: postgresql support
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#
# import sqlalchemy
# from sqlalchemy import and_
# from sqlalchemy import select

import datetime
import time

import sqlalchemy
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import select

from sql_table import (
    LoadLog,
)

class PostGres:
    db_engine = None
    Session = None

    def __init__(self, session: sqlalchemy.orm.session.sessionmaker):
        self.Session = session

    def load_log_insert(
        self, args: dict[str, any], obs_quantity: int, geo_loc_id: int
    ) -> LoadLog:
        args["duration_ms"] = 0
        args["file_date"] = args["file_time"].date()
        args["obs_quantity"] = obs_quantity

        candidate = LoadLog(args, geo_loc_id)

        try:
            with self.Session() as session:
                session.add(candidate)
                session.commit()
        except Exception as error:
            print(error)

        return candidate

    def load_log_select_all(self) -> list[LoadLog]:
        with self.Session() as session:
            return session.scalars(select(LoadLog)).all()

    def load_log_select_by_file_name(self, file_name: str) -> LoadLog:
        with self.Session() as session:
            return session.scalars(
                select(LoadLog).filter_by(file_name=file_name)
            ).first()

    def load_log_select_by_file_date(self, target: datetime) -> list[LoadLog]:
        with self.Session() as session:
            return session.scalars(select(LoadLog).filter_by(file_date=target)).all()

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
