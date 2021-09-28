from stock import stockDB

url = "127.0.0.1"
port = 27017
db = stockDB.StockDB(url, port)
for year in range(2016, 2019):
    for month in range(1, 13):
        print(f'get {year}.{month} data')
        monthly_data = db.getData("2330", month, year)

print(f'get 1st quarter data')
quarterly_data = db.getData("2330", "1st", 2021)
print(quarterly_data)
