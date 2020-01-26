import pandas as pd
import joblib
import glob
import os
from data import DataUtils, DataManager


DEFAULT_STOCK_NUM = '066570'


class BoughtStock:
    close_price = 0

    def __init__(self, _stock_num, _stock_name, _bought_day, _bought_price, _holding_period=5):
        self.stock_num = _stock_num
        self.stock_name = _stock_name
        self.bought_day = _bought_day
        self.bought_price = _bought_price
        self.holding_period = _holding_period
        self.stock_df = pd.read_csv(DataUtils.get_raw_data_path() + _stock_num + '.csv', index_col=0)

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


class PredStock:
    def __init__(self, _stock_num, _sell, _hold, _buy):
        self.stock_num = _stock_num
        self.pred_sell = _sell
        self.pred_hold = _hold
        self.pred_buy = _buy

    def get_stock_num(self):
        return self.stock_num

    def get_pred_sell(self):
        return self.pred_sell

    def get_pred_hold(self):
        return self.pred_hold

    def get_pred_buy(self):
        return self.pred_buy


def select_buy_stock(_stock_pred_list):
    _stock_pred_list.sort(key=lambda x: x.get_pred_buy)
    return _stock_pred_list[0], _stock_pred_list[1]


def get_eval_days():
    df = pd.read_csv(DataUtils.get_raw_data_path() + DEFAULT_STOCK_NUM + '.csv', index_col=0)
    return df.index.values[:200]


def evaluate_model():
    day_list = sorted(get_eval_days())

    for day in day_list:
        stock_pred_list = []
        stock_file_list = glob.glob('./data/raw_data/*.csv')
        for idx, stock_file in enumerate(stock_file_list):
            stock_file = os.path.basename(stock_file)
            stock_num = os.path.splitext(stock_file)[0]
            dataset_day = DataManager.get_data_at_day(stock_num, day)

            trained_model = joblib.load(DataUtils.get_model_name_path(stock_num))
            predict = trained_model.predict_proba(dataset_day)
            stock_pred_list.append(PredStock(stock_num, predict[0], predict[1], predict[2]))
        selected1, selected2 = select_buy_stock(stock_pred_list)



print(sorted(get_eval_days()))
