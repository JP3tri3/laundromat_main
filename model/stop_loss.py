import time
import sys
sys.path.append("..")
import database.database as db
from api.bybit_api import Bybit_Api
from model.orders import Orders
from model.calc import Calc

class Stop_Loss():

    # def __init__(self):

    api = Bybit_Api()
    orders = Orders()
    calc = Calc()

    def changeStopLoss(self, slAmount):
        self.api.changeStopLoss(slAmount)
        print("")
        print("Changed stop Loss to: " + str(slAmount))

    def updateStopLoss(self):
        flag = True

        while (flag == True):
            if(self.activePositionCheck() == 1):
                if (comms.viewData("vwap", "1min") != "null"):
                    self.closePositionMarket()
                else:
                    if(side == "Buy"):
                        if(self.api.lastPrice(self) > level):
                            self.calc.calculateStopLoss()
                            time.sleep(4)
                        else:
                            print("Waiting...")
                            print("Percent Gained: " +
                                  str(self.calc.calculatePercentGained()))
                            print("Level: " + str(level))
                            print("BTC Price: " + str(self.api.lastPrice(self)))
                            print("")
                            time.sleep(4)
                    else:
                        if(self.api.lastPrice(self) < level):
                            self.calc.calculateStopLoss()
                            time.sleep(4)
                        else:
                            print("Waiting...")
                            print("Percent Gained: " +
                                  str(self.calc.calculatePercentGained()))
                            print("Level: " + str(level))
                            print("BTC Price: " + str(self.api.lastPrice(self)))
                            print("")
                            time.sleep(4)
            else:
                print("Position Closed")
                print("")
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
                stop_loss = (entry_price - self.calc.calculateOnePercentLessEntry())
            else:
                stop_loss = (entry_price + self.calc.calculateOnePercentLessEntry())
            percentLevel = 0.25
        elif (percentGained >= 0.25) and (percentLevel >= 0.25) and (percentLevel < 0.5):
            stop_loss = entry_price
            percentLevel = 0.5
            level = self.api.lastPrice(self)
        elif (percentGained >= 0.5) and (percentLevel < 0.75):
            stop_loss = level
            percentLevel = 0.75
            level = self.api.lastPrice(self)
        elif (percentGained >= 0.75) and (percentLevel < 1.0):
            stop_loss = level
            percentLevel = 1.0
            level = self.api.lastPrice(self)
        elif (percentGained > (percentLevel + 0.5)):
            stop_loss = level
            percentLevel += 0.5
            level = self.api.lastPrice(self)

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

