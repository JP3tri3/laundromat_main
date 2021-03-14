import json
import sys
sys.path.append("..")
import database.database as db
from api.bybit_api import Bybit_Api
import controller.comms as comms
from model.calc import Calc
from model.stop_loss import Stop_Loss
import time

symbol = None
symbolPair = None
limitPriceDifference = None
orderId = None
atr = None

# orderId = ""
# orderPrice = 0
# margin = 5.0
# inputQuantity = 100 * margin
# entry_price = 0.0
# stop_loss = 0
# level = entry_price
# symbolPair = ""
# side = ""
# percentLevel = 0.0
# percentGainedLock = 0.0
# market_type = ""
# totalGain = 0.0

class Orders():

    def __init__(self):
        global symbol
        global limitPriceDifference
        global client

        self.symbol = db.getSymbol()
        self.symbolPair = db.getSymbolPair()
        self.limitPriceDifference = db.getLimitPriceDifference()
        

    api = Bybit_Api(symbolPair)
    calc = Calc(symbolPair)
    sl = Stop_Loss(symbolPair)

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

    def forceLimitOrder(self):
        flag = False
        currentPrice = self.api.lastPrice()
        price = self.calc.calcLimitPriceDifference()

        while(flag == False):
            if (self.activeOrderCheck() == 1):
                if (self.api.lastPrice(self) != currentPrice) and (self.api.lastPrice(self) != price):
                    print("LastPrice: " + str(self.api.lastPrice(self)))
                    print("currentPrice: " + str(currentPrice))
                    print("price: " + str(price))
                    currentPrice = self.api.lastPrice(self)
                    price = self.calc.calcLimitPriceDifference()
                    self.api.changeOrderPrice(price)
                    print("Order Price Updated: " + str(price))
                    print("")
                time.sleep(2)
            else:
                flag = True

    def createOrder(self, side, order_type, stop_loss, inputQuantity):
        global level
        global percentLevel
        global percentGainedLock

        percentGainedLock = 0.0
        percentLevel = 0.0
        flag = False

        if(side == "Buy"):
            stop_loss = (self.api.lastPrice() - stop_loss)
            print("TEST StopLoss = " + str(stop_loss))
        else:
            stop_loss = (self.api.lastPrice() + stop_loss)

        while(flag == False):
            if ((self.activeOrderCheck() == 0) and (self.activePositionCheck() == 0)):
                print("Attempting to place order...")
                entry_price = self.calc.calcLimitPriceDifference(side)
                self.api.placeOrder(price=self.calc.calcLimitPriceDifference(side=side), order_type=order_type, side=side, inputQuantity=inputQuantity, stop_loss=stop_loss)
            else:
                if(order_type == 'Limit'):
                    print("Order ID: " + self.api.getOrderId())
                    self.forceLimitOrder(self.api.getOrderId())
                
                print("")
                print("Confirming Order...")
                
                if ((self.activeOrderCheck() == 0) and (self.activePositionCheck() == 0)):
                    print("Order Failed")
                else:
                    entry_price = float(self.api.getActivePositionEntryPrice())
                    level = entry_price

                    print("Order Successful")
                    print("Entry Price: " + str(entry_price))
                    print("Initial Stop Loss: " + str(stop_loss))
                    print("")
                    flag = True

        # self.sl.updateStopLoss()
        # print("Entry Price: " + str(entry_price))
        # print("Exit Price: " + str(stop_loss))
        # print("Percent Level: " + str(percentLevel))
        # comms.logClosingDetails(
        #     entry_price, level, percentLevel, stop_loss, side, totalGain)
        # comms.updateData("vwap", "1min", 0)

    def closePositionSl(self):
        flag = True
        stopLossInputPrice = Bybit_Info.lastPrice(self)
        print("Forcing Close")
        self.changeStopLoss(Bybit_Info.lastPrice(self) - float(2))
        time.sleep(5)

        while(flag == True):
            if(self.activePositionCheck() == 1):
                if (Bybit_Info.lastPrice(self) > stopLossInputPrice):
                    stopLossInputPrice = Bybit_Info.lastPrice(self)
                    print("")
                    print("Forcing Close")
                    comms.timeStamp()
                    self.changeStopLoss(Bybit_Info.lastPrice(self) - float(2))
                    time.sleep(5)
            else:
                print("Position Closed")
                flag = False

    def closePositionMarket(self):
        positionSize = self.getPositionSize()
        flag = True
        if(side == "Sell"):
            client.Order.Order_new(side="Buy", symbol=symbol, order_type="Market",
                                   qty=positionSize, time_in_force="GoodTillCancel").result()
        else:
            client.Order.Order_new(side="Sell", symbol=symbol, order_type="Market",
                                   qty=positionSize, time_in_force="GoodTillCancel").result()

        while(flag == True):
            if (self.activePositionCheck() == 1):
                print("Error Closing Position")
                self.closePositionMarket()
            else:
                print("Position Closed at: " + str(Bybit_Info.lastPrice(self)))
                flag = False