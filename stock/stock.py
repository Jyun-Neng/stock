from multipledispatch import dispatch

from . import stockDB
from . import errors


class Stock():

    def __init__(self, id):
        self.id = id
        self.db = stockDB.StockDB("127.0.0.1", 27017)

    @dispatch(int, int, int, str)
    def getInfo(self, day, month, year, info):
        INFO = [
            "date", "trading_vol", "turnover", "opening", "hi", "lo", "closing",
            "transactions"
        ]
        if info not in INFO:
            raise errors.StockDataKeyError(f'Request key is not exist in DB.')
        data = self.db.getData(self.id, day, month, year)
        if data:
            return data[info]
        return

    @dispatch(int, int, str)
    def getInfo(self, month, year, info):
        INFO = [
            "date", "trading_vol", "turnover", "opening", "hi", "lo", "closing",
            "transactions"
        ]
        if info not in INFO:
            raise errors.StockDataKeyError(f'Request key is not exist in DB.')
        monthly_data = self.db.getData(self.id, month, year)
        return [data[info] for data in monthly_data]

    @dispatch(str, int, str)
    def getInfo(self, quarter, year, info):
        INFO = [
            "date", "trading_vol", "turnover", "opening", "hi", "lo", "closing",
            "transactions"
        ]
        if info not in INFO:
            raise errors.StockDataKeyError(f'Request key is not exist in DB.')
        quarterly_data = self.db.getData(self.id, quarter, year)
        return [data[info] for data in quarterly_data]
