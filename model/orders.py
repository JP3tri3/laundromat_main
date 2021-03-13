import json
import sys
sys.path.append("..")
import database.database as db
from api.bybit_api import Bybit_Api
import controller.comms as comms
from model.calc import Calc
import time

symbol = None
symbolPair = None
limitPriceDifference = None
orderId = None
atr = None

class Orders():

    def __init__(self):
        global symbol
        global limitPriceDifference
        global client

        self.symbol = db.getSymbol()
        self.symbolPair = db.getSymbolPair()
        self.limitPriceDifference = db.getLimitPriceDifference()
        

    api = Bybit_Api(symbol, symbolPair)
    calc = Calc(symbol, symbolPair)

    def test(self):
        return(self.symbolPair)

    def activeOrderCheck(self):
        global orderId
        order = self.api.getOrder()
        if (order == []):
            print("no pending orders")
            return 0
        else:
            self.orderId = self.api.getOrderId()
            return 1

    def activePositionCheck(self):
        try:
            positionValue = self.api.getPositionValue()
            if(positionValue != "0"):
                return 1
            else:
                return 0
        except Exception as e:
            print("Active Position Check Exception Occured...")
            print("Trying again...")
            time.sleep(2)
            self.activePositionCheck()

    def inputAtr(self):
        global atr
        flag = False
        print("")
        while(flag == False):
            atr = input("Input ATR: ")
            if(atr.isnumeric()):
                print("ATR input accepted for SL: " + str(atr))
                flag = True
            else:
                print("Invalid Input, try again...")


    def placeOrder(self, price, side, order_type, inputQuantity, margin):

        if(side == "Buy"):
            stop_loss = self.api.lastPrice() - float(self.calc.calcOnePercentLessEntry(price, margin))
        else:
            stop_loss = self.api.lastPrice() + float(self.calc.calcOnePercentLessEntry(price, margin))
        print("Initial Stop Loss: " + str(stop_loss))
        self.api.placeOrder(price, side, order_type, inputQuantity, stop_loss)
        print("Order placed successfully")
        print("Order ID: ")
        print(self.api.getOrderId())
        print("")

