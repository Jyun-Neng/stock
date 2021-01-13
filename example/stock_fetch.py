from stock import stock
from stock import parser

args = parser.parsing()
stock = stock.Stock(args)
stock.fetchn(args.year, args.month, 12)
if stock.collection.find_one({"stock_id": args.id}) is None:
    stock.addToDB()
else:
    stock.updateToDB()
