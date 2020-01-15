import datetime
import configparser
import csv
from pathlib import Path
import os


CONFIG_FILE = 'config.cfg'


def get_today():
    return datetime.datetime.now().strftime('%Y.%m.%d')


def get_this_month():
    return datetime.datetime.now().strftime('%Y.%m')


def get_time():
    return datetime.datetime.now().strftime('%H%M')


def get_config_value(section, key):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if config.has_section(section):
        return config.get(section, key)
    else:
        config.add_section(section)
    return 0


def set_config_value(section, key, value):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if config.has_section(section):
        config.set(section, key, value)
    else:
        config.add_section(section)
        config.set(section, key, value)
    with open(CONFIG_FILE, 'w') as config_file:
        config.write(config_file)


# +
def write_dictionary_to_csv(dictionary, csv_file_name):
    try:
        with open(csv_file_name, 'w') as csv_file:
            csv_file.write('stock_name,acc_test,acc_eval,expected_value,buy_percent,pred_sell,pred_hold,pred_buy\r\n')
            for key, value in dictionary.items():
                csv_file.write(str(key) + ',' + str(value))
                csv_file.write('\r\n')
    except IOError:
        print('except')
        
# def write_dictionary_to_csv(dictionary, csv_file_name):
#     try:
# #         with open(csv_file_name, 'w', newline='') as csv_file:
# #             writer = csv.writer(csv_file)
# #             for key, value in dictionary.items():
# #                 writer.writerow([key, value])
#     except IOError:
#         print('except')


# -

def read_dictionary_to_csv(csv_file_name):
    stock_dict = {}
    try:
        with open(csv_file_name, 'r') as csv_file:
            reader = csv.reader(csv_file)
            # for rows in reader:
            #     print(rows)
            stock_dict = {rows[0]: rows[1] for rows in reader}
    except IOError:
        print('except')
    return stock_dict


def get_pred_data_path():
    paths = os.getcwd() + '/result/pred_data/'
    if not os.path.exists(paths):
        os.makedirs(paths)
    return paths


def get_project_path():
    return Path(os.getcwd()).parent

