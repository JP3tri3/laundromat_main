import sys
sys.path.append("..")
import config
from api.bybit_api import Bybit_Api
import controller.comms as comms
from logic.strategy import Strategy
from logic.calc import Calc as calc
import database.sql_connector as conn
from database.database import Database as db
from time import time, sleep
import asyncio

# #TEST
# from logic.trade_logic import Trade_Logic
# from logic.stop_loss import Stop_Loss

api_key = config.BYBIT_TESTNET_API_KEY
api_secret = config.BYBIT_TESTNET_API_SECRET
leverage = 5
active = False
symbol_pair = 'BTCUSD'
input_quantity = 500
strat_id = '1_min'
trade_id = 'bybit_auto_1'
vwap_margin_neg = -7
vwap_margin_pos = 7

def get_active():
    return active

def get_trade_id():
    return trade_id

def get_strat_id():
    return strat_id

async def main():

    db().clear_all_tables_values()
    db().delete_trade_records(True)

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

    # #TEST
    # tl = Trade_Logic(api_key, api_secret, symbol, symbol_pair, key_input, leverage, limit_price_difference)
    # sl = Stop_Loss()

    api.set_leverage(leverage)

    #input true to clear:
    comms.clear_json(True)

    #initiate strategy:
    strat.vwap_cross_strategy()
                    



loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
