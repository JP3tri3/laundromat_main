import sys
sys.path.append("..")
# import controller.comms as comms
# from model.orders import Orders
# from model.stop_loss import Stop_Loss
# from api.bybit_api import Bybit_Api
# from strategy import Strategy
from time import time, sleep
import datetime

import asyncio

leverage = 5
symbol_pair = 'BTCUSD'
input_quantity = 500
strat_id = '1_min'
trade_id = 'bybit_auto_1'
vwap_margin_neg = -10.5
vwap_margin_pos = 10.5

def get_trade_id():
    return trade_id

def get_strat_id():
    return strat_id

# async def main():

#     if (symbol_pair == "BTCUSD"):
#         conn.updateTradeValues(trade_id, 'BTC', symbol_pair, 0, 0.50, 5, input_quantity, strat_id)
#     elif (symbol_pair == "ETHUSD"):
#         conn.updateTradeValues(trade_id, 'ETH', symbol_pair, 1, 0.05, 5, input_quantity, strat_id)
#     else:
#         print("Invalid Symbol Pair")

#     strat = Strategy(vwap_margin_neg, vwap_margin_pos)
#     api = Bybit_Api()
#     order = Orders()

#     api.setLeverage()

#     #input true to clear
#     comms.clearJson(True, data_name)
#     comms.clearLogs(True)

#     flag = True
#     temp = 0
#     tempCondition = 60

#     while(flag == True):
#         sleep(1)
#         temp += 1
#         if (temp == tempCondition):
#             print("waiting on input...")
#             comms.timeStamp()
#             temp = 0
#         strat.vwapCrossStrategy()
#     order.activePositionCheck()    



# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# loop.close()
