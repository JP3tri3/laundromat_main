import sys
sys.path.append("..")
import controller.comms as comms
import database.database as db
from model.orders import Orders
from model.stop_loss import Stop_Loss
from api.bybit_api import Bybit_Api
import config
import strategy
from time import time, sleep
import datetime

import asyncio

async def main():

    margin = 3
    symbolPair = 'BTCUSD'
    inputQuantity = 500

    orders = Orders()
    sl = Stop_Loss()
    api = Bybit_Api()

#input true to clear
    comms.clearDisplay(True)
    comms.clearLogs(True)

    db.setInitialValues('BTC', symbolPair, margin, 0, 0.50, inputQuantity)

    flag = True
    temp = 0
    tempCondition = 60

    while(flag == True):
        strategy.vwapStrategy1Min()
        sleep(1)
        temp += 1
        if (temp == tempCondition):
            print("waiting on input...")
            comms.timeStamp()
            temp = 0

    


        



loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
