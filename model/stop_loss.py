import sys
sys.path.append("..")
import database.database as db
from api.bybit_api import Bybit_Api

class Stop_Loss():

    def __init__(self, inputSymbolPair):
        global symbolPair

        symbolPair = inputSymbolPair

    api = Bybit_Api(symbolPair)

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