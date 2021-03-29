import sys
sys.path.append("..")
import auto
import database.sql_connector as conn

class Database:

    def __init__ (self):
        self.trade_id = auto.get_trade_id()
        self.strat_id = auto.get_strat_id()
        self.trade_record_id = 0

        print("DATABASE INITIALIZED")


    # # trades table:

    def get_symbol(self):
        return conn.viewDbValue('trades', self.trade_id, 'symbol')

    def get_key_input(self):
        return conn.viewDbValue('trades', self.trade_id, 'key_input')

    def get_symbol_pair(self):
        return conn.viewDbValue('trades', self.trade_id, 'symbol_pair')

    def get_limit_price_difference(self):
        return conn.viewDbValue('trades', self.trade_id, 'limit_price_difference')

    def set_side(self):
        return conn.viewDbValue('trades', self.trade_id, 'limit_price_difference')

    def get_side(self, trade_record_id):
        return conn.viewDbValue('trade_records', trade_record_id, 'side')

    def get_input_quantity(self):
        return conn.viewDbValue('trades', self.trade_id, 'input_quantity')

    def set_input_quantity(self, data_input):
        conn.updateTableValue('trades', self.trade_id, 'input_quantity', data_input)

    def get_leverage(self):
        return conn.viewDbValue('trades', self.trade_id, 'leverage')


    # # strategy table:

    def get_wt1(self):
        return conn.viewDbValue('strategy', self.strat_id, 'wt1')    

    def get_wt2(self):
        return conn.viewDbValue('strategy', self.strat_id, 'wt2')       

    def get_last_candle_vwap(self):
        return conn.viewDbValue('strategy', self.strat_id, 'last_candle_vwap')       

    def get_last_candle_low(self):
        return conn.viewDbValue('strategy', self.strat_id, 'last_candle_low')  

    def get_last_candle_high(self):
        return conn.viewDbValue('strategy', self.strat_id, 'last_candle_high')  

    def get_active_position(self):
        return conn.viewDbValue('strategy', self.strat_id, 'active_position')  

    def set_active_position(self, data_input):
        return conn.updateTableValue('strategy', self.strat_id, 'active_position', data_input)  

    def get_new_trend(self):
        return conn.viewDbValue('strategy', self.strat_id, 'new_trend')  

    def set_new_trend(self, data_input):
        return conn.updateTableValue('strategy', self.strat_id, 'new_trend', data_input)  

    def get_last_trend(self):
        return conn.viewDbValue('strategy', self.strat_id, 'last_trend')  

    def set_last_trend(self, data_input):
        return conn.updateTableValue('strategy', self.strat_id, 'last_trend', data_input)  

    def get_active_trend(self):
        return conn.viewDbValue('strategy', self.strat_id, 'active_trend')  

    def set_active_trend(self, data_input):
        return conn.updateTableValue('strategy', self.strat_id, 'active_trend', data_input)  

    # # trade_records table:

    def create_trade_record(self, trade_record_id_input, side):
        self.trade_record_id = trade_record_id_input
        return conn.create_trade_record(trade_record_id_input, self.symbol_pair, 0, 0, 0, 0, 0, 0, 0, side, 0)

    def set_entry_price(self, entry_price_input):
        return conn.updateTableValue('trade_records', self.trade_record_id, 'entry_price', entry_price_input)

    def get_entry_price(self):
        return conn.viewDbValue('trade_records', self.trade_record_id, 'entry_price')


    # # table dictionaries

    def get_trade_values(self):
        return conn.get_table_pair('trades', self.trade_id)

    def get_strat_values(self):
        return conn.get_table_pair('strategy', self.strat_id)





    # def setLevel(self):
    #     global level
    #     level = levelInput

    # def getLevel(self):
    #     return level

    # def setEntryPrice(self):
    #     global entry_price
    #     entry_price = entryPriceInput

    # def getEntryPrice(self):
    #     return entry_price

    # def setStopLoss(self):
    #     global stop_loss
    #     stop_loss = stopLossInput

    # def getStopLoss(self):
    #     return stop_loss

    # def setExitPrice(self):
    #     global exit_price
    #     exit_price = exitPriceInput

    # def getExitPrice(self):
    #     return exit_price

    # def setTotalPercentGain(self):
    #     global total_percent_gained
    #     total_percent_gained = totalPercentGainInput

    # def getTotalPercentGain(self):
    #     return total_percent_gained

    # def setLeverage(self):
    #     global leverage
    #     leverage = leverageInput

