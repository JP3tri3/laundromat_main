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

    api = Bybit_Api()
    calc = Calc()
    orders = Orders()

    def changeStopLoss(self, slAmount):
        self.api.changeStopLoss(slAmount)
        print("")
        print("Changed stop Loss to: " + str(slAmount))

    def updateStopLoss(self, slStrat):
        level = self.api.getActivePositionEntryPrice()
        side = self.api.getPositionSide()
        
        if(side == 'Buy'):
            if(self.api.lastPrice() > level):
                self.calculateStopLoss(slStrategy=slStrat)

        elif(side == 'Sell'):
            if(self.api.lastPrice() < level):
                self.calculateStopLoss(slStrategy=slStrat)

    def calculateStopLoss(self, slStrategy):
        global level
        global percent_level
        global percent_gained_lock
        global stop_loss
        side = self.api.getPositionSide()
        percentGained = self.calc.calcPercentGained()

        if (slStrategy == 'raise_percentage'):

            pre_percent_level = percent_level
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
                db.setStopLoss(stop_loss)
                print("Percent Gained: " + str(total_percent_gained))
                print("Percent Level: " + str(percent_level))
                print("Level: " + str(round(level, 2)))
                print("Stop Loss: " + str(stop_loss))
                print("")
                pre_percent_level = percent_level

        elif (slStrategy == 'candles'):
            lastCandleHigh = comms.viewData(db.getDataName(), 'last_candle_high')
            lastCandleLow = comms.viewData(db.getDataName(), 'last_candle_low')

            stop_loss = lastCandleLow - (2.0 * self.calc.calcOnePercent()) if(side == 'Buy') \
                else lastCandleHigh + (2.0 * self.calc.calcOnePercent())

            if(level != stop_loss):
                level = stop_loss    
                self.changeStopLoss(stop_loss)
                db.setStopLoss(stop_loss)
                db.setTotalPercentGain(percentGained)
                print("level: " + str(level))
                print("stop_loss: " + str(stop_loss))

        else:
            print('invalid strategy')

