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

    def calcTotalGain(self, market_type, inputQuantity, percentGained):
        total = (inputQuantity * percentGainedLock)/100
        return total - self.calcFees("Market") if (market_type == "Market") \
            else total + self.calcFees("Limit")


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
        return float(percent * margin)

    def calcLimitPriceDifference(self, side):
        lastPrice = self.api.lastPrice()
        difference = db.getLimitPriceDifference()

        return (lastPrice - difference) if (side == 'Buy') \
            else (lastPrice + difference)