# Welcome to Stock

[**Requirements**](#requirements)
| [**Installation**](#installation)
| [**Quick Start**](#quick-start)
| [**Examples**](https://github.com/Jyun-Neng/stock/tree/master/examples)


台灣股市資料收集及分析系統。

`stock` 目前可以從 [TWSE](https://www.twse.com.tw/zh/) 網站爬取台灣個股每天的量價資訊，以供使用者做後續的分析處理。


## Requirements

- Python 3.x
- mongoDB
- requests >= 2.24.0 (python module)
- pymongo >= 3.11.0 (python module)
- lxml >= 4.6.1 (python module)

## Installation

你可以直接執行 `setup.py` 來安裝此 package。

```
> python setup.py install
```

## Quick Start

基本個股資訊抓取方法，`stock` 會把你需要的個股資訊都從網站上存取下來，並儲存在自己建立的 database。

`Stock` class 提供三種抓取個股資訊的方法，分別是：
- 抓取個股某日資訊 (`getInfo(day, month, year, info)`)
- 抓取個股某月資訊 (`getInfo(month, year, info)`)
- 抓取個股某季資訊 (`getInfo(quarter, year, info)`)

*Note:* `quarter` 要給的參數是 `"1st", "2nd", "3rd", "4th"`。

這些抓取資訊的 functions 都叫 `getInfo`，差別在於輸入的參數。其中有項參數 `info` 是用來決定要抓取個股的什麼資訊。目前能夠使用 `getInfo` 獲取的資訊有:
- 日期 (date)
- 每日成交股數 (trading_vol)
- 每日成交金額 (turnover)
- 每日開盤價 (opening)
- 每日收盤價 (closing)
- 每日最高價 (hi)
- 每日最低價 (lo)
- 每日成交量 (transactions)

下面程式碼示範如何使用 `Stock` 的 `getInfo` function 獲得個股每日最高價的資訊。

```python
from stock import stock

s = stock("2330")
s.getInfo(8, 2021, "hi") # 抓取 2021 年 8 月的每日最高價
```
另外也可以參考 [Examples](https://github.com/Jyun-Neng/stock/tree/master/examples) 內的一些範例程式。