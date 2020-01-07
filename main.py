from utils import utils
from data import DataManager as DM
from train import model_xgboost as xgTrain


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

    def __str__(self) -> str:
        return str(self.stock_name) + ',' + str(self.accuracy_test) + ',' + str(self.accuracy_eval) + ',' + \
                str(self.expected_value) + '.' + str(self.buy_percent) + ',' + \
                str(self.predict_sell) + ',' + str(self.predict_hold) + ',' + str(self.predict_buy)

    def __repr__(self) -> str:
        return str(self.stock_name) + ',' + str(self.accuracy_test) + ',' + str(self.accuracy_eval) + ',' + \
               str(self.expected_value) + '.' + str(self.buy_percent) + ',' + \
               str(self.predict_sell) + ',' + str(self.predict_hold) + ',' + str(self.predict_buy)


if __name__ == '__main__':
    predict_stock_dic = {}
    DM.data_save_and_update()
    stock_num_list = DM.get_stock_list()
    for idx, stock_num in enumerate(stock_num_list):
        print('--Train start: ' + str(stock_num))
        df_train, df_eval, expected_value = DM.get_stock_info(stock_num)
        accuracy_test = xgTrain.train_model(stock_num, df_train)
        accuracy_eval, buy_percent = xgTrain.evaluate_model(stock_num, df_eval)
        today_set = df_eval.iloc[:1, :-1]
        predicted = xgTrain.predict_today(stock_num, today_set)
        pred_sell, pred_hold, pred_buy = predicted[0], predicted[1], predicted[2]
        stock_name = DM.get_num_to_name(stock_num)
        predict_stock_dic[stock_num] = Stock(stock_name, accuracy_test, accuracy_eval, expected_value, buy_percent, pred_sell, pred_hold, pred_buy)
        print('-Train End: ' + str(stock_num))
        if idx == 2:
            break
    utils.write_dictionary_to_csv(predict_stock_dic, 'predict.csv')
    print('-All End')

