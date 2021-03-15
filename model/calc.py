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
        if (market_type == "market"):
            entryFee = (inputQuantity) * 0.00075
        else:
            entryFee = (inputQuantity) * 0.00025
        print("Entry Fee: " + str(entryFee))
        return entryFee

    def calcTotalGain(self, market_type, inputQuantity, percentGained):
        total = (inputQuantity * percentGainedLock)/100
        if (market_type == "market"):
            total = total - self.calculateFees("market")
        else:
            total = total + self.calculateFees("limit")

        return total

    def calcOnePercentLessEntry(self, entry_price, margin):
        onePercentDifference = (float(self.api.getActivePositionEntryPrice()) * 0.01) / margin
        return onePercentDifference

    def calcPercentGained(self, side, entry_price):
        # value = inputQuantity / entry_price
        entry_price = self.api.getActivePositionEntryPrice()
        if(side == "Buy"):
            difference = (self.api.lastPrice() - float(entry_price))
        else:
            difference = (float(entry_price) - self.api.lastPrice())

        percent = (difference/self.api.lastPrice()) * 100
        percentWithMargin = (percent) * margin
        return float(percentWithMargin)

    def calcLimitPriceDifference(self, side):
        if(side == "Buy"):
            limitPrice = self.api.lastPrice() - db.getLimitPriceDifference()
        else:
            limitPrice = self.api.lastPrice() + db.getLimitPriceDifference()             
        return limitPrice
