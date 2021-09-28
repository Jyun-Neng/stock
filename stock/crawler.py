from datetime import datetime
import requests

from . import errors


class Crawler():

    def getMonthlyData(self, id, month, year):
        """Get stock daily information in specific month from TWSE.

        Args:
            id: stock ID.
            month: the month of required data.
            year: the year of required data.
        Returns:
            The list of daily information.
        """
        # query string parameters
        qs = {"date": "%d%02d01" % (year, month), "stockNo": id}
        resp = requests.get(
            "https://www.twse.com.tw/exchangeReport/STOCK_DAY", params=qs)
        raw_data = resp.json()
        # Check the response of HTTPS request.
        if raw_data['stat'] != 'OK':
            raise errors.InvalidHttpsReqError(f'bad response')
        # Convert RepublicEra to AD year.
        def convertDate(date: str) -> object:
            if int(date.split('/')[0]) < 1900:
                date = '/'.join([str(int(date.split('/')[0]) + 1911)] +
                                date.split('/')[1:])
            return datetime.strptime(date, "%Y/%m/%d")

        def toInt(s):
            s = s.replace(',', '')
            return 0 if s == '' else int(s)

        def toFloat(s):
            if '--' == s:
                return None
            s = s.replace(',', '')
            return 0 if s == '' else float(s)

        def dataFormatter(data):
            # Format raw data fetched from TWSE
            # 0: date
            # 1: trading volumne
            # 2: turnover in value
            # 3: opening price
            # 4: hi
            # 5: lo
            # 6: closing price
            # 7: daliy pricing
            # 8: # of transactions
            return {
                "date": convertDate(data[0]),
                "trading_vol": toInt(data[1]),
                "turnover": toInt(data[2]),
                "opening": toFloat(data[3]),
                "hi": toFloat(data[4]),
                "lo": toFloat(data[5]),
                "closing": toFloat(data[6]),
                "transactios": toInt(data[8])
            }

        return [dataFormatter(daily_info) for daily_info in raw_data["data"]]
