import logging
from data_job_etl.config.etl_logger import logger

from data_job_etl.extract.extract import Extractor
from data_job_etl.transform.preprocess import Preprocessor
from data_job_etl.transform.process import Processor
from data_job_etl.load.load import Loader


def extract():
    extractor = Extractor()
    raw_jobs = extractor.extract_table('raw_jobs')
    return raw_jobs


def transform(raw_jobs):
    preprocessor = Preprocessor(raw_jobs)
    preprocessor.preprocess()
    preprocessed_jobs = preprocessor.jobs

    processor = Processor()
    processed_jobs = processor.process_technos(preprocessed_jobs)
    pivotted_jobs = processor.pivot_technos(processed_jobs)
    return processed_jobs, pivotted_jobs


def load(processed_jobs, pivotted_jobs):
    loader = Loader()
    loader.load_processed(processed_jobs)
    loader.load_pivotted(pivotted_jobs)


def main():
    try:
        raw_jobs = extract()
        processed_jobs, pivotted_jobs = transform(raw_jobs)
        load(processed_jobs, pivotted_jobs)
    except Exception as e:
        logger.exception("Exception occurred:\n", e)


if __name__ == "__main__":
    main()
