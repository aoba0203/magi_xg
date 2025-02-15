from data import StockManager, StockInfoGather, DatasetGenerator, DataUtils
import os
from utils import utils

CONFIG_DATA_SECTION = 'Data'
CONFIG_OPTION_UPDATE_DATE = 'update_date'


def data_save_and_update():
    print('-Start raw data update')
    updated = utils.get_config_value(CONFIG_DATA_SECTION, CONFIG_OPTION_UPDATE_DATE)
    if updated != utils.get_today():
        stock_list = StockManager.get_stock_num_list()
        StockInfoGather.save_and_update_info(stock_list)
        utils.set_config_value(CONFIG_DATA_SECTION, CONFIG_OPTION_UPDATE_DATE, utils.get_today())
    print('--Data Update Done')


def get_stock_list():
    return StockManager.get_stock_num_list()


def get_kospi_list():
    return StockManager.get_kospi_list()


def get_num_to_name(_stock_num):
    return StockManager.get_stock_num_to_name(_stock_num)


def get_stock_info_all(_stock_num):
    df_dataset, d, f = DatasetGenerator.get_stock_info_all(_stock_num)
    return df_dataset, d, f


def get_stock_info(_stock_num):
#     updated = utils.get_config_value(CONFIG_DATA_SECTION, CONFIG_OPTION_UPDATE_DATE)
#     if updated != utils.get_today():
#         data_save_and_update()
    df_train, df_eval, v_range = DatasetGenerator.get_stock_info(_stock_num)
    expected_value = v_range[1]
    return df_train, df_eval, expected_value


def get_temp_data_path():
    return DataUtils.get_temp_data_path()


def update_raw_file():
    raw_data_path = DataUtils.get_raw_data_path()
    raw_file_list = os.listdir(raw_data_path)
    stock_list = get_stock_list()
    for raw_file in raw_file_list:
        _stock_file = os.path.basename(raw_file)
        stock_num = os.path.splitext(_stock_file)[0]
        if stock_num not in stock_list:
            os.remove(raw_data_path + raw_file)
            print('not in stock_list: ' + str(stock_num))



