import sys
sys.path.append("..")
import controller.comms as comms
from model.orders import Orders
# from model.stop_loss import Stop_Loss
from api.bybit_api import Bybit_Api
from strategy import Strategy
import database.sql_connector as conn
from time import time, sleep
import datetime

import asyncio

leverage = 5
active = False
symbol_pair = 'BTCUSD'
input_quantity = 500
strat_id = '1_min'
trade_id = 'bybit_auto_1'
vwap_margin_neg = -10.5
vwap_margin_pos = 10.5

def get_active():
    return active

def get_trade_id():
    return trade_id

def get_strat_id():
    return strat_id

async def main():

    if (symbol_pair == "BTCUSD"):
        conn.updateTradeValues(trade_id, strat_id, 'BTC', 'BTCUSD',  0, 0.50, leverage, input_quantity, 'empty', 0, 0, 0)
    elif (symbol_pair == "ETHUSD"):
        conn.updateTradeValues(trade_id, strat_id,'ETH', 'ETHUSD', 1, 0.05, leverage, input_quantity, 'empty', 0, 0, 0)
    else:
        print("Invalid Symbol Pair")

    strat = Strategy(vwap_margin_neg, vwap_margin_pos)
    order = Orders()
    api = Bybit_Api()

    api.set_leverage()

    #input true to clear
    comms.clear_json(True)
    comms.clear_logs(True)

    flag = True
    temp = 0
    tempCondition = 60

    while(flag == True):
        sleep(1)
        temp += 1
        if (temp == tempCondition):
            print("waiting on input...")
            comms.time_stamp()
            temp = 0
        strat.vwap_cross_strategy()
    order.active_position_check()    



loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
