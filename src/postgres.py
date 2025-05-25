#
# Title: postgres.py
# Description: postgresql support
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#

import datetime
import time

import sqlalchemy
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import select

from sql_table import (
    BinSample, LoadLog, RowHeader
)

class PostGres:
    db_engine = None
    Session = None

    def __init__(self, session: sqlalchemy.orm.session.sessionmaker):
        self.Session = session
        
    def bin_sample_insert(self, args: dict[str, any]) -> BinSample:
        candidate = BinSample(args)

        try:
            with self.Session() as session:
                session.add(candidate)
                session.commit()
        except Exception as error:
            print(error)

        return candidate

    def bin_sample_bulk_insert(self, bin_samples: list[dict[str, any]], row_head_id: int) -> None:
        for sample in bin_samples:
            sample["row_head_id"] = row_head_id

        try:
            with self.Session() as session:
                session.bulk_insert_mappings(BinSample, bin_samples)
                session.commit()
        except Exception as error:
            print(error)

    def load_log_insert(self, args: dict[str, any]) -> LoadLog:
        args["first_row_date"] = args["first_row_time"].date()

        candidate = LoadLog(args)

        try:
            with self.Session() as session:
                session.add(candidate)
                session.commit()
        except Exception as error:
            print(error)

        return candidate

#    def load_log_select_all(self) -> list[LoadLog]:
#        with self.Session() as session:
#            return session.scalars(select(LoadLog)).all()

    def load_log_select_by_file_name(self, file_name: str) -> LoadLog:
        with self.Session() as session:
            return session.scalars(select(LoadLog).filter_by(file_name=file_name)).first()

#    def load_log_select_by_file_date(self, target: datetime) -> list[LoadLog]:
#        with self.Session() as session:
#            return session.scalars(select(LoadLog).filter_by(file_date=target)).all()

    def row_header_insert(self, args: dict[str, any]) -> RowHeader:
        args["row_date"] = args["row_time"].date()
        
        candidate = RowHeader(args)

        try:
            with self.Session() as session:
                session.add(candidate)
                session.commit()
        except Exception as error:
            print(error)

        return candidate

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
