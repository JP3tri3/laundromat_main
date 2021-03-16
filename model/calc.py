import sys
sys.path.append("..")
import database.database as db
from api.bybit_api import Bybit_Api

symbol = None
symbolPair = None

class Calc():

    # def __init__(self):


    api = Bybit_Api()


    def calcFees(self, market_type, inputQuantity):
        return (inputQuantity) * 0.00075 if (market_type == "Market") \
            else (inputQuantity) * 0.00025

    def calcLastGain(self, index):
        total = self.api.lastProfitLoss(index)
        exitPrice = float(self.api.exitPriceProfitLoss(index))
        return round(float("%.10f" % total) * exitPrice, 3)

    def calcTotalGain(self):
        total = 0
        flag = False
        index = 0
        totalQuantity = 0

        while(flag == False):
            inputQuantity = db.getInputQuantity()
            totalQuantity += self.api.closedProfitLossQuantity(index)
            total += self.calcLastGain(index)

            if totalQuantity < inputQuantity:
                index += 1
            else:
                flag = True
        
        return total
        






    def calcOnePercentLessEntry(self):
        margin = db.getMargin()
        entry_price = self.api.getActivePositionEntryPrice()
        return(float(entry_price) * 0.01) / margin
         

    def calcPercentGained(self):
        # value = inputQuantity / entry_price
        side = self.api.getPositionSide()
        entry_price = self.api.getActivePositionEntryPrice()
        lastPrice = self.api.lastPrice()
        margin = db.getMargin()

        difference = (lastPrice - entry_price) if(side == "Buy") \
            else (entry_price - lastPrice)

        percent = (difference/lastPrice) * 100
        return float(round(percent * margin, 3))

    def calcLimitPriceDifference(self, side):
        lastPrice = self.api.lastPrice()
        difference = db.getLimitPriceDifference()

        return (lastPrice - difference) if (side == 'Buy') \
            else (lastPrice + difference)