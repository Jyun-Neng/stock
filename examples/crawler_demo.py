from stock import crawler

cr = crawler.Crawler()
monthly_data = cr.getMonthlyData("2330", 8, 2021)
print(monthly_data)
