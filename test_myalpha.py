import os
import unittest
from myauz import myalpha


class MyAPIkeyTest(unittest.TestCase):
    def test_api_key(self):
        _api_key_alpha = myalpha.secret['api_key_alpha']
        my_api_key = '77K8XPSR3XWWZJ80'
        print("TEST api_key:", _api_key_alpha)

        self.assertEqual(_api_key_alpha, my_api_key)

    def test_data_path(self):
        _path = myalpha.secret['path']
        my_path = '/Users/svengatsos/stocks'
        print("TEST datapathdb:", _path)

        self.assertEqual(_path, my_path)


class MyWorkingDirTest(unittest.TestCase):
    def test_path(self):
        _wd = os.getcwd()
        print("TEST working diretory:", _wd)
        self.assertEqual(_wd, '/Users/svengatsos/PycharmProjects/alpha')


if __name__ == '__main__':
    unittest.main()
