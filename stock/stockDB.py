from pymongo import MongoClient


class StockDB():

    def __init__(self, url: str, port: int):
        client = MongoClient(url, port)
        db = client["stock"]
        self.collection = db["twse"]
