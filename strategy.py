import sys
sys.path.append("..")
# import asyncio
from model.orders import Orders
from model.stop_loss import Stop_Loss
import controller.comms as comms
import database.database as db


vwap1min = ""
lastVwap = 0
currentVwap = 0
lastTrend = ""


orders = Orders()
sl = Stop_Loss()
def getvWap():
    return vwap1min

def checkInputs():
    global vwap1min

    vwap1min = comms.viewData('vwap', '1min')
    return vwap1min

def determineVwapTrend():
    global lastVwap
    global currentVwap
    global vwapTrend
    global lastTrend
    newTrend = ""

    lastCandleVwap = comms.viewData('1_min', 'last_candle_vwap')

    if (lastCandleVwap != currentVwap):
        lastVwap = currentVwap
        print("")
        print("lastVwap: " + str(lastVwap))
        currentVwap = lastCandleVwap
        print("current vwap: " + str(currentVwap))

        if(currentVwap > 0) and (lastVwap < 0):
            newTrend = 'cross_up'
        elif(currentVwap < 0) and (lastVwap > 0):
            newTrend = 'cross_down'
        elif(currentVwap > 0) and (lastVwap > 0):
            newTrend = 'positive_vwap'
        elif(currentVwap < 0) and (lastVwap < 0):
            newTrend = 'negative_vwap'
        else:
            newTrend = 'not_enough_information'
        
        if (newTrend == 'cross_up') or (newTrend == 'cross_down'):
            comms.updateData('notice', 'active_position', 'change')
            if ((lastTrend == 'cross_up') and (newTrend == 'cross_down')) or ((lastTrend == 'cross_down') and (newTrend == 'cross_up')):
                comms.updateData('notice', 'new_trend', newTrend)

        print("lastTrend: " + str(lastTrend))
        print("newTrend: " + str(newTrend))
        comms.updateData('notice', 'new_trend', newTrend)
        lastTrend = comms.viewData('notice', 'new_trend')
        comms.updateData('notice', 'last_trend', lastTrend)
        
def vwapStrategy1Min():
    determineVwapTrend()
    newTrend = comms.viewData('notice', 'new_trend')
    comms.updateData('notice', 'new_trend', 'null')

    if (newTrend == 'cross_up'):
        if (orders.activePositionCheck() == 1):
            print("closing active Position")
            orders.closePositionMarket()
            comms.logClosingDetails()
        comms.updateData('notice', 'active_position', 'null')    
        orders.createOrder(side='Buy', order_type='Market', stop_loss=100, inputQuantity=db.getInputQuantity())
        print("updating stop loss...")
        sl.updateStopLoss('candles')

    elif (newTrend == 'cross_down'):
        if (orders.activePositionCheck() == 1):
            print("closing active Position")
            orders.closePositionMarket()
        comms.updateData('notice', 'active_position', 'null')
        orders.createOrder(side='Sell', order_type='Market', stop_loss=100, inputQuantity=db.getInputQuantity())
        print("updating stop loss...")
        sl.updateStopLoss('candles')

    