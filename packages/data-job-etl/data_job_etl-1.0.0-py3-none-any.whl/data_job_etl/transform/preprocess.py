import pandas as pd
import numpy as np
import re


class Preprocessor:

    def __init__(self, jobs):
        self.jobs = jobs

    def preprocess(self):
        self.cast_types(self.jobs)
        self.add_missing_value(self.jobs)
        self.jobs['title'] = self.jobs['title'].apply(lambda x: self.process_title(x))
        self.jobs['text'] = self.jobs['text'].apply(lambda x: self.process_text(x))
        self.jobs.reset_index(inplace=True, drop=True)

    @staticmethod
    def cast_types(jobs):
        jobs = jobs.convert_dtypes()
        jobs['id'] = jobs['id'].values.astype(int)
        jobs['created_at'] = pd.to_datetime(jobs['created_at'])
        return jobs

    @staticmethod
    def add_missing_value(jobs):
        jobs['remote'] = jobs['remote'].replace('N', np.nan)
        return jobs

    @staticmethod
    def process_title(title):
        HF = r'\(?H\s?\/?\s?F\)?'
        FHX = r'\(?F\s?\/?\s?H\)?\/?X?\)?'
        MFD = r'\(?M\s?\/?\s?F\)?\/?D?\)?'
        FMD = r'\(?F\s?\/?\s?M\)?\/?D?\)?'
        mfd = r'\(m\/f\/d\)'
        fmd = r'\(f\/m\/d\)'
        mwd = r'\(m\/w\/d\)'
        HST = r'\(H\/S\/T\)'
        MW = r'M\/W'
        gender_regex = f'{HF}|{MFD}|{FMD}|{FHX}|{mfd}|{fmd}|{mwd}|{HST}|{MW}'
        title = re.sub(gender_regex, '', title)
        title = title.strip()
        return title

    @staticmethod
    def process_text(text):
        text = text.replace(u'\xa0', u' ')  # \xa0 (non-breaking space in Latin1 ISO 8859-1)
        text = re.sub('\s\s\s+', ' ', text)
        text = re.sub('^\s*', '', text)
        return text
