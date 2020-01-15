from bs4 import BeautifulSoup
import os
import re
import requests
from utils import utils


CONFIG_STOCK_SECTION = 'Stock'
CONFIG_OPTION_KOSPI_LIST = 'kospi_list'

mStock_num_dic = {}
mStock_name_dic = {}
mStock_in_kospi = []


def __get_dic_data_path():
    paths = os.getcwd() + '/data/dic_data/'
    if not os.path.exists(paths):
        os.makedirs(paths)
    return paths


DIC_NAME_FILE = __get_dic_data_path() + utils.get_this_month() + '_stock_name_dic.csv'
DIC_NUM_FILE = __get_dic_data_path() + utils.get_this_month() + '_stock_num_dic.csv'


def __set_stock_num_in_kospi():
    global mStock_in_kospi
    
    stock_list = ' ,'.join(mStock_in_kospi)
    utils.set_config_value(CONFIG_STOCK_SECTION, CONFIG_OPTION_KOSPI_LIST, stock_list)


def __get_stock_num_in_kospi():
    global mStock_in_kospi
    
    stock_list = utils.get_config_value(CONFIG_STOCK_SECTION, CONFIG_OPTION_KOSPI_LIST)
    if stock_list == 0:
        __parse_stock_dictionary()
    else:
        mStock_in_kospi = stock_list.split(' ,')


def __parse_stock_dictionary():
    global mStock_num_dic
    global mStock_name_dic
    global mStock_in_kospi

    base_url_kospi = 'https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page='
    base_url_kosdaq = 'https://finance.naver.com/sise/sise_market_sum.nhn?sosok=1&page='

    mStock_num_dic = {}
    mStock_name_dic = {}
    for idx, base_url in enumerate([base_url_kospi, base_url_kosdaq]):
        for i in range(1, 3):
            url = base_url + str(i)
            r = requests.get(url)

            soup = BeautifulSoup(r.text, 'lxml')
            t_items = soup.find_all('tr', {'onmouseover': 'mouseOver(this)'})
            for item in t_items:
                txt = item.a.get('href')
                k = re.search('[\d]', txt)
                if k:
                    code = str(txt.split('=')[1])
                    name = item.find_all('a', {'class': 'tltle'})[0].text
                    mStock_num_dic[code] = name
                    mStock_name_dic[name] = code
                    if idx == 0:
                        mStock_in_kospi.append(name)
    __set_stock_num_in_kospi()
    utils.write_dictionary_to_csv(mStock_name_dic, DIC_NAME_FILE)
    utils.write_dictionary_to_csv(mStock_num_dic, DIC_NUM_FILE)


# def __write_dictionary_to_csv(dictionary, csv_file_name):
#     try:
#         with open(csv_file_name, 'w', newline='') as csv_file:
#             writer = csv.writer(csv_file)
#             for key, value in dictionary.items():
#                 writer.writerow([key, value])
#     except IOError:
#         print('except')
#
#
# def __read_dictionary_to_csv(csv_file_name):
#     stock_dict = {}
#     try:
#         with open(csv_file_name, 'r') as csv_file:
#             reader = csv.reader(csv_file)
#             # for rows in reader:
#             #     print(rows)
#             stock_dict = {rows[0]: rows[1] for rows in reader}
#     except IOError:
#         print('except')
#     return stock_dict


def get_kospi_list():
    global mStock_in_kospi
    
    if len(mStock_in_kospi) < 10:
        __get_stock_num_in_kospi()
    return mStock_in_kospi


def get_stock_num_list(update=False):
    global mStock_num_dic
    if os.path.exists(DIC_NUM_FILE):
        mStock_num_dic = utils.read_dictionary_to_csv(DIC_NUM_FILE)
    else:
        __parse_stock_dictionary()
    if update:
        __parse_stock_dictionary()
    return list(mStock_num_dic.keys())


def get_stock_num_to_name(_stock_num):
    global mStock_num_dic
    if os.path.exists(DIC_NUM_FILE):
        mStock_num_dic = utils.read_dictionary_to_csv(DIC_NUM_FILE)
    else:
        __parse_stock_dictionary()
    return mStock_num_dic[_stock_num]


def get_stock_name_to_num(_stock_name):
    global mStock_name_dic
    if os.path.exists(DIC_NAME_FILE):
        mStock_name_dic = utils.read_dictionary_to_csv(DIC_NAME_FILE)
    else:
        __parse_stock_dictionary()
    return mStock_name_dic[_stock_name]

# def get_chart_data_path():
#     paths = os.getcwd() + '/data/chart_data/'
#     if not os.path.exists(paths):
#         os.makedirs(paths)
#     return paths

# def __remove_legacy_file(_stock_list):









