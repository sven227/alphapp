#
import os

from myauz import myalpha


class StocksDb:
    def __init__(self):
        self.path = myalpha.secret['path']
        self.api_key_alpha = myalpha.secret['api_key_alpha']

    def check_api_key(self):
        return self.api_key_alpha

    def check_path(self):
        dir_name = self.path + '/data'
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
            print("Directory ", dir_name, " Created ")
        else:
            print("Directory ", dir_name, " already exists")
        return dir_name
