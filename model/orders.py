import json
import sys
sys.path.append("..")
from database.database import Database
from api.bybit_api import Bybit_Api
import controller.comms as comms
from model.calc import Calc
import time
import asyncio


class Orders:
    
    def __init__(self):
        self.atr = None
        self.total_profit_loss = 0

        self.api = Bybit_Api()
        self.calc = Calc()
        self.db = Database()

    def logClosingDetails(self):
        global total_profit_loss

        trade_kv_dict = self.db.get_trade_vales()

        symbol_pair = trade_kv_dict['symbol_pair']
        entry_price = calc.calcEntryPrice()
        exit_price = calc.calcExitPrice()
        stop_loss = trade_kv_dict['stop_loss']
        percent_gain = trade_kv_dict['percent_gain']
        side =  trade_kv_dict['side']
        total_gain = calc.calcTotalGain()
        total_coin = calc.calcTotalCoin()
        time = str(comms.timeStamp())

        total_number_trades = trade_kv_dict['trade_record_id'] + 1
        self.db.set_trade_record_id(total_number_trades)
        self.total_profit_loss += total_gain 

        conn.createTradeRecord(trade_id_input, symbol_pair, entry_price, exit_price, stop_loss, percent_gain, total_gain, total_coin, self.total_profit_loss, time)

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

    def createOrder(self, side_input, order_type, inputQuantity):
        global level
        global percentLevel
        global percentGainedLock

        percentGainedLock = 0.0
        percentLevel = 0.0
        flag = False
        self.db.set_side(side_input)

        if (self.activeOrderCheck() == 1):
            print("Current Active Order...")
            print("Create Order Cancelled")
        elif (self.activePositionCheck() == 1):
            print("Current Active Position...")
            print("Create Order Cancelled")
        else:

            initialStopLoss = (self.api.lastPrice() - (2*self.calc.calcOnePercent())) if (side_input == 'Buy') \
                else (self.api.lastPrice() + (2*self.calc.calcOnePercent()))

            while(flag == False):
                if ((self.activeOrderCheck() == 0) and (self.activePositionCheck() == 0)):
                    print("Attempting to place order...")
                    entry_price = self.calc.calcLimitPriceDifference(side_input)
                    self.api.placeOrder(price=self.calc.calcLimitPriceDifference(side=side_input), order_type=order_type, side=side_input, inputQuantity=self.db.get_input_quantity(), stop_loss=initialStopLoss, reduce_only=False)

                    if(order_type == 'Limit'):
                        print("")
                        print("Retrieving Order ID...")
                        print("Order ID: " + str(self.api.getOrderId()))
                        self.forceLimitOrder(side=side_input)
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