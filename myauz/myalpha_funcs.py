import os
from datetime import datetime

import pandas as pd


############helpers##########

def read_symbol(symbol, api_key_alpha, function='TIME_SERIES_DAILY_ADJUSTED'):
    url = (
        f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&outputsize=full&apikey={api_key_alpha}&datatype=csv')

    _df = pd.read_csv(url)
    _df.dropna(inplace=True)

    _df['timestamp'] = pd.to_datetime(_df['timestamp'], infer_datetime_format='%Y--%m-%d')
    _df.set_index('timestamp', inplace=True)
    _df.sort_values(by=['timestamp'], axis='index', ascending=True, inplace=True)
    return _df


def create_path4symbol(symbol, _root_path):
    symbol.replace('.', '_')
    _path_symbol = _root_path + '/data/{0}/daily_{1}.csv'.format(symbol, symbol)
    dir_name = _root_path + '/data/{0}'.format(symbol)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        print("Directory ", dir_name, " Created ")
    else:
        print("Directory ", dir_name, " already exists")
    return _path_symbol


###############call these ones##########
def read_data(_root_path, _api_key_alpha, _symbol_list, function='TIME_SERIES_DAILY_ADJUSTED'):
    num = len(_symbol_list)
    _dict = {}
    _path_list = []

    for symbol in _symbol_list:
        _dict[symbol] = read_symbol(symbol, _api_key_alpha, function)
        _path_list.append(create_path4symbol(symbol, _root_path))
        print("_____________________________", num)
        print(symbol + " " + str(len(_dict)))
    return _dict, _path_list


# use for path,_df in zip(path_list,df_list) to do _df.to_csv - this should work
def persist_data(symbol_list, _dict, _path_list):
    for symbol, path in zip(symbol_list, _path_list):
        _df = _dict[symbol]

        _df.to_csv(path)
    path = _path_list[-1]
    _modTimesinceEpoc = os.path.getmtime(path)
    _modificationTime = datetime.fromtimestamp(_modTimesinceEpoc).strftime('%Y-%m-%d %H:%M:%S')
    print("Last Modified Time : ", _modificationTime)
    del _dict
    return _modificationTime
