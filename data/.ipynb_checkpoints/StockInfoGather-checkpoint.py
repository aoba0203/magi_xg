from bs4 import BeautifulSoup
import urllib
from urllib import parse, request
import requests
import pandas as pd
import os
import sys
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from datetime import date, timedelta
from multiprocessing import Pool

from data import DataUtils

FOLDER_RAW = DataUtils.get_raw_data_path()


def __get_last_page_num_demand(stock_num):
    content = requests.get(('http://finance.naver.com/item/frgn.nhn?code=' + stock_num)).text
    soup = BeautifulSoup(content, features='lxml')
    return __get_last_page(soup)


def __get_last_page(soup):
    pgrrs = soup.findAll('td', {'class': 'pgRR'})
    if len(pgrrs) == 0:
        return 0
    parsed = parse.urlparse(pgrrs[0].a['href'])
    parsed_qs = parse.parse_qs(parsed.query, keep_blank_values=True)
    return int(parsed_qs['page'][0])


def __parse_stock_info(stock_num, page_num):
    global stock_info
    # parse index- end | diff | open | high | low | volume
    parse_url = 'http://finance.naver.com/item/sise_day.nhn?code=' + stock_num + '&page=' + page_num
    soup = BeautifulSoup(request.urlopen(parse_url), 'lxml')
    elements_day = soup.findAll('td', {'align': 'center'})
    elements_num = soup.findAll('td', {'class': 'num'})

    count = 0
    diff = 1
    for elements in elements_day:
        info = []
        day = elements.text
        info.append(day)
        for idx in range(6):
            idx += (count * 6)
            if len(elements_num[idx].text) == 1:
                continue
            parse_value = int(elements_num[idx].text.replace(',', ''))
            if idx % 6 == 1:
                if parse_value == 0:
                    diff = 0
                elif 'ico_down.gif' in elements_num[idx].img['src']:
                    # elif elements_num[idx].img['src'] == 'http://imgstock.naver.com/images/images4/ico_down.gif':
                    diff = -1
            parsed_info = diff * int(elements_num[idx].text.replace(',', ''))
            info.append(parsed_info)
            diff = 1
        count += 1
        stock_info.append(info)


def __parse_stock_demand(stock_num, page_num):
    global stock_demand
    # parse index- day | agency | foreign
    parse_url = 'http://finance.naver.com/item/frgn.nhn?code=' + stock_num + '&page=' + page_num
    soup = BeautifulSoup(request.urlopen(parse_url), 'lxml')
    elements = soup.findAll('tr', {'onmouseover': 'mouseOver(this)'})

    for element in elements:
        demand = []
        text_array = element.text.split()
        for idx in range(len(text_array)):
            if idx % 9 == 0: demand.append(text_array[idx])
            if idx % 9 == 5: demand.append(float(text_array[idx].replace(',', '')))
            if idx % 9 == 6: demand.append(float(text_array[idx].replace(',', '')))
        stock_demand.append(demand)


def __get_stock_dataframe_from_csv(stock_num):
    df = pd.read_csv(FOLDER_RAW + '/' + stock_num + '.csv', index_col=0)
    return df


def __update_stock_info(stock_num):
    global stock_info
    global stock_demand
    stock_info = []
    stock_demand = []
    df_csv = __get_stock_dataframe_from_csv(stock_num)
    __parse_stock_info(stock_num, '1')
    __parse_stock_info(stock_num, '2')
    __parse_stock_demand(stock_num, '1')
    df_info = pd.DataFrame(stock_info)
    df_demand = pd.DataFrame(stock_demand)
    df_info.set_index(0, inplace=True)
    df_demand.set_index(0, inplace=True)
    df_update = (pd.concat([df_info, df_demand], axis=1)).sort_index(ascending=False)
    df_update.columns = ['close', 'diff', 'open', 'high', 'low', 'volume', 'agency', 'foreign']
    #     df_update = __update_add_stock_fundamental(df_update, stock_num)

    df_result = df_csv.combine_first(df_update)
    df_result.sort_index(inplace=True, ascending=False)
    df_result.to_csv(FOLDER_RAW + '/' + stock_num + '.csv')
    return df_result


def __get_stock_dataframe_from_web(stock_num, last_page_num):
    global stock_info
    global stock_demand

    stock_info = []
    stock_demand = []
#     last_page_num = __get_last_page_num_demand(stock_num)
    for page_num in range(1, (last_page_num * 2)):
        __parse_stock_info(stock_num, str(page_num))
    #         std_print_overwrite('Parsing Progress: ' + str(round(float((count * 100.0) / max_page_num), 1)) + ' %')
    for page_num in range(1, last_page_num):
        __parse_stock_demand(stock_num, str(page_num))
    #         std_print_overwrite('Parsing Progress: ' + str(round(float((count * 100.0) / max_page_num), 1)) + ' %')
    df_info = pd.DataFrame(stock_info)
    df_demand = pd.DataFrame(stock_demand)
    df_info.set_index(0, inplace=True)
    df_demand.set_index(0, inplace=True)
    df_info = df_info.dropna()
    df_demand = df_demand.dropna()
    # print(stock_num, ': ', df_info.shape, ', ', df_demand.shape)
    if df_info.shape[0] > df_demand.shape[0]:
        df_info = df_info[:df_demand.shape[0]]
    elif df_info.shape[0] < df_demand.shape[0]:
        df_demand = df_demand[:df_info.shape[0]]
    df = pd.concat([df_info, df_demand], axis=1)
    df.sort_index(inplace=True, ascending=False)
    df = df.dropna()
    df.columns = ['close', 'diff', 'open', 'high', 'low', 'volume', 'agency', 'foreign']
#     df = __add_stock_fundamental(df, stock_num)
    df.to_csv(FOLDER_RAW + '/' + stock_num + '.csv')
    return df


def __save_update_stock_info(stock_num):
    if not os.path.exists(FOLDER_RAW):
        os.makedirs(FOLDER_RAW)
    try:
        
        if not os.path.exists(FOLDER_RAW + '/' + stock_num + '.csv'):
            last_page_num = __get_last_page_num_demand(stock_num)
            if last_page_num < 50:
                return
            __get_stock_dataframe_from_web(stock_num, last_page_num)
        else:
            __update_stock_info(stock_num)
    except:
        print('Except: ', stock_num)
        # if __is_need_update(stock_num):
        #     df_stock_info = __update_stock_info(stock_num)
        # else:
        #     df_stock_info = __get_stock_dataframe_from_csv(stock_num)
#     df_stock_info = __add_stock_fundamental(df_stock_info, stock_num)

    return
#     return df_stock_info.dropna()

def save_and_update_info(stock_list):
    pool = Pool()
    for i, _ in enumerate(pool.map(__save_update_stock_info, stock_list)):
#         sys.stderr.write('/rDone {0:%}'.format(i/len(stock_list)))
        pass
#     for i, stock_num in enumerate(stock_list):
#         print(str(i) + '/' + str(len(stock_list)) + ': ' + str(stock_num))
#         __save_update_stock_info(stock_num)
#         if i == 2:
#             break


if __name__ == '__main__':
    print(FOLDER_RAW)
