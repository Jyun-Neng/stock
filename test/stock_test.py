import argparse
import unittest
from datetime import datetime
from stock import stock


class StockTest(unittest.TestCase):

    def setUp(self):
        self.args = argparse.Namespace(
            id="2885", year=2021, month=1, url="127.0.0.1", port=27017)
        self.year = self.args.year
        self.month = self.args.month
        self.stock = stock.Stock(self.args)

    def test_fetch(self):
        stock_info_list = self.stock.fetch(2021, 1)
        self.assertTrue(stock_info_list is not None,
                        "Stock info is not fetched")

    def test_fetchn(self):
        stock_info_list = self.stock.fetchn(2020, 1, 13)
        date = stock_info_list[-1].date
        self.assertTrue(date.year == 2021 and date.month == 1,
                        "Fetched date is wrong")

    def test_fetchFrom(self):
        today = datetime.today()
        date = '/'.join([str(self.year), str(self.month)])
        start_date = datetime.strptime(date, "%Y/%m")
        self.stock.fetchFrom(self.year, self.month)
        for daily_info in self.stock.daily_info_list:
            self.assertTrue(today >= daily_info.date >= start_date,
                            "Fetch date is not in specified date")


if __name__ == "__main__":
    unittest.main()
