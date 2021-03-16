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
activeTrend = ""


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
    global activeTrend
    trend = ""
    activeTrend = comms.viewData('notice', 'new_trend')

    lastCandleVwap = comms.viewData('1_min', 'last_candle_vwap')

    if (lastCandleVwap != currentVwap):
        lastVwap = currentVwap
        print("")
        print("lastVwap: " + str(lastVwap))
        currentVwap = lastCandleVwap
        print("urrent vwap: " + str(currentVwap))

        if(currentVwap > 0) and (lastVwap < 0):
            trend = 'cross_up'
        elif(currentVwap < 0) and (lastVwap > 0):
            trend = 'cross_down'
        elif(currentVwap > 0) and (lastVwap > 0):
            trend = 'positive_vwap'
        elif(currentVwap < 0) and (lastVwap < 0):
            trend = 'negative_vwap'
        else:
            trend = 'not_enough_information'
        
        if (activeTrend == 'cross_up') and (trend == 'cross_down'):
            comms.updateData('notice', 'active_position', 'change')
            comms.updateData('notice', 'active_trend', trend)

        elif (activeTrend == 'cross_down') and (trend == 'cross_up'):
            comms.updateData('notice', 'active_position', 'change')
            comms.updateData('notice', 'active_trend', trend)

        print("activeTrend: " + str(activeTrend))
        print("Trend: " + str(trend))
        comms.updateData('notice', 'new_trend', trend)

def vwapStrategy1Min():
    determineVwapTrend()
    trend = comms.viewData('notice', 'new_trend')

    if (trend == 'cross_up'):
        if (orders.activePositionCheck() == 1):
            print("closing active Position")
            orders.closePositionMarket()
            comms.logClosingDetails()
        comms.updateData('notice', 'active_position', 'null')      
        orders.createOrder(side='Buy', order_type='Market', stop_loss=100, inputQuantity=db.getInputQuantity())
        print("updating stop loss...")
        sl.updateStopLoss('candles')

    elif (trend == 'cross_down'):
        if (orders.activePositionCheck() == 1):
            print("closing active Position")
            orders.closePositionMarket()
        comms.updateData('notice', 'active_position', 'null')
        orders.createOrder(side='Sell', order_type='Market', stop_loss=100, inputQuantity=db.getInputQuantity())
        print("updating stop loss...")
        sl.updateStopLoss('candles')

    