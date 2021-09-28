from stock import stock

stock_id = "2330"
s = stock.Stock(stock_id)
print(s.getInfo(8, 2021, "date"))
