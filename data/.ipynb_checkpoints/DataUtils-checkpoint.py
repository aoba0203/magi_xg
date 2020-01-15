import os


def get_raw_data_path():
    paths = os.getcwd() + '/data/raw_data/'
    if not os.path.exists(paths):
        os.makedirs(paths)
    return paths


def get_xg_data_path():
    paths = os.getcwd() + '/data/xg_data/'
    if not os.path.exists(paths):
        os.makedirs(paths)
    return paths

def get_model_data_path():
    paths = os.getcwd() + '/data/model_data/'
    if not os.path.exists(paths):
        os.makedirs(paths)
    return paths


def get_temp_data_path():
    paths = os.getcwd() + '/data/temp_data/'
    if not os.path.exists(paths):
        os.makedirs(paths)
    return paths
