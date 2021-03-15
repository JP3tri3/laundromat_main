import sys
sys.path.append("..")
# import asyncio
from model.orders import Orders
import controller.comms as comms
import database.database as db


vwap1min = ""

# self.api = Bybit_Api()
orders = Orders()

def getvWap():
    return vwap1min

def checkInputs():
    global vwap1min

    vwap1min = comms.viewData('vwap', '1min')
    return vwap1min


def initiateMarketTradeVwap():
    
    db.setInitialValues('BTC', 'BTCUSD', 5, 0, 0.50)
    # global vwap1min
    if (vwap1min == "crossover"):
        comms.updateData("vwap", "1min", "null")
        orders.createOrder("Buy", "Limit", 100, 100)
    elif (vwap1min == "crossunder"):
        comms.updateData("vwap", "1min", "null")
        orders.createOrder("Sell", "Limit", 100, 100)

# add close order if vwap changes
