import sys
sys.path.append("..")
from database import config
from api.bybit_api import Bybit_Api
import controller.comms as comms
from logic.strategy import Strategy
from logic.calc import Calc as calc
import database.sql_connector as conn
from database.database import Database as db
from time import time, sleep
import asyncio

api_key = config.BYBIT_TESTNET_API_KEY_auto_2
api_secret = config.BYBIT_TESTNET_API_SECRET_auto_2
leverage = 3
symbol_pair = 'BTCUSD'
input_quantity = 500
strat_id = '9_min'
trade_id = 'bybit_auto_2'
vwap_margin_neg = -9
vwap_margin_pos = 9

async def main():

    if (symbol_pair == "BTCUSD"):
        symbol = 'BTC'
        key_input = 0
        limit_price_difference = 0.50
        db().update_trade_values(trade_id, strat_id, symbol, symbol_pair,  key_input, limit_price_difference, leverage, input_quantity, 'empty', 0, 0, 0)
    elif (symbol_pair == "ETHUSD"):
        symbol = 'ETH'
        key_input = 1
        limit_price_difference = 0.05
        db().update_trade_values(trade_id, strat_id, symbol, symbol_pair, key_input, limit_price_difference, leverage, input_quantity, 'empty', 0, 0, 0)
    else:
        print("Invalid Symbol Pair")

    strat = Strategy(api_key, api_secret, trade_id, strat_id, symbol, symbol_pair, key_input, input_quantity, leverage, limit_price_difference, vwap_margin_neg, vwap_margin_pos)
    api = Bybit_Api(api_key, api_secret, symbol, symbol_pair, key_input)

    api.set_leverage(leverage)


    #initiate strategy:
    strat.vwap_cross_strategy()
                    



loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
