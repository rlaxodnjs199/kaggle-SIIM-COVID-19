from os import getenv
from dotenv import load_dotenv

load_dotenv()

COMPETITION = getenv('COMPETITION')
DATASET_PATH = getenv('DATASET_PATH')
SUBMISSION_DATA_PATH = getenv('SUBMISSION_DATA_PATH')
