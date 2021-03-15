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

    margin = 5
    symbolPair = 'BTCUSD'
    inputQuantity = 500

    # flag = True
    # temp = 0
    # tempCondition = 30

    # while(flag == True):

    #     strategy.checkInputs()

    #     strategy.initiateMarketTradeVwap()
    #     time.sleep(1)
    #     temp += 1
    #     if (temp == tempCondition):
    #         print("waiting on input...")
    #         comms.timeStamp()
    #         temp = 0


    db.setInitialValues('BTC', symbolPair, margin, 0, 0.50, inputQuantity)
    orders = Orders()
    sl = Stop_Loss()
    api = Bybit_Api()

    print("Placing Orders")
    orders.createOrder(side='Buy', order_type='Market', stop_loss=api.lastPrice() - 200, inputQuantity=inputQuantity)
    print("Updating Stop Loss")
    sl.updateStopLoss()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
