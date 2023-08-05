import os
import pandas as pd
# import spacy
import json
import re
import importlib.resources

from data_job_etl.config.definitions import PROJECT_PATH, TECHNOS


class Processor:

    def __init__(self, jobs):
        self.jobs = jobs
        # self.model_path = os.path.join(PROJECT_PATH, f'elt/transform/data/model_en/model-best')

    def process_technos(self):
        technos_added = self.add_technos_from_custom_list()
        technos_pivotted = self.pivot_technos(technos_added)
        df_cleaned = self.clean_df(technos_pivotted)
        technos_mapped = self.map_techno_lower_to_pretty(df_cleaned)
        technos_mapped.reset_index(drop=True, inplace=True)
        return technos_mapped

    def add_technos_from_custom_list(self):
        """
        Add a 'stack' column containing a list of technologies present in the text of the job posting
        then expand this list in as many columns as there are elements in the list.
        """
        # create a column containing a list of technologies present in the text column
        self.jobs['stack'] = self.jobs['text'].apply(lambda x: self.extract_custom_technos(x))

        # transform dataframe with one column per technology
        technos = pd.DataFrame(self.jobs['stack'].to_list())
        df = pd.merge(self.jobs, technos, left_index=True, right_index=True)
        return df

    @staticmethod
    def extract_custom_technos(text):
        """
        Extracts a list of technology names from a text.
        """
        words = re.split(r'\W+', text)
        technos = {w.lower() for w in words if w.lower() in TECHNOS}
        return list(technos)

    @staticmethod
    def pivot_technos(df):
        """ Melt dataframe to have one technology per row (for usage in Tableau). """
        unpivotted_columns = ['url', 'title', 'company', 'location', 'type', 'industry', 'remote', 'created_at',
                              'text', 'stack']
        pivotted_technos = pd.melt(df, id_vars=unpivotted_columns).sort_values(by=['company', 'created_at', 'title'])
        pivotted_technos.reset_index(drop=True, inplace=True)
        return pivotted_technos

    @staticmethod
    def clean_df(df):
        # rename technos column
        df['technos'] = df['value']
        # delete old columns
        df.drop(['variable', 'stack', 'value'], axis=1, inplace=True)
        # remove missing values
        df.dropna(subset='technos', inplace=True)
        return df

    @staticmethod
    def map_techno_lower_to_pretty(df):
        """ Rename techno with their cased name and correcting aliases. """
        with importlib.resources.path('data_job_etl.data', 'technos_lower_to_pretty.csv') as path:
            mapper = pd.read_csv(path, sep=';')
        lower = mapper.Skills_lower.values
        pretty = mapper.Skills_pretty.values
        mapper_dict = dict(zip(lower, pretty))
        df['technos'] = df['technos'].map(mapper_dict)
        return df

#     def add_technos_from_model(self):
#         self.jobs['technos'] = self.jobs['text'].apply(lambda x: self.extract_ner_technos(x))
#
#     def extract_ner_technos(self, text):
#         model_output = spacy.load(self.model_path)
#         doc = model_output(text)
#         technos = [ent.text for ent in doc.ents]
#         return list(set(technos))
#
# df = pd.DataFrame(columns=['title', 'company'])
# TechnosProcessor.map_techno_lower_to_pretty(df)
