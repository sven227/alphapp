import os
from functools import reduce
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, date

from time import sleep
import glob


############helpers##########


def read_symbol(symbol, api_key_alpha, function="TIME_SERIES_DAILY_ADJUSTED"):
    url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&outputsize=full&apikey={api_key_alpha}&datatype=csv"

    _df = pd.read_csv(url)
    _df.dropna(inplace=True)

    try:
        _df["timestamp"] = pd.to_datetime(
            _df["timestamp"], infer_datetime_format="%Y—%m-%d"
        )
        _df.set_index("timestamp", inplace=True)
        _df.sort_values(by=["timestamp"], axis="index", ascending=True, inplace=True)
    except IOError:
        print((symbol, "does not exist in alpha-vantage db"))
    return _df


def create_path4symbol(symbol, _root_path):
    symbol.replace(".", "_")
    _path_symbol = _root_path + "/data/{0}/daily_{1}.csv".format(symbol, symbol)
    dir_name = _root_path + "/data/{0}".format(symbol)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        print(("Directory ", dir_name, " Created "))
    else:
        print(("Directory ", dir_name, " already exists"))
    return _path_symbol


# get last 100 registries of time_series daily from alpha-vantage
def get_alphav_last100(
    symbol, api_key_alpha, function="TIME_SERIES_DAILY_ADJUSTED", outputsize="compact"
):
    url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&outputsize=outputsize&apikey={api_key_alpha}&datatype=csv"
    name = "daily" + "_" + symbol
    _df = pd.read_csv(url)
    _df.set_index("timestamp", inplace=True)
    _df.index = pd.to_datetime(_df.index)
    _df.sort_values(by=["timestamp"], axis="index", ascending=True, inplace=True)
    return _df


# read from csv - input list of symbol-tickers and returns a dictionary with key <symbol> and dataframe as value
def get_daily(symbol_list, root_path, startd, endd, wd=None, usecols=None):
    if wd == None:
        wd = os.getcwd()

    # suffixes = list( map( lambda x:  '_'+x ,symbol_list))
    path_list = {
        symbol: create_path4symbol(symbol, root_path) for symbol in symbol_list
    }
    dict = retrieveDF(path_list, startd, endd, usecols)
    # return dictionary with key=df_<symbol> and the dataframe as value
    return dict


# read from csv with path_list  - is called from get_daily
def retrieveDF(path_list, startd, endd, usecols, rename_column=False):
    if startd == "":
        startd, endd = get_startd_endd_default()
    if endd == "":
        startd, endd = get_startd_endd_default()

    dict_of_df = {}
    for symbol, path in list(path_list.items()):
        # key_name = 'df_'+symbol
        key_name = symbol
        _df = pd.read_csv(path, usecols=usecols)
        _df.set_index("timestamp", inplace=True)
        _df.index = pd.to_datetime(_df.index)
        # _df.sort_index(inplace=True)
        _df.sort_values(by=["timestamp"], axis="index", ascending=True, inplace=True)
        # when sorted by date in ascending order the slice by startd:endd is correct
        _df = _df.loc[startd:endd]
        # _df = _df.loc[endd:startd]

        if rename_column == True:
            column = f"{symbol}"
            dict_of_df[key_name] = _df.rename(columns={"adjusted_close": column})
        else:
            dict_of_df[key_name] = _df
    return dict_of_df


###############additional little helpers##########
def get_startd_endd_default():
    _startd = "2000-01-01"
    _endd = "2020-12-31"
    return _startd, _endd


def getlastdate(symbol):
    startd, endd = get_startd_endd_default()
    dict = get_daily([symbol], startd, endd)
    # key_name = 'df_'+symbol
    pd = dict[symbol].tail(1)
    # return pd.index[0]
    return string2date(pd.index[0])


def string2date(date_string, format="%Y-%m-%d"):
    if type(date_string) == str:
        date_time_obj = datetime.strptime(date_string, format)
        return date_time_obj
    else:
        return date_string


def date2string(date_time_obj, format="%Y-%m-%d"):
    return date_time_obj.strftime(format)


###############call these ones##########
def read_data(
    _root_path, _api_key_alpha, _symbol_list, function="TIME_SERIES_DAILY_ADJUSTED"
):
    num = len(_symbol_list)
    _dict = {}
    _path_list = []

    for symbol in _symbol_list:
        _dict[symbol] = read_symbol(symbol, _api_key_alpha, function)
        _path_list.append(create_path4symbol(symbol, _root_path))
        print(("_____________________________", num))
        print((symbol + " " + str(len(_dict))))
    return _dict, _path_list


# use for path,_df in zip(path_list,df_list) to do _df.to_csv - this should work
def persist_data(symbol_list, _dict, _path_list):
    for symbol, path in zip(symbol_list, _path_list):
        _df = _dict[symbol]

        _df.to_csv(path)
    path = _path_list[-1]
    _modTimesinceEpoc = os.path.getmtime(path)
    _modificationTime = datetime.fromtimestamp(_modTimesinceEpoc).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    print(("Last Modified Time : ", _modificationTime))
    del _dict
    return _modificationTime


