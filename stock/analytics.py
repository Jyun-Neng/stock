from datetime import datetime
import numpy as np
import collections as coll
import pandas as pd

from . import stockDB


class Analytics(stockDB.StockDB):
    """Stock information analysis"""

    def __init__(self, args: object):
        super().__init__(args.url, args.port)
        self.stock_id = args.id

    @property
    def _getClosingPrice(self) -> list:
        assert self.isStockExist(
        ), "No stock information in DB. Plz fetch it first."
        field = self.collection.find_one({"stock_id": self.stock_id}, {
            "closing_price": 1,
            "_id": 0
        })
        return field["closing_price"]

    @property
    def _getDate(self) -> list:
        assert self.isStockExist(
        ), "No stock information in DB. Plz fetch it first."
        field = self.collection.find_one({"stock_id": self.stock_id}, {
            "date": 1,
            "_id": 0
        })
        return field["date"]

    @property
    def _getDailyPricing(self) -> list:
        assert self.isStockExist(
        ), "No stock information in DB. Plz fetch it first."
        field = self.collection.find_one({"stock_id": self.stock_id}, {
            "daily_pricing": 1,
            "_id": 0
        })
        return field["daily_pricing"]

    @property
    def _getTradingVolume(self) -> list:
        assert self.isStockExist(
        ), "No stock information in DB. Plz fetch it first."
        field = self.collection.find_one({"stock_id": self.stock_id}, {
            "trading_volume": 1,
            "_id": 0
        })
        return field["trading_volume"]

    def isStockExist(self) -> bool:
        doc = self.collection.find_one({"stock_id": self.stock_id})
        return doc is not None

    def isPriceRaising(self, daily_pricing) -> bool:
        return daily_pricing > 0

    def isPriceFalling(self, daily_pricing) -> bool:
        return daily_pricing < 0

    def daysCount(self, raising: bool) -> dict:
        """Count the number of days the price has continuously increased or 
           decreased.
        
        Args:
            raising: count price raising days if true. Otherwise, count price falling days.
        Returns:    
            A dict of all the daily information.
        """
        date_table = {}
        daily_pricing_list = self._getDailyPricing
        date_list = self._getDate
        record_start_date = True
        days = 0
        for i in range(len(daily_pricing_list)):
            if (raising and self.isPriceRaising(daily_pricing_list[i])) or (
                    not raising and self.isPriceFalling(daily_pricing_list[i])):
                if record_start_date:
                    start_date = date_list[i]
                days += 1
                record_start_date = False
            else:
                if record_start_date is False:
                    date_table[start_date] = days
                record_start_date = True
                days = 0
        return coll.Counter(date_table.values())

    def raisingFallingDaysDist(self) -> object:
        """The distribution of continuous raising and falling days.

        Returns:    
            A dataframe of the distribution of the continuous raising and falling days.
        Example:
            dataframe:
              days times
            0   -2     2 (The stock price fell 2 days twice)
        """
        raising_days_cnt = self.daysCount(True)
        falling_days_cnt = self.daysCount(False)
        raising_days_list = list(raising_days_cnt.keys())
        falling_days_list = list(falling_days_cnt.keys())
        max_raising_days = max(raising_days_list)
        max_falling_days = max(falling_days_list)

        days_dist = [
            falling_days_cnt[i] for i in range(max_falling_days, 0, -1)
        ]
        days_dist += [
            raising_days_cnt[i] for i in range(1, max_raising_days + 1)
        ]

        df = pd.DataFrame({
            "days": [
                days for days in range(-max_falling_days, max_raising_days)
            ],
            "times": days_dist
        })
        return df

    def priceRaiseRate(self) -> list:
        """Calculate daily price increase rate.

        Returns:
            A list of price increase rate.
        """
        cur_cp_list = self._getClosingPrice
        last_cp_list = cur_cp_list[:]
        cur_cp_list.pop(0)  # Remove first cp
        last_cp_list.pop()  # Remove last cp
        cur_cp_list = np.array(cur_cp_list)
        last_cp_list = np.array(last_cp_list)
        return np.round((cur_cp_list - last_cp_list) * 100 / last_cp_list,
                        4).tolist()

    def sma(self, data_list: list, days: int) -> list:
        """Calculate moving average.
        
        Args:
            data_list: Data list to calculate moving average.
            days: The average days.
        Returns:
            A list of moving average.
        """
        data_list = data_list[:]
        total_price = sum(data_list[:days])
        ma_list = [round(total_price / days, 2)]
        while len(data_list) > days:
            cur_price = data_list[days]
            removed_price = data_list.pop(0)
            total_price = total_price - removed_price + cur_price
            ma_list.append(round(total_price / days, 2))
        return ma_list

    def ema(self, data_list: list, days: int) -> list:
        """Calculate exponential moving average.

        Args:
            data_list: Data list to calculate exponential moving average.
            days: The average days.
        Returns:
            A list of exponential moving average.
        """
        data_list = data_list[:]
        total = sum(data_list[:days])
        # The first EMA is SMA.
        ema_list = [round(total / days, 2)]
        for cur_data in data_list[days:]:
            last_ema = ema_list[-1]
            cur_ema = round(
                ((2 * cur_data + (days - 1) * last_ema) / (days + 1)), 2)
            ema_list.append(cur_ema)
        return ema_list

    def dif(self, data_list: list, short=12, long=26) -> list:
        """Calculate DIF.

        Args:
            data_list: Data list to calculate DIF.
            short: short days to calculate EMA. Default is 12 days.
            long: long days to calculate EMA. Default is 26 days.
        Returns:
            A list of DIF.
        """
        ema_short = self.ema(data_list, short)
        ema_long = self.ema(data_list, long)
        dif_days = long - short
        ema_short = ema_short[dif_days:]
        dif_list = np.array(ema_short) - np.array(ema_long)
        return dif_list.tolist()

    def macd(self, data_list: list, short=12, long=26, n=9) -> list:
        """Calculate MACD.
        
        Args:
            data_list: Data list to calculate MACD.
            short: short days to calculate EMA. Default is 12 days.
            long: long days to calculate EMA. Default is 26 days.
            n: the # of days to calculate MACD. Default is 9 days.
        Returns:
            A list of MACD.
        """
        dif_list = self.dif(data_list, short, long)
        macd_list = self.ema(dif_list, n)
        return macd_list
