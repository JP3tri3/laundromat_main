import sys
sys.path.append("..")
# import auto
import database.sql_connector as conn

class Database:

    print("DATABASE INITIALIZED")

    # # trades table:

    def get_symbol(self, trade_id):
        return conn.viewDbValue('trades', trade_id, 'symbol')

    def get_key_input(self, trade_id):
        return conn.viewDbValue('trades', trade_id, 'key_input')

    def get_symbol_pair(self, trade_id):
        return conn.viewDbValue('trades', trade_id, 'symbol_pair')

    def get_limit_price_difference(self, trade_id):
        return conn.viewDbValue('trades', trade_id, 'limit_price_difference')

    def get_side(self, trade_id):
        return conn.viewDbValue('trades', trade_id, 'side')

    def set_side(self, trade_id, side):
        return conn.updateTableValue('trades', trade_id, 'side', side)

    def get_input_quantity(self, trade_id):
        return conn.viewDbValue('trades', trade_id, 'input_quantity')

    def set_input_quantity(self, trade_id, data_input):
        conn.updateTableValue('trades', trade_id, 'input_quantity', data_input)

    def get_leverage(self, trade_id):
        return conn.viewDbValue('trades', trade_id, 'leverage')

    def set_trade_record_id(self, trade_id, trade_record_id):
        conn.updateTableValue('trades', trade_id, 'trade_record_id', trade_record_id)

    # # strategy table:

    def update_strat_values(self, strat_id, wt1, wt2, last_candle_high, last_candle_low, last_candle_vwap):
        return conn.updateStratValues(strat_id, wt1, wt2, last_candle_high, last_candle_low, last_candle_vwap)

    def get_wt1(self, strat_id):
        return conn.viewDbValue('strategy', strat_id, 'wt1')    

    def get_wt2(self, strat_id):
        return conn.viewDbValue('strategy', strat_id, 'wt2')       

    def get_last_candle_vwap(self, strat_id):
        return conn.viewDbValue('strategy', strat_id, 'last_candle_vwap')       

    def get_last_candle_low(self, strat_id):
        return conn.viewDbValue('strategy', strat_id, 'last_candle_low')  

    def get_last_candle_high(self, strat_id):
        return conn.viewDbValue('strategy', strat_id, 'last_candle_high')  

    def get_active_position(self, strat_id):
        return conn.viewDbValue('strategy', strat_id, 'active_position')  

    def set_active_position(self, strat_id, data_input):
        return conn.updateTableValue('strategy', strat_id, 'active_position', data_input)  

    def get_new_trend(self, strat_id):
        return conn.viewDbValue('strategy', strat_id, 'new_trend')  

    def set_new_trend(self, strat_id, data_input):
        return conn.updateTableValue('strategy', strat_id, 'new_trend', data_input)  

    def get_last_trend(self, strat_id):
        return conn.viewDbValue('strategy', strat_id, 'last_trend')  

    def set_last_trend(self, strat_id, data_input):
        return conn.updateTableValue('strategy', strat_id, 'last_trend', data_input)  

    def get_active_trend(self, strat_id):
        return conn.viewDbValue('strategy', strat_id, 'active_trend')  

    def set_active_trend(self, strat_id, data_input):
        return conn.updateTableValue('strategy', strat_id, 'active_trend', data_input)  

    # # trade_records table:

    def create_trade_record(self, trade_record_id, symbol_pair, entry_price, exit_price, stop_loss, percent_gain, dollar_gain, coin_gain, number_of_trades, side, total_p_l, time):
        self.trade_record_id = trade_record_id_input
        return conn.create_trade_record(trade_record_id, symbol_pair, entry_price, exit_price, stop_loss, percent_gain, dollar_gain, coin_gain, number_of_trades, side, total_p_l, time)

    def set_entry_price(self, trade_record_id, entry_price_input):
        return conn.updateTableValue('trade_records', trade_record_id, 'entry_price', entry_price_input)

    def get_entry_price(self, trade_record_id):
        return conn.viewDbValue('trade_records', trade_record_id, 'entry_price')


    # # table dictionaries

    def get_trade_values(self, trade_id):
        return conn.get_table_pair('trades', trade_id)

    def get_strat_values(self, trade_id):
        return conn.get_table_pair('strategy', trade_id)

    def test1(self, trade_id):
        print(conn.get_table_pair('trades', trade_id))


    # def set_level(self):
    #     global level
    #     level = level_input

    # def getLevel(self):
    #     return level

    # def setEntryPrice(self):
    #     global entry_price
    #     entry_price = entryPriceInput

    # def getEntryPrice(self):
    #     return entry_price

    # def set_stop_loss(self):
    #     global stop_loss
    #     stop_loss = stopLossInput

    # def getStopLoss(self):
    #     return stop_loss

    # def set_exit_price(self):
    #     global exit_price
    #     exit_price = exit_priceInput

    # def getexit_price(self):
    #     return exit_price

    # def set_total_percent_gained(self):
    #     global total_percent_gained
    #     total_percent_gained = totalPercentGainInput

    # def getTotalPercentGain(self):
    #     return total_percent_gained

    # def set_leverage(self):
    #     global leverage
    #     leverage = leverageInput

