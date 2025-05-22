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
    """load_log table definition"""

    __tablename__ = "bin_sample"

    id = Column(Integer, primary_key=True)
    bin_ndx = Column(Integer)
    freq_hz = Column(Integer)
    parent_id = Column(BigInteger)
    signal_dbm = Column(Float)

    def __init__(self, args: dict[str, any]):
        self.bin_ndx = args["bin_ndx"]
        self.freq_hz = args["freq_hz"]
        self.parent_id = args["parent_id"]
        self.signal_dbm = args["signal_dbm"]

    def __repr__(self):
        return f"bin_sample({self.parent_id} {self.bin_ndx})"
    
class LoadLog(Base):
    """load_log table definition"""

    __tablename__ = "load_log"

    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    file_type = Column(String)
    freq_mhz_low = Column(Integer)
    freq_mhz_high = Column(Integer)
    obs_date = Column(Date)
    obs_time = Column(DateTime)
    project = Column(String)
    site = Column(String)

    def __init__(self, args: dict[str, any]):
        self.file_name = args["file_name"]
        self.file_type = args["file_type"]
        self.freq_mhz_low = args["freq_mhz_low"]
        self.freq_mhz_high = args["freq_mhz_high"]
        self.obs_date = args["obs_date"]
        self.obs_time = args["obs_time"]
        self.project = args["project"]
        self.site = args["site"]

    def __repr__(self):
        return f"load_log({self.file_name} {self.obs_time})"

class RowHeader(Base):
    """row_header table definition"""

    __tablename__ = "row_header"

    id = Column(Integer, primary_key=True)
    bin_quantity = Column(Integer)
    freq_hz_low = Column(Integer)
    freq_hz_high = Column(Integer)
    freq_hz_step = Column(Integer)
    load_log_id = Column(BigInteger)
    obs_time = Column(DateTime)
    sample_quantity = Column(Integer)

    def __init__(self, args: dict[str, any]):
        self.bin_quantity = args["bin_quantity"]
        self.freq_hz_low = args["freq_hz_low"]
        self.freq_hz_high = args["freq_hz_high"]
        self.freq_hz_step = args["freq_hz_high"]
        self.load_log_id = args["load_log_id"]
        self.obs_time = args["obs_time"]
        self.sample_quantity = args["sample_quantity"]

    def __repr__(self):
        return f"row_header({self.load_log_id} {self.freq_hz_low} {self.freq_hz_high})"

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
