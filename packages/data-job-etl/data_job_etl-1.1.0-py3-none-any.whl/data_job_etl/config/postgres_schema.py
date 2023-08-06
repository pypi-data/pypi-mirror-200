from numpy.random._generator import Sequence
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, inspect, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

Base = declarative_base()


class RawJob(Base):
    __tablename__ = 'raw_jobs'

    id = Column(Integer, primary_key=True)
    url = Column(String(400), nullable=False, unique=True)
    title = Column(String(100), nullable=False)
    company = Column(String(100), nullable=False)
    industry = Column(String(100))
    location = Column(String(100))
    remote = Column(String(100))
    type = Column(String(20))
    created_at = Column(Date)
    text = Column(String)


class ProcessedJob(Base):
    __tablename__ = 'processed_jobs'

    id = Column(Integer, primary_key=True)
    url = Column(String(500), nullable=False, unique=True)
    title = Column(String(150), nullable=False)
    company = Column(String(150), nullable=False)
    stack = Column(String(500))
    remote = Column(String(150))
    location = Column(String(150))
    industry = Column(String(150))
    type = Column(String(150))
    created_at = Column(Date)
    text = Column(String)
    summary = Column(String)


class PivottedJob(Base):
    __tablename__ = 'pivotted_jobs'

    id = Column(Integer, primary_key=True)
    raw_id = Column(Integer)
    url = Column(String(500), nullable=False)
    title = Column(String(150), nullable=False)
    company = Column(String(150), nullable=False)
    technos = Column(String(500))
    remote = Column(String(150))
    location = Column(String(150))
    industry = Column(String(150))
    type = Column(String(150))
    created_at = Column(Date)
