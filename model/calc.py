import sys
sys.path.append("..")
import database.database as db
from api.bybit_api import Bybit_Api

symbol = None
symbolPair = None

class Calc():

    api = Bybit_Api()

    def calcFees(self, market_type, inputQuantity):
        return (inputQuantity) * 0.00075 if (market_type == "Market") \
            else (inputQuantity) * 0.00025

    def calcLastGain(self, index):
        total = self.api.lastProfitLoss(index)
        exitPrice = float(self.calcExitPrice())
        return round(float('%.10f' % total) * exitPrice, 3)

    def calcTotalGain(self):
        total = 0
        index = 0
        totalQuantity = 0
        inputQuantity = db.getInputQuantity()
        flag = False

        while(flag == False):
            totalQuantity += self.api.closedProfitLossQuantity(index)
            total += self.calcLastGain(index)

            if totalQuantity < inputQuantity:
                index += 1
            else:
                flag = True

        return total

    def calcTotalCoin(self):
        index = 0
        totalQuantity = 0
        inputQuantity = db.getInputQuantity()
        total = 0.0
        flag = False

        while(flag == False):
            amount = float(self.api.lastProfitLoss(index))
            total += amount
            totalQuantity += self.api.closedProfitLossQuantity(index)

            if totalQuantity < inputQuantity:
                index += 1
            else:
                flag = True

        return ('%.10f' % total)
       

    def calcEntryPrice(self):
        index = 0
        divisible = 1
        lastEntryPrice = self.api.lastEntryPrice(index)
        entry_price = 0
        totalQuantity = 0

        inputQuantity = db.getInputQuantity()
        flag = False

        while(flag == False):
            totalQuantity += self.api.closedProfitLossQuantity(index)
            entry_price += lastEntryPrice

            if totalQuantity < inputQuantity:
                index += 1
                divisible += 1
                print("Index = " + str(index))
            else:
                flag = True

        if (index == 0):
            return entry_price
        else:
            return (entry_price / divisible)


    def calcExitPrice(self):
        index = 0
        divisible = 1
        lastExitPrice = self.api.lastExitPrice(index)
        exit_price = 0
        totalQuantity = 0
        inputQuantity = db.getInputQuantity()
        flag = False

        while(flag == False):
            totalQuantity += self.api.closedProfitLossQuantity(index)
            exit_price += lastExitPrice

            if totalQuantity < inputQuantity:
                index += 1
                divisible += 1
                print("Index = " + str(index))
            else:
                flag = True
        
        if (index == 0):
            return exit_price
        else:
            return (exit_price / divisible)


    def calcOnePercentLessEntry(self):
        leverage = db.getLeverage()
        entry_price = self.api.getActivePositionEntryPrice()
        return(float(entry_price) * 0.01) / leverage
         
    def calcPercentGained(self):
        try:
            side = self.api.getPositionSide()
            entry_price = self.api.getActivePositionEntryPrice()
            lastPrice = self.api.lastPrice()
            leverage = db.getLeverage()

            difference = (lastPrice - entry_price) if(side == "Buy") \
                else (entry_price - lastPrice)

            percent = (difference/lastPrice) * 100
            return float(round(percent * leverage, 3))

        except Exception as e:
            print("an exception occured - {}".format(e))

    def calcLimitPriceDifference(self, side):
        lastPrice = self.api.lastPrice()
        difference = db.getLimitPriceDifference()

        return (lastPrice - difference) if (side == 'Buy') \
            else (lastPrice + difference)