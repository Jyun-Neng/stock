import csv
from collections import namedtuple
from datetime import datetime
import numpy as np
import os
import pandas as pd
import requests
import time

from . import analytics
from . import plot
from . import stock_list_gen

# Taiwan Stock Exchange URL
TWSE_URL = "https://www.twse.com.tw/"
REPORT_URL = "https://www.twse.com.tw/exchangeReport/STOCK_DAY"
DAILY_INFO = namedtuple("DAILY_INFO", [
    "date", "tradingVolume", "turnover", "openingPrice", "hi", "lo",
    "closingPrice", "dailyPricing", "tansactions"
])
STOCK_LIST = "./stock-list/stock-list.csv"


class Stock(analytics.Analytics, plot.Plot):

    def __init__(self, args: object):
        if not os.path.exists(STOCK_LIST):
            stock_list_gen.stockListGen(STOCK_LIST)
        col_list = [
            "MSType", "code", "name", "ISIN", "ListingDate", "market",
            "IndustrialClass", "CFIcode"
        ]
        df = pd.read_csv(STOCK_LIST, usecols=col_list)
        code_list = df["code"].to_list()
        today = datetime.today()
        assert args.id in code_list, "Invalid stock ID!"
        assert (today.year >= args.month and
                today.month >= args.month), "Error Date!"
        super().__init__(args)
        self.stock_id = args.id
        self.month = args.month
        self.year = args.year
        self.daily_info_list = []

    def _convertDate(self, date: str) -> object:
        """Convert RepublicEra to AD year.

        Args:
            date: Y(PublicEra)/m/d
        Returns: 
            datetime object Y(AD)/m/d
        """
        if int(date.split('/')[0]) < 1900:
            date = '/'.join([str(int(date.split('/')[0]) + 1911)] +
                            date.split('/')[1:])
        return datetime.strptime(date, "%Y/%m/%d")

    def _dataFormatter(self, data_list: list):
        """Format raw data fetched from TWSE

        0: date
        1: trading volumne
        2: turnover in value
        3: opening price
        4: hi
        5: lo
        6: closing price
        7: daliy pricing
        8: # of transactions

        Args:
            data_list: Daily information list.
        Returns:
            A list of daily information.
        """
        daily_info_list = []
        for data in data_list:
            data[0] = self._convertDate(data[0])
            data[1] = int(data[1].replace(',', ''))
            data[2] = int(data[2].replace(',', ''))
            data[3] = None if data[3] == '--' else float(data[3].replace(
                ',', ''))
            data[4] = None if data[4] == '--' else float(data[4].replace(
                ',', ''))
            data[5] = None if data[5] == '--' else float(data[5].replace(
                ',', ''))
            data[6] = None if data[6] == '--' else float(data[6].replace(
                ',', ''))
            data[7] = float(0.0 if data[7].replace(',', '') ==
                            'X0.00' else data[7].replace(',', ''))
            data[8] = int(data[8].replace(',', ''))
            daily_info_list.append(DAILY_INFO(*data))

        return daily_info_list

    def writeDailyInfo(self):
        """Write daily information of the stock to csv.
        """
        path = '.'.join([self.stock_id, "csv"])
        with open(path, 'w', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            # Write title row
            writer.writerow(self.daily_info_list[0]._fields)
            # Write data rows
            for daily_info in self.daily_info_list:
                writer.writerow([_info for _info in daily_info])

    def addToDB(self):
        """Add new fetched daily information to DB if there is no
           information of the stock stored in DB.

        """
        doc = self.collection.find_one({"stock_id": self.stock_id})
        assert doc is None, "Stock ID has existed! Use updateToDB()."
        if len(self.daily_info_list) == 0:
            print("No data fetched!")
            return
        doc = {
            "stock_id": self.stock_id,
            "latest_date": self.getDate[-1],
            "date": self.getDate,
            "closing_price": self.getClosingPrice,
            "opening_price": self.getOpeningPrice,
            "hi": self.getHi,
            "lo": self.getLo,
            "daily_pricing": self.getDailyPricing,
            "trading_volume": self.getTradingVolume
        }
        self.collection.insert_one(doc).inserted_id

    def updateToDB(self):
        """Update stock daily information to DB. updateToDB can only update 
           daily information fetched after the latest date, it cannot update
           the day before update date.

        """
        query = {"stock_id": self.stock_id}
        doc = self.collection.find_one(query)
        assert doc is not None, "Stock ID does not exist! Use addToDB()."
        last_date = doc["latest_date"]
        date_list = self.getDate
        if date_list[-1] == last_date:
            print("Already update to the latest date.")
            return
        if date_list[-1] <= last_date:
            return
        idx = 0
        self.collection.update_one(query,
                                   {"$set": {
                                       "latest_date": date_list[-1]
                                   }})
        for date in date_list:
            if date > last_date:
                break
            idx += 1
        update = {
            "$push": {
                "date": {
                    "$each": date_list[idx:]
                },
                "closing_price": {
                    "$each": self.getClosingPrice[idx:]
                },
                "opening_price": {
                    "$each": self.getOpeningPrice[idx:]
                },
                "hi": {
                    "$each": self.getHi[idx:]
                },
                "lo": {
                    "$each": self.getLo[idx:]
                },
                "trading_volume": {
                    "$each": self.getTradingVolume[idx:]
                },
                "daily_pricing": {
                    "$each": self.getDailyPricing[idx:]
                }
            }
        }
        self.collection.update_one(query, update)

    def update(self) -> int:
        """Update stock daily information in DB to the latest trading day.

        Returns:
            Return 1 if require update DB. Otherwise, return 0.
        """
        date = self.getDate[-1]
        today = datetime.today()
        if today > date:
            self.fetchFrom(date.year, date.month)
            self.updateToDB()
            return 1
        else:
            return 0

    def fetch(self, year: int, month: int):
        """Fetch stock daily information in specified month.

        Args:
            year: The year of data to be fetched.
            month: The month of data to be fetched.
        Returns:
            A list of daily information.
        """
        params = {"date": "%d%02d01" % (year, month), "stockNo": self.stock_id}
        response = requests.get(REPORT_URL, params=params)
        assert response.status_code == 200, "URL requests fail."
        raw_data = response.json()
        daily_info_list = []
        if raw_data["stat"] == "OK":
            daily_info_list = self._dataFormatter(raw_data["data"])
        return daily_info_list

    def fetchn(self, start_year: int, start_mon: int, n: int) -> list:
        """Fetch n months of stock daily infromation.

        Args:
            start_year: start year to fetch the data.
            start_mon: start month to fetch the data.
            n: specify the number of months to fetch stock information.
        Returns:    
            A list of all the daily information.
        """
        year, mon = start_year, start_mon
        for i in range(n):
            print("fetch %d-%02d" % (year, mon))
            self.daily_info_list += self.fetch(year, mon)
            year = year + 1 if mon == 12 else year
            mon = mon + 1 if mon < 12 else 1
            time.sleep(3)
        return self.daily_info_list

    def fetchFrom(self, start_year: int, start_mon: int) -> list:
        """Fetch stock daily infromation from year-month to today.

        Args:
            start_year: start year to fetch the data.
            start_mon: start month to fetch the data.
        Returns:    
            A list of all the daily information.
        """
        today = datetime.today()
        total_mon = (12 * (today.year - start_year) +
                     (today.month - start_mon) + 1)
        year, mon = start_year, start_mon
        for i in range(total_mon):
            print("fetch %d-%02d" % (year, mon))
            self.daily_info_list += self.fetch(year, mon)
            year = year + 1 if mon == 12 else year
            mon = mon + 1 if mon < 12 else 1
            time.sleep(3)
        return self.daily_info_list

    @property
    def getDate(self):
        if not self.daily_info_list:
            field = self.collection.find_one({"stock_id": self.stock_id}, {
                "date": 1,
                "_id": 0
            })
            return field["date"]
        return [daily_info.date for daily_info in self.daily_info_list]

    @property
    def getOpeningPrice(self):
        if not self.daily_info_list:
            field = self.collection.find_one({"stock_id": self.stock_id}, {
                "opening_price": 1,
                "_id": 0
            })
            return field["opening_price"]
        return [daily_info.openingPrice for daily_info in self.daily_info_list]

    @property
    def getClosingPrice(self):
        if not self.daily_info_list:
            field = self.collection.find_one({"stock_id": self.stock_id}, {
                "closing_price": 1,
                "_id": 0
            })
            return field["closing_price"]
        return [daily_info.closingPrice for daily_info in self.daily_info_list]

    @property
    def getLo(self):
        if not self.daily_info_list:
            field = self.collection.find_one({"stock_id": self.stock_id}, {
                "lo": 1,
                "_id": 0
            })
            return field["lo"]
        return [daily_info.lo for daily_info in self.daily_info_list]

    @property
    def getHi(self):
        if not self.daily_info_list:
            field = self.collection.find_one({"stock_id": self.stock_id}, {
                "hi": 1,
                "_id": 0
            })
            return field["hi"]
        return [daily_info.hi for daily_info in self.daily_info_list]

    @property
    def getDailyPricing(self):
        if not self.daily_info_list:
            field = self.collection.find_one({"stock_id": self.stock_id}, {
                "daily_pricing": 1,
                "_id": 0
            })
            return field["daily_pricing"]
        return [daily_info.dailyPricing for daily_info in self.daily_info_list]

    @property
    def getTradingVolume(self):
        if not self.daily_info_list:
            field = self.collection.find_one({"stock_id": self.stock_id}, {
                "trading_volume": 1,
                "_id": 0
            })
            return field["trading_volume"]
        return [daily_info.tradingVolume for daily_info in self.daily_info_list]
