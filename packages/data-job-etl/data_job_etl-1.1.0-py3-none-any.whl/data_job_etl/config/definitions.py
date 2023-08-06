import os
import json
from pathlib import Path

PROJECT_PATH = Path(os.path.dirname(os.path.abspath(__file__))).parent
DATA_PATH = os.path.join(PROJECT_PATH, 'elt/transform/data')

JOB_MARKET_DB_PWD = os.environ['JOB_MARKET_DB_PWD']
JOB_MARKET_DB_USER = os.environ['JOB_MARKET_DB_USER']
DB_STRING = f"postgresql://{JOB_MARKET_DB_USER}:{JOB_MARKET_DB_PWD}@localhost:5432/job_market"

with open('/Users/donor/PycharmProjects/data-job-etl/data_job_etl/data/mad2023.json', 'r') as f:
    mad = json.load(f)
MAD_TECHNOS = [x['name'] for x in mad]
OTHER_TECHNOS = {'DataBuildTool', 'MxNet', 'Hadoop', 'Beam', 'BigQuery', 'Pig', 'DataStudio', 'Redshift', 'Shell', 'Gitlab', 'data vault', 'Ceph', 'Airflow', 'GCP', 'IAM', 'k8s', 'Numpy', 'MAPR', 'Node', 'Athena', 'Unix', 'NiFi', 'Mongo', 'NoSQL', 'Unix Shell', 'Azure', 'Go', 'Golang', 'Perl', 'EC2', 'EMR', 'SPAR', 'Jenkins', 'Git', 'C/C\\+\\+', 'airflow', 'CloudSQL', 'Ruby', 'Redshift Spectrum', 'Glue', 'Postgres', 'Salt', 'python', 'nodejs', 'Go lang', 'Qlikview', 's3', 'Protobuf', 'MapReduce', 'Google Cloud', 'Elasticsearch', 'Spark', 'Celery', 'Pagerduty', 'mlflow', 'React', 'C\\+\\+', 'Tensorflow', 'Stitch DataGraphQL', 'Django', 'HDFS', 'Matillion WTL', 'SQL server', 'Istio', 'Dataflow', 'Codecov', 'UNIX', 'Typescript', 'DynamoDB', 'Vitess', 'Cassandra', 'HTTP', 'VizQL', 'C#', 'S3', 'SQL', 'Akka', 'MS-SQL', 'Stackdriver', 'Quicksilver', 'Github', 'dbt', 'DAX', 'StitchData', 'HBase', 'Microsoft SSIS', 'AWS S3', 'K8S', 'Java', 'SparkSQL', 'Kubeflow', 'ElasticSearch', '(No)SQL', 'Kinesis', 'Bigtable', 'CockroachDB', 'Scipy', 'Bash', 'git', 'Scikit Learn', 'Google Cloud Platform', 'Synapse', 'AWS', 'Spanner', 'H20', 'Javascript', 'LAMP', 'SQL Server', 'Py torch', 'PHP', 'PowerBI', 'gRPC', 'SAP', 'Neo4J', 'Cloud SQL', 'Reddis', 'Linux', 'SageMaker', 'dataiku', 'PQL', 'GCS', 'CircleCI', 'Kimball'}
PRETTY_TECHNOS = OTHER_TECHNOS.union(MAD_TECHNOS)
TECHNOS = {w.lower() for w in PRETTY_TECHNOS}


