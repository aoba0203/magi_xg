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
import time

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


DM.update_raw_file()

df_train.head()

df_dataset

if __name__ == '__main__':
    first_time = time.time()
    predict_stock_dic = {}
#     DM.data_save_and_update()
    stock_file_list = glob.glob('./data/raw_data/*.csv')
    for idx, stock_file in enumerate(stock_file_list):
#         if os.path.splitext(stock_file)[1] != '.csv':
#             continue
        start_time = time.time()
        stock_file = os.path.basename(stock_file)        
        stock_num = os.path.splitext(stock_file)[0]
        print('--Train start: ' + str(idx) + '/' + str(len(stock_file_list)) + ', target:' + stock_num)
        df_train, df_eval, expected_value = DM.get_stock_info(stock_num)
        model,accuracy_test = xgTrain.train_model(stock_num, df_train)
        accuracy_eval, buy_percent = xgTrain.evaluate_model(model, stock_num, df_eval)
        
        today_set = df_eval.iloc[:1, :-1]        
        df_dataset, df_ori, df_y = DM.get_stock_info_all(stock_num)
        pred_model = xgTrain.train_model_all_data(stock_num, df_dataset)
        predicted = xgTrain.predict_today(pred_model, stock_num, today_set)
        pred_sell, pred_hold, pred_buy = predicted[0], predicted[1], predicted[2]
        stock_name = DM.get_num_to_name(stock_num)
        predict_stock_dic[stock_num] = Stock(stock_name, accuracy_test, accuracy_eval, expected_value, buy_percent, pred_sell, pred_hold, pred_buy)
        print('-Train End: ' + str(stock_num) + ', time: ' + str(time.time() - start_time))
    utils.write_dictionary_to_csv(predict_stock_dic, 'predict_' + utils.get_today() + '.csv')
    print('-All End: ' + str(time.time() - first_time))





if __name__ == '__main__':
    first_time = time.time()
    predict_stock_dic = {}
#     DM.data_save_and_update()
    stock_file_list = glob.glob('./data/raw_data/*.csv')
    for idx, stock_file in enumerate(stock_file_list):
#         if os.path.splitext(stock_file)[1] != '.csv':
#             continue
        start_time = time.time()
        stock_file = os.path.basename(stock_file)        
        stock_num = os.path.splitext(stock_file)[0]
        print('--Train start: ' + str(idx) + '/' + str(len(stock_file_list)) + ', target:' + stock_num)
        df_train, df_eval, expected_value = DM.get_stock_info(stock_num)
        model,accuracy_test = xgTrain.train_model(stock_num, df_train)
        accuracy_eval, buy_percent = xgTrain.evaluate_model(model, stock_num, df_eval)
        
        today_set = df_eval.iloc[:1, :-1]        
        df_dataset = DM.get_stock_info_all(stock_num)
        pred_model = xgTrain.train_model_all_data(stock_num, df_dataset)
        predicted = xgTrain.predict_today(pred_model, stock_num, today_set)
        pred_sell, pred_hold, pred_buy = predicted[0], predicted[1], predicted[2]
        stock_name = DM.get_num_to_name(stock_num)
        predict_stock_dic[stock_num] = Stock(stock_name, accuracy_test, accuracy_eval, expected_value, buy_percent, pred_sell, pred_hold, pred_buy)
        print('-Train End: ' + str(stock_num) + ', ' + stock_name + ', Acc: ' + str(round(accuracy_test, 2)) + ', ' + str(round(accuracy_eval, 2)) + ', time: ' + str(time.time() - start_time))
    utils.write_dictionary_to_csv(predict_stock_dic, 'predict_' + utils.get_today() + '.csv')
    print('-All End: ' + str(time.time() - first_time))

'008560.csv' in os.listdir('data/raw_data/')

df = pd.read_csv('pred')

df = pd.read_csv('predict_1.csv')

df

# df = pd.read_csv('predict_1.csv')
df.to_csv('result/raw/' + utils.get_today() + '_pred.csv')
df[(df.pred_buy > 0.7) & (df.acc_test > 0.55) & (df.acc_eval > 0.25)].sort_values('pred_buy', ascending=False).head(11)



def __write_temp_stock_info(_stock_num, _stock):
    temp_path = DM.get_temp_data_path()
    temp_file_name = temp_path + _stock_num + '_1.csv'
    with open(temp_file_name, 'w') as temp_file:
        temp_file.write(str(_stock_num) + ',' + str(_stock))

# def __is_need_to_train():
    

