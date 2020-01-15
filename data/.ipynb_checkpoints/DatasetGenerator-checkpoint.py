import pandas as pd
import numpy as np
from data import DataUtils

FOLDER_XG = DataUtils.get_xg_data_path()
FOLDER_RAW = DataUtils.get_raw_data_path()


def __set_extra_info(_df):
    # _df['open_next'] = _df['open'].shift()
    # _df['close_next'] = _df['close'].shift()
    _df['candle_size'] = (((_df['close'] - _df['open']) / _df['open']) * 100.0)
    _df['percent'] = (_df['diff'] / _df['close'].shift(-1)) * 100
    _df['volume'] = _df['volume'] / 10000.
    _df['foreign'] = (_df['foreign'] * _df['close'])
    _df['agency'] = (_df['agency'] * _df['close'])
    return _df


def __set_mv_grad(_df):
    for duration in [3, 5, 10, 20, 60, 120, 200]:
        _df['mv_value' + str(duration)] = _df['close'].rolling(duration).mean().shift(-(duration - 1))
        _df['mv_value' + str(duration) + '_grad'] = np.flip(
            np.gradient(_df['mv_value' + str(duration)].sort_index().values), 0)
        _df['mv_volume' + str(duration)] = _df['volume'].rolling(duration).mean().shift(-(duration - 1))
        _df['mv_volume' + str(duration) + '_grad'] = np.flip(
            np.gradient(_df['mv_volume' + str(duration)].sort_index().values), 0)

        _df['mv_foreign' + str(duration)] = _df['foreign'].rolling(duration).mean().shift(-(duration - 1))
        _df['mv_foreign' + str(duration) + '_grad'] = np.flip(
            np.gradient(_df['mv_foreign' + str(duration)].sort_index().values), 0)
        _df['mv_agency' + str(duration)] = _df['agency'].rolling(duration).mean().shift(-(duration - 1))
        _df['mv_agency' + str(duration) + '_grad'] = np.flip(
            np.gradient(_df['mv_agency' + str(duration)].sort_index().values), 0)
    return _df


def __set_period_max(_df, periods=5):
    _df['close_high'] = _df['close'].copy().shift().sort_index(ascending=False).rolling(periods, min_periods=1).max().sort_index()
    # _df = _df.dropna()
    _df['close_high'] -= _df['close']
    _df['close_high'] /= _df['close']
    _df['close_high'] *= 100
    return _df


def __get_value_range(df):
    value = df['close_high'].values.copy()
    value.sort()
    v_len = len(value)
    v_range = int(v_len / 3)
    return value[int(v_range)], value[2 * int(v_range)]


def __set_predict_category(df):
    v_range = __get_value_range(df)
    df['target'] = df[['close_high']].copy()
    df['target'][df['close_high'] >= v_range[1]] = 3
    df['target'][(df['close_high'] < v_range[1]) & (df['close_high'] > v_range[0])] = 2
    df['target'][df['close_high'] <= v_range[0]] = 1

    df_y = df[['target']]
#     df_y = df_y.reset_index()
#     df_y = df_y.drop(df_y.columns[0], axis=1)
    return df, df_y


def __drop_columns(df):
    #     drop_columns = ['close_high', 'close_next', 'open_next', 'target']
    drop_columns = ['close_high', 'target']
    for drop_column in drop_columns:
        df = df.drop(drop_column, axis=1)
    return df


def __get_stacked_dataset(_df):
    data_list = []
    columns = []

    for idx in range(len(_df) - 5):
        data_list.append(_df.iloc[idx:idx + 5].values.flatten())

    for i in range(5):
        for column in _df.columns:
            columns.append(str(i) + '_' + column)
    return pd.DataFrame(data_list, columns=columns)


def __get_dataframe(_stock_num):
    df_ori = pd.read_csv(FOLDER_RAW + _stock_num + '.csv', index_col=0)
    df_ori = df_ori.dropna()
    __set_extra_info(df_ori)
    __set_mv_grad(df_ori)
    df_ori = __set_period_max(df_ori)
    value_range = __get_value_range(df_ori)
    df_ori, df_y = __set_predict_category(df_ori)
    df_ori = __drop_columns(df_ori)
    df_indexs = df_ori.index.copy()
    df_ori = df_ori.reset_index()    
    df_ori = df_ori.drop(df_ori.columns[0], axis=1)
    df_ori = __get_stacked_dataset(df_ori)
    df_ori.index = df_indexs[:len(df_ori)]
    df_ori = df_ori.dropna()

    dataset = pd.concat([df_ori, df_y], axis=1, join='inner')    
    dataset.to_csv(FOLDER_XG + _stock_num + '.csv')
    df_train, df_eval = dataset[200:], dataset[:200]
    return df_train, df_eval, value_range


def __get_dataframe_all(_stock_num):
    df_ori = pd.read_csv(FOLDER_RAW + _stock_num + '.csv', index_col=0)
    __set_extra_info(df_ori)
    __set_mv_grad(df_ori)
    df_ori = __set_period_max(df_ori)
    value_range = __get_value_range(df_ori)
    df_ori, df_y = __set_predict_category(df_ori)
    df_ori = __drop_columns(df_ori)
    df_indexs = df_ori.index.copy()
    df_ori = df_ori.reset_index()    
    df_ori = df_ori.drop(df_ori.columns[0], axis=1)
    df_ori = __get_stacked_dataset(df_ori)
    df_ori.index = df_indexs[:len(df_ori)]
    df_ori = df_ori.dropna()

    dataset = pd.concat([df_ori, df_y], axis=1, join='inner')    
    dataset = dataset.dropna()
    return dataset, df_ori, df_y


def get_stock_info(_stock_num):
    df_train, df_eval, v_range = __get_dataframe(_stock_num)
    # df_train.to_csv(FOLDER_XG + _stock_num + '.csv')
    return df_train, df_eval, v_range


def get_stock_info_all(_stock_num):
    df_dataset = __get_dataframe_all(_stock_num)
    # df_train.to_csv(FOLDER_XG + _stock_num + '.csv')
    return df_dataset


