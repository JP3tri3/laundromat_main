import sys
sys.path.append("..")
# import asyncio
from model.orders import Orders
from model.stop_loss import Stop_Loss
import controller.comms as comms
import database.database as db



class Strategy():

    def __init__(self, vwapMarginNegInput, vwapMarginPosInput, dataNameInput):
        global vwapMarginNeg
        global vwapMarginPos
        global data_name
        global lastVwap
        global currentVwap
        global lastTrend
        global orders
        global sl

        vwapMarginNeg = vwapMarginNegInput
        vwapMarginPos = vwapMarginPosInput
        data_name = dataNameInput
        lastVwap = 0
        currentVwap = 0
        lastTrend = ""

        orders = Orders()
        sl = Stop_Loss()

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
        self.determineVwapTrend()
        newTrend = comms.viewData(data_name, 'new_trend')
        comms.updateData(data_name, 'new_trend', 'null')

        if (newTrend == 'cross_up'):
            if (orders.activePositionCheck() == 1):
                print("closing active Position")
                orders.closePositionMarket()
                comms.logClosingDetails()
            comms.updateData(data_name, 'active_position', 'null')    
            orders.createOrder(side='Buy', order_type='Market', inputQuantity=db.getInputQuantity())
            # print("updating stop loss...")
            # sl.updateStopLoss('candles')
            return 1

        elif (newTrend == 'cross_down'):
            if (orders.activePositionCheck() == 1):
                print("closing active Position")
                orders.closePositionMarket()
            comms.updateData(data_name, 'active_position', 'null')
            orders.createOrder(side='Sell', order_type='Market', inputQuantity=db.getInputQuantity())
            # print("updating stop loss...")
            # sl.updateStopLoss('candles')
            return 1
        
        else:
            return 0


#multiple TFs

