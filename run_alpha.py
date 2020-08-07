def refresh_db(root_path, api_key_alpha, symbol_list, read_from_alphavantage="True"):
    if read_from_alphavantage is True:
        for symbol in symbol_list:
            _symbol_list = []
            _symbol_list.append(symbol)
            _dict, _path_list = read_data(root_path, api_key_alpha, _symbol_list)
            print(_dict.values)
            for path in _path_list:
                print("\n\t", path)

            my_date = persist_data(_symbol_list, _dict, _path_list)
            print(my_date)
    else:
        for symbol in symbol_list:
            time.sleep(5)
            _symbol_list = []
            _symbol_list.append(symbol)
            update_csv(_symbol_list, api_key_alpha, root_path)


def create_path_list(symbol_list, root_path):
    path_list = {symbol: crea_path4symbol(symbol, root_path) for symbol in symbol_list}
    return path_list


def initialize_df(symbol_list, startd, endd):
    end_date = string2date(endd)
    start_date = string2date(startd)
    periods = (end_date - start_date).days
    index = pd.date_range(start_date, periods=periods, freq="D")

    _df = pd.DataFrame(index=index, columns=symbol_list)
    _df = _df.fillna(0)  # with 0s rather than NaNs
    return _df


def retrievePF(symbol_list, path_list, startd, endd, usecols, rename_column=True):
    _df_master = initialize_df(symbol_list, startd, endd)
    for symbol, path in list(path_list.items()):
        # key_name = 'df_'+symbol
        key_name = symbol
        _df = pd.read_csv(path, usecols=usecols)
        _df.set_index("timestamp", inplace=True)
        _df.index = pd.to_datetime(_df.index)
        _df.sort_values(by=["timestamp"], axis="index", ascending=True, inplace=True)
        _df = _df.loc[startd:endd]
        if rename_column == True:
            column = f"{symbol}"
            _df_master[key_name] = _df.rename(columns={"adjusted_close": column})
        else:
            _df_master[key_name] = _df
        _df_master.dropna(inplace=True)
    return _df_master


#######################
from myauz.myalpha_funcs import (
    read_data,
    persist_data,
    update_csv,
    compose_portfolio,
    retrieveDF,
    string2date,
)
from myauz.myalpha_libs import StocksDb

from myauz.myfuncs import crea_path4symbol

import time

###no va: symbol_list = ['WZFS.FRK','FGMD.FRK']
# symbol_list = ['DHR','GOOG','AMZN','AAPL']
# symbol_list = ['EMR','HEINY','HXGBY','LDSVF']
# symbol_list = ['EMR','HEINY','HXGBY','LDSVF','MCD','MSFT','NVS']

symbol_list = [
    "DHR",
    "GOOG",
    "AMZN",
    "AAPL",
    "ATR",
    "CSCO",
    "CL",
    "EMR",
    "HEINY",
    "HXGBY",
    "LDSVF",
    "MCD",
    "MSFT",
    "NVS",
    "NVZMY",
]

alphaDB = StocksDb()
alphaDB.check_path()
print("\n", alphaDB.api_key_alpha, alphaDB.path)
api_key_alpha = alphaDB.api_key_alpha
root_path = alphaDB.path
read_from_alphavantage = False
rename_column = True


from datetime import date
import datetime
import pandas as pd

usecols = ["timestamp", "adjusted_close"]
startd = "2020-01-01"
endd = "2020-08-05"
path_list = create_path_list(symbol_list, root_path)
df_pf = retrievePF(symbol_list, path_list, startd, endd, usecols, rename_column)
print(df_pf)