def __train_xgmodel(_stock_file):    
    _stock_file = os.path.basename(_stock_file)
    stock_num = os.path.splitext(_stock_file)[0]
    print('--train: ' + stock_num)
    start_time = time.time()
    df_train, df_eval, expected_value = DM.get_stock_info(stock_num)
    model, accuracy_test = xgTrain.train_model(stock_num, df_train)
    accuracy_eval, buy_percent = xgTrain.evaluate_model(model, stock_num, df_eval)
    today_set = df_eval.iloc[:1, :-1]
    predicted = xgTrain.predict_today(model, stock_num, today_set)
    pred_sell, pred_hold, pred_buy = predicted[0], predicted[1], predicted[2]
    stock_name = DM.get_num_to_name(stock_num)
    stock = Stock(stock_name, accuracy_test, accuracy_eval, expected_value, buy_percent, pred_sell, pred_hold, pred_buy)
    __write_temp_stock_info(stock_num, stock)
    print('-Train End: ' + str(stock_num) + ', ' + stock_name + ', Acc: ' + str(round(accuracy_test, 2)) + ', ' + str(round(accuracy_eval, 2)) + ', time: ' + str(time.time() - start_time))
    return


def __results_summary_to_csv():
    temp_path = DM.get_temp_data_path()
    summary_file_path = temp_path + 'sum.csv'
    if os.path.exists(summary_file_path):
        os.remove(summary_file_path)
    
    temp_stock_file_list = glob.glob(temp_path + '*.csv')
    stock_list = []
    for idx, temp_file in enumerate(temp_stock_file_list):
        with open(temp_file, 'r') as temp_file:
            stock_list.append(temp_file.read())
    print(len(stock_list))
    with open(temp_path + 'sum.csv', 'w') as temp_file:
        temp_file.write('stock_name,acc_test,acc_eval,expected_value,buy_percent,pred_sell,pred_hold,pred_buy\r\n')
        for stock_info in stock_list:
            temp_file.writelines(stock_info)
            temp_file.write('\r\n')


# +
stock_file_list = glob.glob('./data/raw_data/*.csv')

for idx, stock_file in enumerate(stock_file_list):
    __train_xgmodel(stock_file)
    if idx == 3:
        break
# -

stock_file_list = glob.glob('./data/raw_data/*.csv')
start_time = time.time()
pool = Pool(processes=4)
pool.map(__train_xgmodel, stock_file_list)
# pool.join()
# pool.close()
__results_summary_to_csv()
print('total time: ', str(time.time() - start_time))

stock_file_list = glob.glob('./data/raw_data/*.csv')
pool = Pool(processes=4)
with tqdm(total=len(stock_file_list)) as pbar:
    for _ in tqdm(pool.imap_unordered(__train_xgmodel, stock_file_list), total=len(stock_file_list)):
        pbar.update()
    pool.join()
    pool.close()
__results_summary_to_csv()

__results_summary_to_csv()

pd.read_csv(DM.get_temp_data_path + 'sum.csv')



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
pool.map(__train_xgmodel, stock_file_list)
pool.join()
pool.close()

# +
stock_file_list = glob.glob('./data/raw_data/*.csv')

pool = Pool()
for i, _ in enumerate(pool.map(__train_xgmodel, stock_file_list)):
    pass
print('Done {0:%}'.format(i/len(stock_file_list)))
# -

stock_file_list = glob.glob('./data/raw_data/*.csv')
pool = Pool()
with tqdm(total=len(stock_file_list)) as pbar:
    for _ in tqdm(pool.imap_unordered(__train_xgmodel, stock_file_list), total=len(stock_file_list)):
        pbar.update()

write_dictionary_to_csv(predict_stock_dic, 'predict_2.csv')


def write_dictionary_to_csv(dictionary, csv_file_name):
    try:
        with open(csv_file_name, 'w') as csv_file:
            csv_file.write('stock_name,acc_test,acc_eval,expected_value,buy_percent,pred_sell,pred_hold,pred_buy\r\n')
            for key, value in dictionary.items():
                csv_file.write(str(key) + ',' + str(value))
                csv_file.write('\r\n')
    except IOError:
        print('except')


import pandas as pd

# pd.read_csv('predict_2.csv').sort_values('pred_buy')
df = pd.read_csv('predict_1.csv')

df.sort_values('acc_test', ascending=False)

len(DM.get_stock_list())

stock_list = DM.get_stock_list()
for _file in glob.glob('data/raw_data/*.csv'):
    stock_file = os.path.basename(_file)        
    stock_num = os.path.splitext(stock_file)[0]
    if stock_num in stock_list:
        pass
    else:
        os.remove(_file)        

len(glob.glob('data/raw_data/*.csv'))

stock_list in '005930'


