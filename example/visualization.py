from stock import stock
from stock import parser
import pandas as pd
from datetime import datetime

args = parser.parsing()
stock = stock.Stock(args)

cp_list = stock.getClosingPrice
volumes = stock.getTradingVolume
date_list = stock.getDate
# Calculate moving average of closing price.
cp_ma_3 = stock.sma(cp_list, 3)
cp_ma_5 = stock.sma(cp_list, 5)
cp_ma_10 = stock.sma(cp_list, 10)
cp_ma_20 = stock.sma(cp_list, 20)
cp_ma = [cp_ma_3, cp_ma_5, cp_ma_10, cp_ma_20]
# Calculate moving average of trading volume.
vol_ma_5 = stock.sma(volumes, 5)
vol_ma_10 = stock.sma(volumes, 10)
vol_ma_20 = stock.sma(volumes, 20)
vol_ma = [vol_ma_5, vol_ma_10, vol_ma_20]
# Calculate MACD and DIF
dif_12_26 = stock.dif(cp_list, 12, 26)
macd_9 = stock.macd(cp_list, 12, 26, 9)
# Plot
stock.plotMA(cp_ma, cp_list, date_list)
stock.plotVA(vol_ma, volumes, date_list)
stock.plotPriceVolume(cp_ma, cp_list, vol_ma, volumes, date_list)
stock.plotMACD(macd_9, dif_12_26, date_list)