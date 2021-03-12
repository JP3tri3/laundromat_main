import json
import sys
sys.path.append("..")
import database.database as db
from api.bybit_api import Bybit_Api

symbol = None
symbolPair = None
limitPriceDifference = None
orderId = None

class Orders():

    def __init__(self):
        global symbol
        global limitPriceDifference
        global client

        self.symbol = db.getSymbol()
        self.symbolPair = db.getSymbolPair()
        self.limitPriceDifference = db.getLimitPriceDifference()
        

    api = Bybit_Api(symbol, symbolPair)


    def activeOrderCheck(self):
        global orderId
        order = self.api.getOrder()
        if (order == []):
            print("no pending orders")
            return 0
        else:
            self.orderId = self.api.getOrderId()
            return 1


    def test(self):
        return self.api.getPositionSize()
        # return self.api.getPosition()