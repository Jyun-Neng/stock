from datetime import datetime
from datetime import timedelta
from multipledispatch import dispatch
from pymongo import MongoClient
import time

from . import crawler
from . import errors


class StockDB():

    def __init__(self, url: str, port: int):
        client = MongoClient(url, port)
        self.db = client["stock"]
        self.crawler = crawler.Crawler()

    def isStockExist(self, id: str) -> bool:
        return self.db[id].count() != 0

    def _scrape(self, id, month, year):
        """Scrape monthly stock data from TWSE."""
        time.sleep(3)
        return self.crawler.getMonthlyData(id, month, year)

    def _findMonthlyData(self, collection, month, year):
        date = datetime.strptime(f'{year}/{month}', "%Y/%m")
        return list(
            collection.find({
                "date": {
                    "$gte": self._firstDayOfMon(date),
                    "$lte": self._lastDayOfMon(date)
                }
            }))

    def _insertDoc(self, id, month, year):
        """Insert scraped data in DB."""
        collection = self.db[id]
        monthly_data = self._scrape(id, month, year)
        db_data = collection.find({}, {"_id": 0})
        # Check if scraped data has been existed in DB.
        for data in db_data:
            if data in monthly_data:
                monthly_data.remove(data)
        if monthly_data:
            collection.insert_many(monthly_data)
        return monthly_data

    def _lastDayOfMon(self, date):
        next_mon = date.replace(day=28) + timedelta(days=4)
        return next_mon - timedelta(days=next_mon.day)

    def _firstDayOfMon(self, date):
        return date.replace(day=1)

    @dispatch(str, int, int, int)
    def getData(self, id, day, month, year):
        """Get daily data"""
        collection = self.db[id]
        date = datetime.strptime(f'{year}/{month}/{day}', "%Y/%m/%d")
        data = collection.find_one({"date": {"$eq": date}})
        if data is None:
            self._insertDoc(id, month, year)
            data = collection.find_one({"date": {"$eq": date}})
        return data

    @dispatch(str, int, int)
    def getData(self, id, month, year):
        """Get monthly data."""
        collection = self.db[id]
        date = datetime.strptime(f'{year}/{month}', "%Y/%m")
        today = datetime.today()
        today = datetime.strptime(f'{today.year}/{today.month}/{today.day}',
                                  "%Y/%m/%d")
        # run insertDoc if request month is current month.
        if today.year == year and today.month == month:
            self._insertDoc(id, month, year)
            return self._findMonthlyData(collection, month, year)
        monthly_data = self._findMonthlyData(collection, month, year)
        # run inserDoc if request monthly data is not exist in DB.
        if not monthly_data:
            self._insertDoc(id, month, year)
            return self._findMonthlyData(collection, month, year)
        return list(monthly_data)

    @dispatch(str, str, int)
    def getData(self, id, quarter, year):
        """Get quarterly data."""
        # Map quarter to month
        quarter_map = {
            "1st": [1, 3],
            "2nd": [4, 6],
            "3rd": [7, 9],
            "4th": [10, 12]
        }
        mon_range = quarter_map.get(quarter)
        if mon_range is None:
            raise errors.InvalidQuarterError(f'Invalid quarter {quarter}.')
        start_mon, end_mon = mon_range
        collection = self.db[id]
        start_date = datetime.strptime(f'{year}/{start_mon}', "%Y/%m")
        end_date = datetime.strptime(f'{year}/{end_mon}', "%Y/%m")
        for mon in range(start_mon, end_mon + 1):
            self._insertDoc(id, mon, year)
        quarterly_data = collection.find({
            "date": {
                "$gte": self._firstDayOfMon(start_date),
                "$lte": self._lastDayOfMon(end_date)
            }
        })
        return list(quarterly_data)
