from sqlalchemy import create_engine
import pandas as pd

from data_job_etl.config.definitions import DB_STRING


class Extractor:

    def __init__(self):
        self.engine = None

    def extract_raw_jobs(self):
        self.engine = create_engine(DB_STRING)
        raw_jobs = pd.read_sql('raw_jobs', self.engine)
        return raw_jobs



