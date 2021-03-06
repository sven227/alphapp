#######################
from myauz.myalpha_funcs import (
    read_data,
    persist_data,
    update_csv,
    compose_portfolio,
    retrieveDF,
    string2date,
    retrievePF,
    initialize_DF,
    time_sleep,
    create_path_list,
    refresh_db,
)
from myauz.myalpha_libs import StocksDb

from myauz.myfuncs import crea_path4symbol

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
read_from_alphavantage = False
rename_column = True


from datetime import date
import datetime
import pandas as pd

usecols = ["timestamp", "adjusted_close"]
startd = "2020-01-01"
endd = "2020-08-14"
path_list = create_path_list(symbol_list, root_path)


# refresh_db(root_path, api_key_alpha, symbol_list, False)

### create dataframe with portfolio
df_pf = retrievePF(symbol_list, path_list, startd, endd, usecols, rename_column)
print(df_pf)
