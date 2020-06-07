def crea_path4symbol(symbol, _root_path):
    _path_symbol = _root_path + '/data/{0}/daily_{1}.csv'.format(symbol, symbol)
    return _path_symbol
