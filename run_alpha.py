#######################
from myauz.myalpha_funcs import (
    read_data,
    persist_data,
    update_csv,
    compose_portfolio,
    retrieveDF,
    string2date,
    retrievePF,
    initialize_df,
    time_sleep,
    create_path_list,
    refresh_db,
)

#this is only for ipad pyto:
#from myauz.myalpha_libs import StocksDb
#use this one instead:
from myauz.myalpha_libs_universal import StocksDb

import time

symbol_list = ["DHR", "GOOG"]
# symbol_list = ['EMR','HEINY','HXGBY','LDSVF']
# symbol_list = ['EMR','HEINY','HXGBY','LDSVF','MCD','MSFT','NVS']

# symbol_list = [
#    "DHR",
#    "GOOG",
#    "AMZN",
#    "AAPL",
#    "ATR",
#    "CSCO",
#    "CL",
#    "EMR",
#    "HEINY",
#    "HXGBY",
#    "LDSVF",
#    "MCD",
#    "MSFT",
#    "NVS",
#    "NVZMY",
# ]

alphaDB = StocksDb()
alphaDB.check_path()
print("\n", alphaDB.api_key_alpha, alphaDB.path)
print("\n\n")
api_key_alpha = alphaDB.api_key_alpha
root_path = alphaDB.path
print("root_path: ", root_path)
read_from_alphavantage = False
rename_column = True


from datetime import date
import datetime
import pandas as pd

#usecols = ["timestamp", "adjusted_close"]

usecols = ["timestamp", "volume"]

startd = "2020-01-01"
endd = "2020-08-14"
path_list = create_path_list(symbol_list, root_path)


# refresh_db(root_path, api_key_alpha, symbol_list, False)

### create dataframe with portfolio
df_pf = retrievePF(symbol_list, path_list, startd, endd, usecols, rename_column)
print(df_pf) 
