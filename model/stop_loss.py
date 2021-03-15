import time
import sys
sys.path.append("..")
import database.database as db
from api.bybit_api import Bybit_Api
from model.calc import Calc
from model.orders import Orders

percent_level = 0
level = 0

class Stop_Loss():

    # def __init__(self):
    #     retrun

    api = Bybit_Api()
    calc = Calc()
    orders = Orders()

    def changeStopLoss(self, slAmount):
        self.api.changeStopLoss(slAmount)
        print("")
        print("Changed stop Loss to: " + str(slAmount))

    def updateStopLoss(self):
        flag = True
        level = self.api.getActivePositionEntryPrice()
        side = self.api.getPositionSide()

        while (flag == True):
            if(self.orders.activePositionCheck() == 1):
                if(side == "Buy"):
                    if(self.api.lastPrice() > level):
                        self.calculateStopLoss()
                        level = db.getLevel()
                        time.sleep(4)
                    else:
                        print("Waiting...")
                        print("Percent Gained: " +
                            str(self.calc.calcPercentGained()))
                        print("Level: " + str(level))
                        print("BTC Price: " + str(self.api.lastPrice()))
                        print("")
                        time.sleep(4)
                else:
                    if(self.api.lastPrice() < level):
                        self.calculateStopLoss()
                        level = db.getLevel()
                        time.sleep(4)
                    else:
                        print("Waiting...")
                        print("Percent Gained: " +
                            str(self.calc.calcPercentGained()))
                        print("Level: " + str(level))
                        print("Price: " + str(self.api.lastPrice()))
                        print("")
                        time.sleep(4)
            else:
                print("Position Closed")
                print("")
                flag = False


    def calculateStopLoss(self):
        global level
        global percent_level
        global percent_gained_lock
        level = db.getLevel()
        pre_percent_level = percent_level
        percentGained = self.calc.calcPercentGained()

        print("calculating Stop Loss:")
        print("Level before calc: " + str(level))
        if (percent_level < 0.25):
            if (side == "Buy"):
                stop_loss = (entry_price - self.calc.calculateOnePercentLessEntry())
            else:
                stop_loss = (entry_price + self.calc.calculateOnePercentLessEntry())
            percent_level = 0.25
        elif (percentGained >= 0.25) and (percentLevel >= 0.25) and (percentLevel < 0.5):
            stop_loss = entry_price
            percent_level = 0.5
            level = self.api.lastPrice(self)
        elif (percentGained >= 0.5) and (percentLevel < 0.75):
            stop_loss = level
            percent_level = 0.75
            level = self.api.lastPrice(self)
        elif (percentGained >= 0.75) and (percentLevel < 1.0):
            stop_loss = level
            percent_level = 1.0
            level = self.api.lastPrice(self)
        elif (percentGained > (percentLevel + 0.5)):
            stop_loss = level
            percent_level += 0.5
            level = self.api.lastPrice(self)

        if (pre_percent_level != percent_level):
            db.setLevel(level=level)
            db.setPercentLevel(percent_level)
            print("Changing Stop Loss")
            total_percent_gained = percentGained
            db.setTotalPercentGain(total_percent_gained)
            self.changeStopLoss(stop_loss)
            print("Percent Gained: " + str(percentGainedLock))
            print("Percent Level: " + str(percent_level))
            print("Level: " + str(level))
            print("Stop Loss: " + str(stop_loss))
            print("")
            pre_percent_level = percent_level

