import argparse
import unittest
from datetime import datetime
from stock import stock


class StockTest(unittest.TestCase):
    def setUp(self):
        self.args = argparse.Namespace(id="2885",
                                       year=2021,
                                       month=1,
                                       url="127.0.0.1",
                                       port=27017)
        self.year = self.args.year
        self.month = self.args.month
        self.stock = stock.Stock(self.args)

    def test_fetch(self):
        stock_info_list = self.stock.fetch(self.year, self.month)
        self.assertTrue(stock_info_list is not None,
                        "Stock info is not fetched")

    def test_fetchFrom(self):
        today = datetime.today()
        date = '/'.join([str(self.year), str(self.month)])
        start_date = datetime.strptime(date, "%Y/%m")
        self.stock.fetchFrom(self.year, self.month)
        for daily_info in self.stock.daily_info_list:
            self.assertTrue(today >= daily_info.date >= start_date,
                            "Fetch date is not in specified date")

    def test_getDate(self):
        self.stock.fetch(self.year, self.month)
        self.assertEqual(self.stock.getDate[0], datetime(2020, 1, 2),
                         "Get wrong date")

    def test_getDailyPricing(self):
        self.stock.fetch(self.year, self.month)
        self.assertEqual(self.stock.getDailyPricing[0], 0.0,
                         "Get wrong daily pricing")


if __name__ == "__main__":
    unittest.main()
