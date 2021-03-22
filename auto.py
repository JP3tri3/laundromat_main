import sys
sys.path.append("..")
import controller.comms as comms
import database.database as db
from model.orders import Orders
from model.stop_loss import Stop_Loss
from api.bybit_api import Bybit_Api
import config
from strategy import Strategy
from time import time, sleep
import datetime

import asyncio

async def main():

    leverage = 5
    symbolPair = 'BTCUSD'
    inputQuantity = 500
    data_name = '1_min'
    vwapMarginNeg = -10.5
    vwapMarginPos = 10.5

    if (symbolPair == "BTCUSD"):
        db.setInitialValues('BTC', symbolPair, leverage, 0, 0.50, inputQuantity, data_name)
    elif (symbolPair == "ETHUSD"):
        db.setInitialValues('ETH', symbolPair, leverage, 1, 0.05, inputQuantity, data_name)



    orders = Orders()
    sl = Stop_Loss()
    api = Bybit_Api()
    strat = Strategy(vwapMarginNeg, vwapMarginPos, data_name)

    #input true to clear
    comms.clearJson(True, data_name)
    comms.clearLogs(True)

    flag = True
    temp = 0
    tempCondition = 60

    while(flag == True):
        sleep(1)
        temp += 1
        if (temp == tempCondition):
            print("waiting on input...")
            comms.timeStamp()
            temp = 0
        if(strat.vwapCrossStrategy() == 1):
            print("update SL")
        else:
            print(0)


        



loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
