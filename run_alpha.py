from myauz.myalpha_funcs import read_data, persist_data, update_csv, compose_portfolio
from myauz.myalpha_libs import StocksDb

from myauz.myfuncs import crea_path4symbol
symbol_list = ['AAPL']
#symbol_list = ['DHR','GOOG','AMZN','AAPL']
#symbol_list = ['WZFS.FRK','FGMD.FRK']
#symbol_list = ['EMR','HEINY','HXGBY','LDSVF']
#symbol_list = ['EMR','HEINY','HXGBY','LDSVF','MCD','MSFT','NVS']
#symbol_list = ['DHR','GOOG','AMZN','AAPL','ATR','CSCO','CL','EMR','HEINY','HXGBY','LDSVF','MCD','MSFT','NVS','NVZMY']
alphaDB = StocksDb()

alphaDB.check_path()
print(alphaDB.api_key_alpha, alphaDB.path)
api_key_alpha = alphaDB.api_key_alpha
root_path = alphaDB.path


read_from_alphavantage = False

#pg_path = crea_path4symbol('PG', alphaDB.path)
#print(pg_path)

#_df = read_symbol('PG', api_key_alpha)
#print(_df)
if read_from_alphavantage is True:
    for symbol in symbol_list:
        _symbol_list = []
        _symbol_list.append(symbol)
        _dict, _path_list = read_data(root_path, api_key_alpha, _symbol_list)
        print(_dict.values)
        for path in _path_list:
            print(path)

        my_date = persist_data(_symbol_list, _dict, _path_list)
        print(my_date)
else:
    for symbol in symbol_list:
        _symbol_list = []
        _symbol_list.append(symbol)
        update_csv(_symbol_list, api_key_alpha, root_path)

#compose portfolio
#usecols=['timestamp','adjusted_close', 'volume']
df_portfolio= compose_portfolio(symbol_list, root_path, startd='2019-01-01')
df_portfolio.head()
df_portfolio.info()
endd='2020-02-21'
startd='2020-02-19'
df_portfolio = df_portfolio.loc[startd:endd]
print(df_portfolio.head(1))
print(df_portfolio.info())

# my_dict, path_list = mal.read_data(alphaDB.path, alphaDB.api_key_alpha, symbol_list)
# for path in path_list:
#   print(path)
