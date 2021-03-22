import sys
sys.path.append("..")
# import asyncio
from model.orders import Orders
from model.stop_loss import Stop_Loss
from model.calc import Calc
from api.bybit_api import Bybit_Api
import controller.comms as comms
import database.database as db
import time

class Strategy():

    orders = Orders()
    sl = Stop_Loss()
    calc = Calc()
    api = Bybit_Api()

    def __init__(self, vwapMarginNegInput, vwapMarginPosInput, dataNameInput):
        global vwapMarginNeg
        global vwapMarginPos
        global data_name
        global lastVwap
        global currentVwap
        global lastTrend

        vwapMarginNeg = vwapMarginNegInput
        vwapMarginPos = vwapMarginPosInput
        data_name = dataNameInput
        lastVwap = 0.0
        currentVwap = 0.0
        lastTrend = ""
        lastCandleWt1 = 0.0
        lastCandleWt2 = 0.0

    #single
    def determineVwapTrend(self):
        global lastVwap
        global currentVwap
        global vwapTrend
        global lastTrend

        newTrend = ""
        
        lastCandleVwap = comms.viewData(data_name, 'last_candle_vwap')


        if (lastCandleVwap != currentVwap):
            lastVwap = currentVwap
            print("")
            print("lastVwap: " + str(lastVwap))
            currentVwap = lastCandleVwap
            print("current vwap: " + str(currentVwap))

            if(currentVwap >= vwapMarginPos) and (lastVwap <= vwapMarginPos):
                newTrend = 'cross_up'
            elif(currentVwap <= vwapMarginNeg) and (lastVwap >= vwapMarginNeg):
                newTrend = 'cross_down'
            elif(currentVwap > 0) and (lastVwap > 0):
                newTrend = 'positive_vwap'
            elif(currentVwap < 0) and (lastVwap < 0):
                newTrend = 'negative_vwap'
            else:
                newTrend = 'not_enough_information'
            
            if (newTrend == 'cross_up') or (newTrend == 'cross_down'):
                comms.updateData(data_name, 'active_position', 'change')
                if ((lastTrend == 'cross_up') and (newTrend == 'cross_down')) or ((lastTrend == 'cross_down') and (newTrend == 'cross_up')):
                    comms.updateData(data_name, 'new_trend', newTrend)

            print("lastTrend: " + str(lastTrend))
            print("newTrend: " + str(newTrend))
            comms.updateData(data_name, 'new_trend', newTrend)
            lastTrend = comms.viewData(data_name, 'new_trend')
            comms.updateData(data_name, 'last_trend', lastTrend)
            
    def vwapCrossStrategy(self):
        initial_stop_loss = 0
        self.determineVwapTrend()
        newTrend = comms.viewData(data_name, 'new_trend')
        comms.updateData(data_name, 'new_trend', 'null')
        lastCandleWt1 = comms.viewData(data_name, 'wt1')
        lastCandleWt2 = comms.viewData(data_name, 'wt2')

        if (newTrend == 'cross_up') or (newTrend == 'cross_down'):
            if (self.orders.activePositionCheck() == 1):
                print("closing active Position")
                self.orders.closePositionMarket()
                comms.logClosingDetails()

            if ((newTrend == 'cross_up') and (lastCandleWt1 > 0) and (lastCandleWt2 > 0)) or (newTrend == 'cross_down') and (lastCandleWt1 < 0) and (lastCandleWt2 < 0):
                if (newTrend == 'cross_up'):
                    print("Opening new Long:")
                    self.orders.createOrder(side='Buy', order_type='Market', inputQuantity=db.getInputQuantity())

                elif (newTrend == 'cross_down'):
                    print("Opening new Short:")
                    self.orders.createOrder(side='Sell', order_type='Market', inputQuantity=db.getInputQuantity())

                #process Stop Loss:
                print("Checking for stop loss...")
                flag = True
                counter = 0
                tempTime = 60

                while (flag == True):
                    counter += 1

                    #display counter
                    if (counter == tempTime):
                        counter = 0
                        print("Waiting - Update SL")
                        print("Percent Gained: " + str(self.calc.calcPercentGained()))
                        print("")

                    elif(counter == tempTime/6):
                            print("Percent Gained: " +
                                        str(self.calc.calcPercentGained()))
                            print("Last Price: " + str(self.api.lastPrice()))

                    elif(comms.viewData(db.getDataName(), 'active_position') == 'change'):
                        flag = False

                    #process SL if position is active
                    else:
                        if(self.orders.activePositionCheck() == 1):
                            self.sl.updateStopLoss('candles')
                            time.sleep(1)
                        else:
                            print("Position Closed")
                            print("")
                            comms.logClosingDetails()
                            flag = False

            comms.updateData(data_name, 'active_position', 'null')
                  


#check for order of lastTrend verse newTrend