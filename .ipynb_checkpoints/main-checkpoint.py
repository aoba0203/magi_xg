from utils import utils
from data import DataManager as DM
from train import model_xgboost as xgTrain

import warnings
import os
import glob
from multiprocessing import Pool
import sys
# import tqdm
from tqdm import *

warnings.filterwarnings(action='ignore')
# warnings.filterwarnings(action='default')

class Stock:
    stock_name = ''
    accuracy_test = 0
    accuracy_eval = 0
    expected_value = 0
    buy_percent = 0
    predict_sell = 0
    predict_hold = 0
    predict_buy = 0

    def __init__(self, _stock_name, _acc_test, _acc_eval, _expected_value, _buy_percent, _pred_sell, _pred_hold, _pred_buy):
        self.stock_name = _stock_name
        self.accuracy_test = _acc_test
        self.accuracy_eval = _acc_eval
        self.expected_value = _expected_value
        self.buy_percent = _buy_percent
        self.predict_sell = _pred_sell
        self.predict_hold = _pred_hold
        self.predict_buy = _pred_buy

    def __str__(self):
        return str(self.stock_name) + ' ,' + str(round(self.accuracy_test, 4)) + ',' + str(round(self.accuracy_eval, 4)) + ',' + \
                str(round(self.expected_value, 4)) + ',' + str(round(self.buy_percent, 4)) + ',' + \
                str(round(self.predict_sell, 4)) + ',' + str(round(self.predict_hold, 4)) + ',' + str(round(self.predict_buy, 4))

    def __repr__(self):
        return str(self.stock_name) + ' ,' + str(round(self.accuracy_test, 4)) + ',' + str(round(self.accuracy_eval, 4)) + ',' + \
                str(round(self.expected_value, 4)) + ',' + str(round(self.buy_percent, 4)) + ',' + \
                str(round(self.predict_sell, 4)) + ',' + str(round(self.predict_hold, 4)) + ',' + str(round(self.predict_buy, 4))


DM.data_save_and_update()


predict_stock_diction = {}


def __train_xgmodel(_stock_file):
    global predict_stock_diction
    
    _stock_file = os.path.basename(_stock_file)
    stock_num = os.path.splitext(_stock_file)[0]
    df_train, df_eval, expected_value = DM.get_stock_info(stock_num)
    model, accuracy_test = xgTrain.train_model(stock_num, df_train)
    accuracy_eval, buy_percent = xgTrain.evaluate_model(model, stock_num, df_eval)
    today_set = df_eval.iloc[:1, :-1]
    predicted = xgTrain.predict_today(model, stock_num, today_set)
    pred_sell, pred_hold, pred_buy = predicted[0], predicted[1], predicted[2]
    stock_name = DM.get_num_to_name(stock_num)
    predict_stock_diction[stock_num] = Stock(stock_name, accuracy_test, accuracy_eval, expected_value, buy_percent, pred_sell, pred_hold, pred_buy)
    return


# +
stock_file_list = glob.glob('./data/raw_data/*.csv')

pool = Pool()
for i, _ in enumerate(pool.map(__train_xgmodel, stock_file_list)):
    pass
print('Done {0:%}'.format(i/len(stock_file_list)))
# -

stock_file_list = glob.glob('./data/raw_data/*.csv')
pool = Pool()
for i, _ in enumerate(pool.map(__train_xgmodel, stock_file_list)):
    print('Done {0:%}'.format(i/len(stock_file_list)))

stock_file_list = glob.glob('./data/raw_data/*.csv')
pool = Pool()
with tqdm(total=len(stock_file_list)) as pbar:
    for _ in tqdm(pool.imap_unordered(__train_xgmodel, stock_file_list), total=len(stock_file_list)):
        pbar.update()



if __name__ == '__main__':
    predict_stock_dic = {}
#     DM.data_save_and_update()
    stock_file_list = os.listdir('./data/')
    for idx, stock_file in enumerate(stock_file_list):
        if os.path.splitext(stock_file)[1] != '.csv':
            continue
        stock_num = os.path.splitext(stock_file)[0]
        print('--Train start: ' + str(idx) + '/' + str(len(stock_file_list)) + ', target:' + stock_num)
        df_train, df_eval, expected_value = DM.get_stock_info(stock_num)
        accuracy_test = xgTrain.train_model(stock_num, df_train)
        accuracy_eval, buy_percent = xgTrain.evaluate_model(stock_num, df_eval)
        today_set = df_eval.iloc[:1, :-1]
        predicted = xgTrain.predict_today(stock_num, today_set)
        pred_sell, pred_hold, pred_buy = predicted[0], predicted[1], predicted[2]
        stock_name = DM.get_num_to_name(stock_num)
        predict_stock_dic[stock_num] = Stock(stock_name, accuracy_test, accuracy_eval, expected_value, buy_percent, pred_sell, pred_hold, pred_buy)
        print('-Train End: ' + str(stock_num))
    utils.write_dictionary_to_csv(predict_stock_dic, 'predict_1.csv')
    print('-All End')

os.path.splitext(os.listdir('./data/raw_data/')[0])[1]


