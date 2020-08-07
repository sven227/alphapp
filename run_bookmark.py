
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



### Pick a csv file for the first time.
### Then, the previously picked file will be reused.
#aapl_path = bm.FileBookmark("aapl").path
#dt = pd.read_csv(aapl_path)
#print(dt.head())


