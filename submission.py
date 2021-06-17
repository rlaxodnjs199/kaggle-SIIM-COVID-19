from kaggle.api.kaggle_api_extended import KaggleApi
from config import *

api = KaggleApi()
api.authenticate()


def download_datasets():
    api.dataset_download_files(
        'xhlulu/siim-covid19-resized-to-256px-jpg', path=DATASET_PATH)
    api.dataset_download_files(
        'dschettler8845/siim-covid19-updated-train-labels', path=DATASET_PATH)
    api.competition_download_files(
        COMPETITION, path=DATASET_PATH)


def download_sample_submission():
    api.competition_download_file(
        COMPETITION, 'sample_submission.csv', path='./')


def submit_result(message: str):
    api.competition_submit(SUBMISSION_DATA_PATH, message, COMPETITION)


if __name__ == '__main__':
    submit_result('Test Submission')