# read from csv one specific ticker - calls get_daily -> retrieveDF
def get_daily_symbol(symbol, root_path, startd="", endd="", wd=None, usecols=None):
    dict = get_daily([symbol], root_path, startd, endd)
    # key_name = 'df_'+symbol
    key_name = symbol
    # return panda dataframe
    _df = dict[key_name]
    _df.index = pd.to_datetime(_df.index)
    # _df.sort_values(by=['timestamp'],axis='index',ascending=True,inplace=True)
    return _df


def update_csv(symbol_list, api_key_alpha, root_path):
    counter = 0
    for symbol in symbol_list:
        counter += counter + 1
        print("")
        print(("processing symbol: " + symbol))
        df_latest = get_alphav_last100(symbol, api_key_alpha)
        df_latest.head(1)
        df_latest.tail(1)

        _xdo = df_latest.tail(1).index[0]
        print(("last stock-date available from alpha_vantage:", date2string(_xdo)))
        _xdo.date()

        df_from_csv = get_daily_symbol(symbol, root_path)
        _xdo = df_from_csv.tail(1).index[0]
        df_filtered = df_latest.loc[df_latest.index > _xdo]
        print(("number of entries we need to append to csv:", df_filtered.size))

        print("retrieving head data from csv")
        df_latest.head(1)
        df_latest.tail(1)
        df_from_csv.sort_values(
            by=["timestamp"], axis="index", ascending=True, inplace=True
        )
        if df_filtered.dropna().empty:
            print("nothing to append")
        else:
            df_updated = df_from_csv.append(
                df_filtered, verify_integrity=False, sort=False
            )
            print("the final csv to be updated")
            df_updated.head(1)
            df_updated.tail(1)
            df_updated.index
            # write_csv_one_by_one_df(symbol, df_updated, counter)
            _path_symbol = create_path4symbol(symbol, root_path)
            df_updated.to_csv(_path_symbol.format(symbol, symbol))
    return


def compose_portfolio(
    symbol_list,
    root_path,
    startd="2000-01-01",
    endd="",
    usecols=["timestamp", "adjusted_close"],
):
    # loop through dict and join columns with inner join to one new dataframe
    # Pre-req. file must exist in relative path e.g.: ./data/PG/daily_PG.csv
    # get all files with symbols we are interested in into a list
    # read file of symbol one by one into dataframe
    # rename column_names to close_PG, close_{}.format(symbol)
    # reset index to timeframe inplace= true
    # join the dataframes into one only using inner join (no NaN)
    # columns: open	high	low	close	adjusted_close	volume	dividend_amount	split_coefficient
    if endd == "":
        today = date.today()
        endd = date2string(today)
    suffixes = list(["_" + x for x in symbol_list])
    wd = os.getcwd()

    # path_list =  {symbol: composePath(wd, '/data/', symbol) for symbol in symbol_list}
    path_list = {
        symbol: create_path4symbol(symbol, root_path) for symbol in symbol_list
    }
    path_list

    dict = retrieveDF(path_list, startd, endd, usecols, True)
    df_final = retrieveDFfinal(dict, suffixes)
    df_final.sort_values(by=["timestamp"], axis="index", ascending=True, inplace=True)
    # df_final.tail()
    return df_final


####################_____run____#################


def refresh_db(root_path, api_key_alpha, symbol_list, full_refresh_alphavantage="True"):
    if full_refresh_alphavantage is True:
        for index, symbol in enumerate(symbol_list):
            _secs_to_wait = time_sleep(index)
            time.sleep(_secs_to_wait)
            _symbol_list = []
            _symbol_list.append(symbol)
            _dict, _path_list = read_data(root_path, api_key_alpha, _symbol_list)
            print((_dict.values))
            for path in _path_list:
                print(("\n\t", path))

            my_date = persist_data(_symbol_list, _dict, _path_list)
            print(my_date)
    else:
        for index, symbol in enumerate(symbol_list):
            _secs_to_wait = time_sleep(index)
            time.sleep(_secs_to_wait)
            _symbol_list = []
            _symbol_list.append(symbol)
            update_csv(_symbol_list, api_key_alpha, root_path)


def crea_path4symbol(symbol, _root_path):
    _path_symbol = _root_path + "/data/{0}/daily_{1}.csv".format(symbol, symbol)
    return _path_symbol


def create_path_list(symbol_list, root_path):
    path_list = {symbol: crea_path4symbol(symbol, root_path) for symbol in symbol_list}
    return path_list


def time_sleep(index):
    seconds_to_wait = index * 5 + index * 1.5
    return seconds_to_wait


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
            if "adjusted_close" in usecols:
                _df_master[key_name] = _df.rename(columns={"adjusted_close": column})
            elif "volume" in usecols:
                _df_master[key_name] = _df.rename(columns={"volume": column})
            else:
                print("usecols does not contain valid value")
        else:
            _df_master[key_name] = _df

        _df_master.dropna(inplace=True)
    return _df_master
