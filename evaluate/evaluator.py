import pandas as pd
import joblib
import glob
import os
from data import DataUtils, DataManager


DEFAULT_STOCK_NUM = ' 066570'


class BoughtStock:
    stock_num = ''
    stock_name = ''
    bought_price = 0
    close_price = 0
    holding_period = 0

    def __init__(self, _stock_num, _stock_name, _bought_price, holding_period):
        self.stock_num = _stock_num
        self.stock_name = _stock_name
        self.bought_price = _bought_price

    def set_close_price(self, _close_price):
        self.close_price = _close_price
        self.holding_period += 1

    def get_bought_price(self):
        return self.bought_price

    def get_holding_period(self):
        return self.holding_period

    def __str__(self):
        return self.stock_num + '(' + self.stock_name + ') - Bought: ' + self.bought_price + ', Close: ' + \
               self.close_price + ', Earn: ' + str(round((self.close_price - self.bought_price)/self.bought_price, 2))


def get_eval_days():
    df = pd.read_csv(DataUtils.get_raw_data_path() + DEFAULT_STOCK_NUM + '.csv')
    return df.index[:200]


def evaluate_model():
    trained_model = joblib.load(DataUtils.get_model_data_path())


    stock_file_list = glob.glob('./data/raw_data/*.csv')
    for idx, stock_file in enumerate(stock_file_list):
        stock_file = os.path.basename(stock_file)
        stock_num = os.path.splitext(stock_file)[0]
        df_train, df_eval, expected_value = DataManager.get_stock_info(stock_num)


print(get_eval_days())
