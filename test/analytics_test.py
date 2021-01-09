import argparse
import unittest
from datetime import datetime
from stock import analytics


class StockTest(unittest.TestCase):
    def setUp(self):
        self.args = argparse.Namespace(id="2885",
                                       year=2021,
                                       month=1,
                                       url="127.0.0.1",
                                       port=27017)
        self.analytics = analytics.Analytics(self.args)

    def test_isRaising(self):
        self.assertEqual(self.analytics.isRaising(), False)
    
    def test_isFalling(self):
        self.assertEqual(self.analytics.isFalling(), False)

if __name__ == "__main__":
    unittest.main()

