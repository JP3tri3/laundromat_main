import comms
import json
import sys
sys.path.append("..")
import database.database as db
import controller.comms as commms
from api.bybit_api import Bybit_Api

orderId = ""
orderPrice = 0
margin = 5.0
inputQuantity = 100 * margin
entry_price = 0.0
stop_loss = 0
level = entry_price
symbolPair = ""
side = ""
percentLevel = 0.0
percentGainedLock = 0.0
market_type = ""
totalGain = 0.0


    # Order Functions

# test


    def calculateFees(self, market_type):
        if (market_type == "market"):
            entryFee = (inputQuantity) * 0.00075
        else:
            entryFee = (inputQuantity) * 0.00025
        print("Entry Fee: " + str(entryFee))
        return entryFee

    def calculateTotalGain(self):
        global totalGain

        total = (inputQuantity * percentGainedLock)/100
        if (market_type == "market"):
            total = total - calculateFees("market")
        else:
            total = total + calculateFees("limit")

        totalGain = total
        return total

    def calculateOnePercentLessEntry(self):
        onePercentDifference = (float(entry_price) * 0.01) / margin
        return onePercentDifference

    def calculatePercentGained(self):
        # value = inputQuantity / entry_price
        if(side == "Buy"):
            difference = (Bybit_Info.lastPrice(self) - float(entry_price))
        else:
            difference = (float(entry_price) - Bybit_Info.lastPrice(self))

        percent = (difference/Bybit_Info.lastPrice(self)) * 100
        percentWithMargin = (percent) * margin
        return float(percentWithMargin)

        # Active Checks



    def activePositionCheck(self):
        try:
            position = client.Positions.Positions_myPosition(
                symbol="BTCUSD").result()
            positionResult = position[0]['result']
            positionValue = positionResult['position_value']
            if(positionValue != "0"):
                return 1
            else:
                return 0
        except Exception as e:
            print("Active Position Check Exception Occured...")
            print("Trying again...")
            time.sleep(2)
            activePositionCheck()



    # traceback test

    def printActivePosition(self):
        position = client.Positions.Positions_myPosition(
            symbol=symbol).result()
        positionResult = position[0]['result']
        positionValue = positionResult['position_value']
        return(positionValue)

    def printActivePositionResult(self):
        position = client.Positions.Positions_myPosition(
            symbol=symbol).result()
        positionResult = position[0]['result']
        positionValue = positionResult['position_value']
        return(positionResult)

    def activePositionEntryPrice(self):
        position = client.Positions.Positions_myPosition(
            symbol=symbol).result()
        positionResult = position[0]['result']
        positionEntryPrice = positionResult['entry_price']
        return float(positionEntryPrice)

    # Create Functions:

    def calcLimitPriceDifference(self):
        if(side == "Buy"):
            limitPrice = Bybit_Info.lastPrice(self) - limitPriceDifference
        else:
            limitPrice = Bybit_Info.lastPrice(self) + limitPriceDifference
        return limitPrice

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

    def placeOrder(self, order_type, price):
        global orderId

        if(side == "Buy"):
            stop_loss = Bybit_Info.lastPrice(
                self) - float(self.calculateOnePercentLessEntry())
        else:
            stop_loss = Bybit_Info.lastPrice(
                self) + float(self.calculateOnePercentLessEntry())
        print("Initial Stop Loss: " + str(stop_loss))
        try:
            print(
                f"sending order {price} - {side} {symbol} {order_type} {stop_loss}")
            order = client.Order.Order_new(side=side, symbol=symbol, order_type=order_type,
                                           qty=inputQuantity, price=price, time_in_force="PostOnly", stop_loss=str(stop_loss)).result()
            orderId = str(order[0]['result']['order_id'])
        except Exception as e:
            print("an exception occured - {}".format(e))
            return False
        return order

    def changeOrderPrice(self, price, orderId):
        global orderPrice
        if (price != orderPrice):
            client.Order.Order_replace(
                symbol=symbol, order_id=orderId, p_r_price=str(price)).result()
            comms.timeStamp()
            print("Updating Order Price")

    def forceOrder(self, orderId):
        flag = False
        currentPrice = Bybit_Info.lastPrice(self)
        price = self.calcLimitPriceDifference()

        while(flag == False):
            if (self.activeOrderCheck() == 1):
                if (Bybit_Info.lastPrice(self) != currentPrice) and (Bybit_Info.lastPrice(self) != price):
                    print("LastPrice: " + str(Bybit_Info.lastPrice(self)))
                    print("currentPrice: " + str(currentPrice))
                    print("price: " + str(price))
                    currentPrice = Bybit_Info.lastPrice(self)
                    price = self.calcLimitPriceDifference()
                    self.changeOrderPrice(price, orderId)
                    print("Order Price Updated: " + str(price))
                    print("")
                time.sleep(2)
            else:
                flag = True

    def createOrder(self, sideInput, symbolInput, order_type):
        global orderPrice
        global entry_price
        global level
        global side
        global symbol
        global percentLevel
        global percentGainedLock
        global market_type

        market_type = order_type
        percentGainedLock = 0.0
        percentLevel = 0.0
        symbol = symbolInput
        side = sideInput
        flag = False
        entry_price = self.calcLimitPriceDifference()

        while(flag == False):
            if ((self.activeOrderCheck() == 0) and (self.activePositionCheck() == 0)):
                print("Attempting to place order...")
                self.placeOrder(order_type=order_type,
                                price=self.calcLimitPriceDifference())
                orderPrice = self.calcLimitPriceDifference()
            else:
                self.forceOrder(orderId)
                print("")
                print("Confirming Order...")
                if ((self.activeOrderCheck() == 0) and (self.activePositionCheck() == 0)):
                    print("Order Failed")
                else:
                    entry_price = float(self.activePositionEntryPrice())
                    level = entry_price
                    print("Entry Price: " + str(entry_price))
                    print("Order Successful")
                    flag = True

        self.updateStopLoss()
        print("Entry Price: " + str(entry_price))
        print("Exit Price: " + str(stop_loss))
        print("Percent Level: " + str(percentLevel))
        comms.logClosingDetails(
            entry_price, level, percentLevel, stop_loss, side, totalGain)
        comms.updateData("vwap", "1min", 0)

    def createMarketOrder(self, sideInput, symbolInput):
        global orderPrice
        global entry_price
        global level
        global side
        global symbol
        global percentLevel
        global percentGainedLock
        global market_type
        global totalGain

        market_type = "market"
        percentGainedLock = 0.0
        percentLevel = 0.0
        symbol = symbolInput
        side = sideInput
        flag = False
        entry_price = Bybit_Info.lastPrice(self)
        totalGain = 0.0

        while(flag == False):
            if ((self.activeOrderCheck() == 0) and (self.activePositionCheck() == 0)):
                print("Attempting to place order...")
                self.placeOrder(order_type="Market",
                                price=Bybit_Info.lastPrice(self))
                orderPrice = Bybit_Info.lastPrice(self)
            else:
                print("")
                print("Confirming Order...")
                if ((self.activeOrderCheck() == 0) and (self.activePositionCheck() == 0)):
                    print("Order Failed or active position")
                else:
                    entry_price = float(self.activePositionEntryPrice())
                    level = entry_price
                    print("Entry Price: " + str(entry_price))
                    print("Order Successful")
                    flag = True

        self.updateStopLoss()
        print("Entry Price: " + str(entry_price))
        print("Exit Price: " + str(stop_loss))
        print("Percent Level: " + str(percentLevel))
        self.calculateTotalGain()
        comms.logClosingDetails(
            entry_price, level, percentGainedLock, stop_loss, side, totalGain)
        print(totalGain)

    # Close & Stoploss

    def updateStopLoss(self):
        flag = True

        while (flag == True):
            if(self.activePositionCheck() == 1):
                if (comms.viewData("vwap", "1min") != "null"):
                    self.closePositionMarket()
                else:
                    if(side == "Buy"):
                        if(Bybit_Info.lastPrice(self) > level):
                            self.calculateStopLoss()
                            time.sleep(4)
                        else:
                            print("Waiting...")
                            print("Percent Gained: " +
                                  str(self.calculatePercentGained()))
                            print("Level: " + str(level))
                            print("BTC Price: " + str(Bybit_Info.lastPrice(self)))
                            print("")
                            time.sleep(4)
                    else:
                        if(Bybit_Info.lastPrice(self) < level):
                            self.calculateStopLoss()
                            time.sleep(4)
                        else:
                            print("Waiting...")
                            print("Percent Gained: " +
                                  str(calculatePercentGained()))
                            print("Level: " + str(level))
                            print("BTC Price: " + str(Bybit_Info.lastPrice(self)))
                            print("")
                            time.sleep(4)
            else:
                print("Position Closed")
                print("")
                flag = False

    def changeStopLoss(self, slAmount):
        client.Positions.Positions_tradingStop(
            symbol=symbol, stop_loss=str(slAmount)).result()
        print("")
        print("Changed stop Loss to: " + str(stop_loss))

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

    def calculateStopLoss(self):
        global level
        global stop_loss
        global percentLevel
        global percentGainedLock
        processTrigger = percentLevel
        percentGained = self.calculatePercentGained()

        print("calculating Stop Loss:")

        if (percentLevel < 0.25):
            if (side == "Buy"):
                stop_loss = (entry_price - self.calculateOnePercentLessEntry())
            else:
                stop_loss = (entry_price + self.calculateOnePercentLessEntry())
            percentLevel = 0.25
        elif (percentGained >= 0.25) and (percentLevel >= 0.25) and (percentLevel < 0.5):
            stop_loss = entry_price
            percentLevel = 0.5
            level = Bybit_Info.lastPrice(self)
        elif (percentGained >= 0.5) and (percentLevel < 0.75):
            stop_loss = level
            percentLevel = 0.75
            level = Bybit_Info.lastPrice(self)
        elif (percentGained >= 0.75) and (percentLevel < 1.0):
            stop_loss = level
            percentLevel = 1.0
            level = Bybit_Info.lastPrice(self)
        elif (percentGained > (percentLevel + 0.5)):
            stop_loss = level
            percentLevel += 0.5
            level = Bybit_Info.lastPrice(self)

        if (processTrigger != percentLevel):
            print("Changing Stop Loss")
            percentGainedLock = percentGained
            self.changeStopLoss(stop_loss)
            print("Percent Gained: " + str(percentGainedLock))
            print("Percent Level: " + str(percentLevel))
            print("Level: " + str(level))
            print("Stop Loss: " + str(stop_loss))
            print("")
            processTrigger = percentLevel

    # def calculateStopLoss50():
    #     global level
    #     global stop_loss
    #     global percentLevel
    #     processTrigger = percentLevel
    #     percentGained = calculatePercentGained()

    #     print("calculating Stop Loss:")

    #     if (percentLevel < 0.50):
    #         if (side == "Buy"):
    #             stop_loss = (entry_price - calculateOnePercentLessEntry())
    #         else:
    #             stop_loss = (entry_price + calculateOnePercentLessEntry())
    #         percentLevel = 0.50
    #         print("Percent Gained: " + str(percentGained))
    #         print("Percent Level: " + str(percentLevel))
    #         print("Level: " + str(level))
    #         print("Stop Loss: " + str(stop_loss))
    #         print("")
    #     elif (percentGained >= 0.5) and (percentLevel >= 0.5) and (percentLevel < 1.0):
    #         stop_loss = entry_price
    #         percentLevel = 1
    #         level = Bybit_Info.lastPrice(self)
    #         print("Percent Gained: " + str(percentGained))
    #         print("Percent Level: " + str(percentLevel))
    #         print("Level: " + str(level))
    #         print("Stop Loss: " + str(stop_loss))
    #         print("")
    #     elif (percentGained > (percentLevel + 1.0)):
    #         stop_loss = level
    #         percentLevel += 0.5
    #         level = Bybit_Info.lastPrice(self)
    #         print("Percent Gained: " + str(percentGained))
    #         print("Percent Level: " + str(percentLevel))
    #         print("Level: " + str(level))
    #         print("Stop Loss: " + str(stop_loss))
    #         print("")

    #     if (processTrigger != percentLevel):
    #         print("Changing Stop Loss")
    #         print(str(stop_loss))
    #         changeStopLoss(stop_loss)
