import json
import sys
sys.path.append("..")
import database.database as db
from api.bybit_api import Bybit_Api
import controller.comms as comms
from model.calc import Calc
import time
import asyncio


class Orders:
    
    def __init__(self):
        self.trade_record_id = 0
        self.symbol = conn.viewDbValue('trades', self.trade_id, 'symbol')
        self.symbol_pair = conn.viewDbValue('trades', self.trade_id, 'symbol_pair')
        self.atr = None

        self.api = Bybit_Api()
        self.calc = Calc()

    def initiateCreateTradeRecord(self):
        global trade_record_id
        self.trade_record_id = self.trade_record_id + 1

        conn.createTradeRecord(self.trade_record_id, self.symbol_pair, 0, 0, 0, 0, 0, 0, 0, 'empty', 0)

    def activeOrderCheck(self):
        order = self.api.getOrder()
        return 0 if (order == []) else 1


    def activePositionCheck(self):
        try:
            positionValue = self.api.getPositionValue()
            return 1 if (positionValue != '0') else 0
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

    def forceLimitOrder(self, side):
        flag = False
        currentPrice = self.api.lastPrice()
        price = self.calc.calcLimitPriceDifference(side=side)

        while(flag == False):
            if (self.activeOrderCheck() == 1):
                if (self.api.lastPrice() != currentPrice) and (self.api.lastPrice() != price):
                    print("LastPrice: " + str(self.api.lastPrice()))
                    print("currentPrice: " + str(currentPrice))
                    print("price: " + str(price))
                    currentPrice = self.api.lastPrice()
                    price = self.calc.calcLimitPriceDifference(side=side)
                    self.api.changeOrderPrice(price)
                    print("Order Price Updated: " + str(price))
                    print("")
                time.sleep(2)

            else:
                flag = True

    def createOrder(self, side, order_type, inputQuantity):
        global level
        global percentLevel
        global percentGainedLock

        percentGainedLock = 0.0
        percentLevel = 0.0
        flag = False

        if (self.activeOrderCheck() == 1):
            print("Current Active Order...")
            print("Create Order Cancelled")
        elif (self.activePositionCheck() == 1):
            print("Current Active Position...")
            print("Create Order Cancelled")
        else:

            initialStopLoss = (self.api.lastPrice() - (2*self.calc.calcOnePercent())) if (side == 'Buy') \
                else (self.api.lastPrice() + (2*self.calc.calcOnePercent()))
            print("onePercentCheck: " + str(self.calc.calcOnePercent()))
            while(flag == False):
                if ((self.activeOrderCheck() == 0) and (self.activePositionCheck() == 0)):
                    print("Attempting to place order...")
                    entry_price = self.calc.calcLimitPriceDifference(side)
                    self.api.placeOrder(price=self.calc.calcLimitPriceDifference(side=side), order_type=order_type, side=side, inputQuantity=conn.viewDbValue('trades', trade_id, 'input_quantity'), stop_loss=initialStopLoss, reduce_only=False)
                    
                    db.setSide(side)
                    db.setEntryPrice(self.api.getActivePositionEntryPrice)

                    if(order_type == 'Limit'):
                        print("")
                        print("Retrieving Order ID...")
                        print("Order ID: " + str(self.api.getOrderId()))
                        self.forceLimitOrder(side=side)
                else:
                    print("")
                    print("Confirming Order...")
                    
                    if((self.activeOrderCheck() == 0) and (self.activePositionCheck() == 0)):
                        print("Order Failed")
                    else:
                        entry_price = float(self.api.getActivePositionEntryPrice())
                        print("")
                        print("Order Successful")
                        print("Entry Price: " + str(entry_price))
                        print("Initial Stop Loss: " + str(initialStopLoss))
                        print("")
                        flag = True

    def closePositionSl(self):
        flag = True
        stopLossInputPrice = self.api.lastPrice()
        print("Forcing Close")
        self.api.changeStopLoss(self.api.lastPrice() - float(2))
        time.sleep(5)

        while(flag == True):
            if(self.activePositionCheck() == 1):
                if (self.api.lastPrice() > stopLossInputPrice):
                    stopLossInputPrice = self.api.lastPrice()
                    print("")
                    print("Forcing Close")
                    comms.timeStamp()
                    self.api.changeStopLoss(self.api.lastPrice() - float(2))
                    time.sleep(5)
            else:
                print("Position Closed")
                flag = False

    def closePositionMarket(self):
        positionSize = self.api.getPositionSize()
        flag = True
        if(self.api.getPositionSide() == "Sell"):
            self.api.placeOrder(self.api.lastPrice(), 'Market', 'Buy', positionSize, 0, True)
        else:
            self.api.placeOrder(self.api.lastPrice(), 'Market', 'Sell', positionSize, 0, True)

        while(flag == True):
            if (self.activePositionCheck() == 1):
                print("Error Closing Position")
                self.closePositionMarket()
            else:
                print("Position Closed at: " + str(self.api.lastPrice()))
                flag = False

    def forceLimitClose(self):
        flag = False
        currentPrice = self.api.lastPrice()
        inputQuantity = self.api.getPositionSize()
        side = self.api.getPositionSide()
        print("CurrentPrice: " + str(currentPrice))

        side = 'Sell' if (side == 'Buy') else 'Buy'

        while(flag == False):
            if(self.activePositionCheck() == 1) and (self.activeOrderCheck() == 0):
                print("Print Order Check")
                price = self.calc.calcLimitPriceDifference(side=side)
                self.api.placeOrder(price=price, order_type='Limit', side=side, inputQuantity=inputQuantity, stop_loss=0, reduce_only=True)
                time.sleep(2)
            elif (self.activePositionCheck() == 1) and (self.activePositionCheck() == 1):
                if (self.api.lastPrice() != currentPrice) and (self.api.lastPrice() != price):
                    print("LastPrice: " + str(self.api.lastPrice()))
                    print("currentPrice: " + str(currentPrice))
                    print("price: " + str(price))
                    currentPrice = self.api.lastPrice()
                    price = self.calc.calcLimitPriceDifference(side=side)
                    print("Price change: " + str(price))
                    self.api.changeOrderPrice(price)
                    print("Order Price Updated: " + str(price))
                    print("")
                time.sleep(2)
            elif(self.activePositionCheck() == 0) and (self.activeOrderCheck() == 0):
                flag = True
            else:
                print("Something's fucking wrong.")
                sleep(2)