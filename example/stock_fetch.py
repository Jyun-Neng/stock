from stock import stock
from stock import parser

args = parser.parsing()
stock = stock.Stock(args)
stock.fetchFrom(args.year, args.month)
if stock.collection.find_one({"stock_id": args.id}) is None:
    stock.addToDB()
else:
    stock.updateToDB()
df = stock.raisingFallingDaysDist()
stock.plot2DHist(df)
