from xgboost import XGBClassifier
import xgboost as xgb
import pandas as pd
import numpy as np
from data import DataUtils
from sklearn.model_selection import train_test_split
import multiprocessing
import joblib

FOLDER_XG = DataUtils.get_xg_data_path()
FOLDER_MODEL = DataUtils.get_model_data_path()


def __get_model_file_path(_stock_num):
    return FOLDER_MODEL + 'xgboost_' + _stock_num + '.joblib'


def __get_xgb_model():
    model = xgb.XGBClassifier(
                objective='multi:softmax',
                colsample_bytree=0.3145282052214442,
                learning_rate=0.1,
                max_depth=128,
                alpha=0.00021890725668370222,
                n_estimators=501,
                n_jobs=10,
                gamma=float(3.6961082548762185e-06),
                subsample=0.9379749659257777,
                eta=0.006468846947776807,
                reg_lambda=0.0017145976534277546,
#                 thread=multiprocessing.cpu_count()*4,
                min_child_weight=float(1.0800292877514307e-05),
#                 gpu_id=0,
#                 tree_method='gpu_hist'                
    )
    return model


def train_model_all_data(_stock_num, _train_set):
    train_x, train_y = _train_set.iloc[:, :-1], _train_set.iloc[:, -1]
    model = __get_xgb_model()
    model.fit(train_x, train_y)
    return model


def train_model(_stock_num, _train_set):
    train, test = train_test_split(_train_set, test_size=0.2)
    train_x, train_y = train.iloc[:, :-1], train.iloc[:, -1]
    test_x, test_y = test.iloc[:, :-1], test.iloc[:, -1]
    model = __get_xgb_model()
    model.fit(train_x, train_y)
    accuracy_test = sum(model.predict(test_x) == test_y) / len(test_y)
#     joblib.dump(model, __get_model_file_path(_stock_num))
    return model, accuracy_test


def evaluate_model(trained_model, _stock_num, _eval_set, threshold=0.70):
#     trained_model = joblib.load(__get_model_file_path(_stock_num))
    eval_x, eval_y = _eval_set.iloc[:, :-1], _eval_set.iloc[:, -1]
    predict = trained_model.predict_proba(eval_x)
    total_count = 0
    correct_count = 0
    buy_count = 1
    true_buy_count = 0
    for i, predict_arr in enumerate(predict):
        idx = np.argmax(predict_arr)
        if predict_arr[idx] > threshold:
            total_count += 1
            if (idx+1) == np.array(eval_y)[i]:
                correct_count += 1
            if (idx+1) == 3:
                buy_count += 1
                if np.array(eval_y)[i] == 3:
                    true_buy_count += 1
    accuracy_eval = correct_count / total_count
    buy_percent = true_buy_count / len(eval_y)
    return accuracy_eval, buy_percent


def predict_today(trained_model, _stock_num, _today_set):
#     trained_model = joblib.load(__get_model_file_path(_stock_num))
    return trained_model.predict_proba(_today_set)[0]
