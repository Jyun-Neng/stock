# Stock

台灣股市資料收集及分析系統

- [Stock](#stock)
  - [Requirements](#requirements)
  - [Anaylsis Tools](#anaylsis-tools)
  - [Quick Start](#quick-start)
  - [Example](#example)

---

## Requirements

- Python 3.x
- mongoDB
- requests >= 2.24.0 (python module)
- pandas >= 1.2.0 (python module)
- numpy >= 1.19.1 (python module)
- plotly >= 4.11.0 (python module)
- pymongo >= 3.11.0 (python module)
- lxml >= 4.6.1 (python module)

## Anaylsis Tools

相關分析工具都在 `analytics.py`

目前已經建好的分析工具:

- 連續漲跌天數分佈 `raisingFallingDaysDist()`
- 每日漲跌幅百分比 `priceRaiseRate()`
- 移動平均計算 `movingAvg()`

## Quick Start

這邊只說明基本股票資訊抓取的操作方法，分析工具請看 [Analysis Tools](#anaylsis-tools)

擷取股票資訊

```python
from stock import stock
from stock import parser

args = parser.parsing() # 獲取指令行參數
stock = stock.Stock(args)
stock.fetch(args.year, args.month) # 擷取指定月份的股票資訊
stock.fetchFrom(args.year, args.month) # 擷取從指定月份到今天的股票資訊
```

建立 `Stock` 物件所需的參數可透過 `parser.parsing()` 來從終端機指令行獲取。參數說明如下，其中 `--id` 為必要參數才能知道要抓取哪支股票資訊

```
usage: stock_fetch.py [-h] [--year YEAR] [--month MONTH] [--url URL] [--port PORT] --id ID

optional arguments:
  -h, --help            show this help message and exit
  --year YEAR, -y YEAR  The year when fetch start
  --month MONTH, -m MONTH
                        The month when fetch start
  --url URL, -u URL     MongoDB url connection
  --port PORT, -p PORT  MongoDB listening port
  --id ID, -i ID        Stock ID
```

儲存擷取的股票資料到 mongoDB

```python
from stock import stock
from stock import parser

args = parser.parsing()
stock = stock.Stock(args)
stock.fetch(args.year, args.month)
stock.addToDB()
# or stock.updateToDB() 
# addToDB 使用於第一次擷取選定股票資訊
# updateToDB 是當擷取的股票曾經儲存在 db 裡時使用
```

產生股票資訊的 csv 檔案

```python
from stock import stock
from stock import parser

args = parser.parsing()
stock = stock.Stock(args)
stock.fetchFrom(args.year, args.month)
stock.writeDailyInfo() # 產生 csv 檔案
```

## Example

```
$ python -m example.stock_fetch -i 2885 -y 2020 -m 12
```