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
        

    api = Bybit_Api()
    calc = Calc()

    def test(self):
        return(self.symbolPair)

    def activeOrderCheck(self):
        global orderId
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

    def createOrder(self, side, order_type, stop_loss, inputQuantity):
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
            stop_loss = (self.api.lastPrice() - stop_loss) if (side == 'Buy') \
                else (self.api.lastPrice() + stop_loss)
            print("TEST StopLoss = " + str(stop_loss))

            while(flag == False):
                if ((self.activeOrderCheck() == 0) and (self.activePositionCheck() == 0)):
                    print("Attempting to place order...")
                    entry_price = self.calc.calcLimitPriceDifference(side)
                    self.api.placeOrder(price=self.calc.calcLimitPriceDifference(side=side), order_type=order_type, side=side, inputQuantity=db.getInputQuantity(), stop_loss=stop_loss, reduce_only=False)
                    
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
                        print("Initial Stop Loss: " + str(stop_loss))
                        print("")
                        flag = True

        # self.sl.updateStopLoss()
        # comms.logClosingDetails(
        #     entry_price, level, percentLevel, stop_loss, side, totalGain)
        # comms.updateData("vwap", "1min", 0)

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
            self.api.placeOrder(self.api.lastPrice(), 'Market', 'Buy', positionSize, 0)
        else:
            self.api.placeOrder(self.api.lastPrice(), 'Market', 'Sell', positionSize, 0)

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