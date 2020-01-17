import os
from utils import utils


def get_raw_data_path():
    paths = utils.get_project_path() + '/data/raw_data/'
    if not os.path.exists(paths):
        os.makedirs(paths)
    return paths


def get_xg_data_path():
    paths = utils.get_project_path() + '/data/xg_data/'
    if not os.path.exists(paths):
        os.makedirs(paths)
    return paths


def get_model_data_path():
    paths = utils.get_project_path() + '/data/model_data/'
    if not os.path.exists(paths):
        os.makedirs(paths)
    return paths


def get_temp_data_path():
    paths = utils.get_project_path() + '/data/temp_data/'
    if not os.path.exists(paths):
        os.makedirs(paths)
    return paths
