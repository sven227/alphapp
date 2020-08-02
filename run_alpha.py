from myauz.myalpha_funcs import read_data, persist_data
from myauz.myalpha_libs import StocksDb

from myauz.myfuncs import crea_path4symbol
#symbol_list = ['DHR','GOOG','AMZN','AAPL']
symbol_list = ['WZFS.FRK','FGMD.FRK']
#symbol_list = ['EMR','HEINY','HXGBY','LDSVF']
#symbol_list = ['EMR','HEINY','HXGBY','LDSVF','MCD','MSFT','NVS']
#symbol_list = ['DHR','GOOG','AMZN','AAPL','ATR','CSCO','CL','FGMD.FRK','EMR','HEINY','HXGBY','LDSVF','MCD','MSFT','NVS','NVZMY','WZFS.FRK']
alphaDB = StocksDb()

alphaDB.check_path()
print(alphaDB.api_key_alpha, alphaDB.path)
api_key_alpha = alphaDB.api_key_alpha
root_path = alphaDB.path

#pg_path = crea_path4symbol('PG', alphaDB.path)
#print(pg_path)

#_df = read_symbol('PG', api_key_alpha)
#print(_df)

for symbol in symbol_list:
    _symbol_list = []
    _symbol_list.append(symbol)
    _dict, _path_list = read_data(root_path, api_key_alpha, _symbol_list)
    print(_dict.values)
    for path in _path_list:
        print(path)

    my_date = persist_data(_symbol_list, _dict, _path_list)
    print(my_date)


# my_dict, path_list = mal.read_data(alphaDB.path, alphaDB.api_key_alpha, symbol_list)
# for path in path_list:
#   print(path)
