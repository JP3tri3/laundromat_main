
import sys
sys.path.append("..")
from database.database import Database as db
import datetime

class Trade:

    def __init__(self, trade_id):
        self.trade_id = trade_id



    def commit_trade_record(self, coin_gain, dollar_gain, entry_price, exit_price):

        kv_dict = db().get_trade_values(self.trade_id)

        trade_record_id = kv_dict['trade_record_id']
        strat_id = kv_dict['strat_id']
        symbol = kv_dict['symbol']
        symbol_pair = kv_dict['symbol_pair']
        input_quantity = kv.dict['input_quantity']
        side = kv_dict['side']
        stop_loss = kv_dict['stop_loss']
        percent_gain = ['percent_gain']

        if (self.trade_record_id > 0):
            previous_dollar_total = db().get_trade_record_total_dollar_gain(self.trade_record_id)
            previous_coin_total = db().get_trade_record_total_coin_gain(self.trade_record_id)
            total_p_l_dollar = previous_dollar_total + dollar_gain
            total_p_l_coin = previous_coin_total + coin_gain
        else:
            total_p_l_dollar = dollar_gain
            total_p_l_coin = coin_gain

        trade_record_id += 1

        db().create_trade_record(trade_record_id, self.trade_id, strat_id, symbol_pair, side, \
            input_quantity, entry_price, exit_price, stop_loss, percent_gain, dollar_gain, \
                coin_gain, total_p_l_dollar, total_p_l_coin)








