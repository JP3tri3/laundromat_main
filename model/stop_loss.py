import time
import sys
sys.path.append("..")
import database.database as db
from api.bybit_api import Bybit_Api
from model.calc import Calc
from model.orders import Orders
import controller.comms as comms

percent_level = 0
level = 0
stop_loss = 0

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

    def updateStopLoss(self, slStrat):
        flag = True
        level = self.api.getActivePositionEntryPrice()
        side = self.api.getPositionSide()

        while (flag == True):
            if(comms.viewData('notice', 'active_position') == 'change'):
                flag = False
            else:
                if(self.orders.activePositionCheck() == 1):
                    if(side == "Buy"):
                        if(self.api.lastPrice() > level):
                            self.calculateStopLoss(slStrategy=slStrat)
                            level = stop_loss
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
                            self.calculateStopLoss(slStrategy=slStrat)
                            level = stop_loss
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
            
        comms.logClosingDetails()


    def calculateStopLoss(self, slStrategy):
        global level
        global percent_level
        global percent_gained_lock
        global stop_loss
        side = self.api.getPositionSide()

        if (slStrategy == 'raise_percentage'):

            level = db.getLevel()
            pre_percent_level = percent_level
            percentGained = self.calc.calcPercentGained()
            onePercentLessEntry = self.calc.calcOnePercentLessEntry()
            entry_price = self.api.getActivePositionEntryPrice()

            print("calculating Stop Loss:")
            print("Level before calc: " + str(level))
            print("")
            if (percent_level < 0.25):
                stop_loss = (entry_price - onePercentLessEntry) if (side == 'Buy') \
                    else (entry_price + onePercentLessEntry)
                percent_level = 0.25
            elif (percentGained >= 0.25) and (percent_level >= 0.25) and (percentLevel < 0.5):
                stop_loss = entry_price
                percent_level = 0.5
                level = self.api.lastPrice(self)
            elif (percentGained >= 0.5) and (percent_level < 0.75):
                stop_loss = level
                percent_level = 0.75
                level = self.api.lastPrice(self)
            elif (percentGained >= 0.75) and (percent_level < 1.0):
                stop_loss = level
                percent_level = 1.0
                level = self.api.lastPrice(self)
            elif (percentGained > (percent_level + 0.5)):
                stop_loss = level
                percent_level += 0.5
                level = self.api.lastPrice(self)

            if (pre_percent_level != percent_level):
                db.setLevel(levelInput=level)
                print("Changing Stop Loss")
                total_percent_gained = percentGained
                db.setExitPrice(stop_loss)
                db.setTotalPercentGain(total_percent_gained)
                self.changeStopLoss(stop_loss)
                print("Percent Gained: " + str(total_percent_gained))
                print("Percent Level: " + str(percent_level))
                print("Level: " + str(round(level, 2)))
                print("Stop Loss: " + str(stop_loss))
                print("")
                pre_percent_level = percent_level

        elif (slStrategy == 'candles'):
            lastCandleHigh = comms.viewData('1_min', 'last_candle_high')
            lastCandleLow = comms.viewData('1_min', 'last_candle_low')

            if(side == 'Buy'):
                stop_loss = lastCandleLow - 20
            else:
                stop_loss = lastCandleHigh + 20

            if(level != stop_loss):
                level = stop_loss
                self.changeStopLoss(stop_loss)
                print("Stop Loss: " + str(stop_loss))

            


        else:
            print('invalid strategy')

