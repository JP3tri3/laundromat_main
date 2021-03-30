import time
import sys
sys.path.append("..")
from database.database import Database as db
from api.bybit_api import Bybit_Api as api
from model.calc import Calc
import controller.comms as comms


class Stop_Loss:

    percent_level = 0
    level = 0
    stop_loss = 0

    def __init__(self):

        self.calc = Calc()

    def change_stop_loss(self, sl_amount):
        api().change_stop_loss(sl_amount)
        print("")
        print("Changed stop Loss to: " + str(sl_amount))

    def update_stop_loss(self, slStrat):
        side = api().get_position_side()
        print("Level: " + str(level))
        if(side == 'Buy'):
            if(api().last_price() > level):
                self.calculate_stop_loss(sl_strategy=slStrat)

        elif(side == 'Sell'):
            if(level == 0) or (api().last_price() < level):
                self.calculate_stop_loss(sl_strategy=slStrat)

    def calculate_stop_loss(self, sl_strategy):
        global level
        global percent_level
        global percent_gained_lock
        global stop_loss
        side = api().get_position_side()
        percent_gained = self.calc.calc_percent_gained()

        if (sl_strategy == 'raise_percentage'):

            pre_percent_level = percent_level
            one_percent_less_entry = self.calc.calc_one_percent_less_entry()
            entry_price = api().get_active_position_entry_price()

            print("calculating Stop Loss:")
            print("Level before calc: " + str(level))
            print("")
            if (percent_level < 0.25):
                stop_loss = (entry_price - one_percent_less_entry) if (side == 'Buy') \
                    else (entry_price + one_percent_less_entry)
                percent_level = 0.25
            elif (percent_gained >= 0.25) and (percent_level >= 0.25) and (percent_level < 0.5):
                stop_loss = entry_price
                percent_level = 0.5
                level = api().last_price(self)
            elif (percent_gained >= 0.5) and (percent_level < 0.75):
                stop_loss = level
                percent_level = 0.75
                level = api().last_price(self)
            elif (percent_gained >= 0.75) and (percent_level < 1.0):
                stop_loss = level
                percent_level = 1.0
                level = api().last_price(self)
            elif (percent_gained > (percent_level + 0.5)):
                stop_loss = level
                percent_level += 0.5
                level = api().last_price(self)

            if (pre_percent_level != percent_level):
                db().set_level(level_input=level)
                print("Changing Stop Loss")
                total_percent_gained = percent_gained
                db().set_exit_price(stop_loss)
                db().set_total_percent_gained(total_percent_gained)
                self.change_stop_loss(stop_loss)
                db().set_stop_loss(stop_loss)
                print("Percent Gained: " + str(total_percent_gained))
                print("Percent Level: " + str(percent_level))
                print("Level: " + str(round(level, 2)))
                print("Stop Loss: " + str(stop_loss))
                print("")
                pre_percent_level = percent_level

        elif (sl_strategy == 'candles'):
            last_candle_high = comms.view_data(db().get_data_name(), 'last_candle_high')
            last_candle_low = comms.view_data(db().get_data_name(), 'last_candle_low')

            if (side == 'Buy'):
                stop_loss = last_candle_low - (2.0 * self.calc.calc_one_percent_less_entry())
                print("level: " + str(level))
                print("stop_loss: " + str(stop_loss))
                print("")
                if (level < stop_loss):
                    level = stop_loss
                    self.change_stop_loss(stop_loss)
                    db().set_stop_loss(stop_loss)
                    db().set_total_percent_gained(percent_gained)

            elif (side == 'Sell'):
                stop_loss = last_candle_high + (2.0 * self.calc.calc_one_percent_less_entry())
                print("level: " + str(level))
                print("stop_loss: " + str(stop_loss))
                print("")
                if (level == 0) or (level > stop_loss):                
                    level = stop_loss    
                    self.change_stop_loss(stop_loss)
                    #TO DO
                    db().set_stop_loss(stop_loss)
                    db().set_total_percent_gained(percent_gained)

        else:
            print('invalid strategy')

