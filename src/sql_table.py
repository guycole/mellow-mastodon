#
# Title: sql_table.py
# Description: database table definitions
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#
# import sqlalchemy
# from sqlalchemy import and_
# from sqlalchemy import select

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, String

from sqlalchemy.orm import registry
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declared_attr

mapper_registry = registry()


class Base(DeclarativeBase):
    pass

class BinSample(Base):
    """bin_sample table definition"""

    __tablename__ = "bin_sample"

    id = Column(Integer, primary_key=True)
    bin_ndx = Column(Integer)
    freq_hz = Column(Integer)
    peaker_flag = Column(Boolean)
    rolling_mean = Column(Float)
    row_head_id = Column(BigInteger)
    signal_dbm = Column(Float)

    def __init__(self, args: dict[str, any]):
        self.bin_ndx = args["bin_ndx"]
        self.freq_hz = args["freq_hz"]
        self.peaker_flag = args["peaker_flag"]
        self.rolling_mean = args["rolling_mean"]
        self.row_head_id = args["row_head_id"]
        self.signal_dbm = args["signal_dbm"]

    def __repr__(self):
        return f"bin_sample({self.row_id} {self.bin_ndx})"
    
class LoadLog(Base):
    """load_log table definition"""

    __tablename__ = "load_log"

    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    file_type = Column(String)
    freq_mhz_low = Column(Integer)
    freq_mhz_high = Column(Integer)
    first_row_date = Column(Date)
    first_row_time = Column(DateTime)
    project = Column(String)
    site = Column(String)

    def __init__(self, args: dict[str, any]):
        self.file_name = args["file_name"]
        self.file_type = args["file_type"]
        self.freq_mhz_low = args["freq_mhz_low"]
        self.freq_mhz_high = args["freq_mhz_high"]
        self.first_row_date = args["first_row_date"]
        self.first_row_time = args["first_row_time"]
        self.project = args["project"]
        self.site = args["site"]

    def __repr__(self):
        return f"load_log({self.file_name} {self.first_row_time})"

class RowHeader(Base):
    """row_header table definition"""

    __tablename__ = "row_header"

    id = Column(Integer, primary_key=True)
    bin_quantity = Column(Integer)
    freq_hz_low = Column(Integer)
    freq_hz_high = Column(Integer)
    freq_hz_step = Column(Float)
    load_log_id = Column(BigInteger)
    row_date = Column(Date)
    row_time = Column(DateTime)
    sample_quantity = Column(Integer)

    def __init__(self, args: dict[str, any]):
        self.bin_quantity = args["bin_quantity"]
        self.freq_hz_low = args["freq_hz_low"]
        self.freq_hz_high = args["freq_hz_high"]
        self.freq_hz_step = args["freq_hz_step"]
        self.load_log_id = args["load_log_id"]
        self.row_date = args["row_date"]
        self.row_time = args["row_time"]
        self.sample_quantity = args["sample_quantity"]

    def __repr__(self):
        return f"row_header({self.load_log_id} {self.freq_hz_low} {self.freq_hz_high})"

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
