import os
from kaggle.api.kaggle_api_extended import KaggleApi
from dotenv import load_dotenv

load_dotenv()
api = KaggleApi()
api.authenticate()


def download_datasets():
    api.dataset_download_files(
        'xhlulu/siim-covid19-resized-to-256px-jpg', path=os.getenv('DATASET_PATH'))
    api.dataset_download_files(
        'dschettler8845/siim-covid19-updated-train-labels', path=os.getenv('DATASET_PATH')
    )
    api.competition_download_files(
        'siim-covid19-detection', path=os.getenv('DATASET_PATH'))


if __name__ == '__main__':
    download_datasets()
