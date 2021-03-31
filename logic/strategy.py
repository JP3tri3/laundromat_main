import sys
sys.path.append("..")
# import asyncio
from model.orders import Orders
from model.stop_loss import Stop_Loss
from model.calc import Calc
import controller.comms as comms
from database.database import Database as db
import time

class Strategy:

    def __init__(self, api_key, api_secret, trade_id, strat_id, symbol, symbol_pair, input_quantity, leverage, limit_price_difference, vwap_margin_neg_input, vwap_margin_pos_input):
        self.trade_id = trade_id
        self.strat_id = strat_id
        self.vwap_margin_neg = vwap_margin_neg_input
        self.vwap_margin_pos = vwap_margin_pos_input
        self.last_vwap = 0.0
        self.current_vwap = 0.0
        self.last_trend = ""
        
        self.orders = Orders(api_key, api_secret, key_input, input_quantity, leverage, limit_price_difference)
        self.sl = Stop_Loss()
        self.calc = Calc()
    
    #single
    def determine_vwap_trend(self):
        global last_vwap
        global current_vwap
        global last_trend

        new_trend = ""
        strat_kv_dict = db().get_strat_values(trade_id)
        last_Candle_vwap = strat_kv_dict['last_candle_vwap']
        active_trend = strat_kv_dict['active_trend']
        

        if (last_Candle_vwap != self.current_vwap):
            self.last_vwap = self.current_vwap
            print("")
            print("last_vwap: " + str(self.last_vwap))
            self.current_vwap = last_Candle_vwap
            print("current vwap: " + str(self.current_vwap))

            if(self.current_vwap >= self.vwap_margin_pos) and (self.last_vwap <= self.vwap_margin_pos):
                new_trend = 'cross_up'
            elif(self.current_vwap <= self.vwap_margin_neg) and (self.last_vwap >= self.vwap_margin_neg):
                new_trend = 'cross_down'
            elif(self.current_vwap > 0) and (self.last_vwap > 0):
                new_trend = 'positive_vwap'
            elif(self.current_vwap < 0) and (self.last_vwap < 0):
                new_trend = 'negative_vwap'
            else:
                new_trend = 'not_enough_information'
            
            if (new_trend == 'cross_up') or (new_trend == 'cross_down'):
                if (active_trend != 'null') and (active_trend != new_trend):
                    db().set_active_position(strat_id, 'change')
                if ((self.last_trend == 'cross_up') and (new_trend == 'cross_down')) or ((self.last_trend == 'cross_down') and (new_trend == 'cross_up')):
                    db().set_new_trend(strat_id, new_trend)

            db().set_new_trend(strat_id, new_trend)
            self.last_trend = new_trend
            db().set_last_trend(strat_id, self.last_trend)

    def vwap_cross_strategy(self):
        print("In Strat")
        self.determine_vwap_trend()
        strat_kv_dict = db().get_strat_values(strat_id)
        new_trend = strat_kv_dict['new_trend']
        last_candle_wt1 = strat_kv_dict['wt1']
        last_candle_wt2 = strat_kv_dict['wt2']
        active_trend = strat_kv_dict['active_trend']

        if (new_trend != 'null') and (new_trend != active_trend):
            db().set_new_trend(strat_id, 'null')
            if (new_trend == 'cross_up') or (new_trend == 'cross_down'):
                if (self.orders.active_position_check() == 1):
                    print("cvwapCrossStrategy(self):losing active Position")
                    self.orders.close_position_market()
                    comms.log_closing_details()

                if ((new_trend == 'cross_up') and (last_candle_wt1 < 5) and (last_candle_wt2 < 5)) or (new_trend == 'cross_down') and (last_candle_wt1 > -5) and (last_candle_wt2 > -5):
                    if (new_trend == 'cross_up'):
                        print("Opening new Long:")
                        self.orders.create_order(side='Buy', order_type='Market', input_quantity=input_quantity)

                    elif (new_trend == 'cross_down'):
                        print("Opening new Short:")
                        self.orders.create_order(side='Sell', order_type='Market', input_quantity=input_quantity)

                    db().set_active_trend(strat_id, new_trend)
                    db().set_active_position(strat_id, 'null')
                    #process Stop Loss:
                    print("Checking for stop loss...")
                    flag = True
                    counter = 0
                    tempTime = 60

                    while (flag == True):
                        counter += 1
                        #display counter
                        if (counter == tempTime):
                            counter = 0
                            print("Waiting - Update SL")
                            print("")

                        elif(counter == tempTime/6):
                                print("Waiting")

                        elif(db().get_active_position(strat_id) == 'change'):
                            flag = False

                        #process SL if position is active
                        else:
                            if(self.orders.active_position_check() == 1):
                                self.sl.updateStopLoss('candles')
                                time.sleep(1)
                            else:
                                print("Position Closed")
                                print("")
                                db().set_active_trend('null')
                                comms.log_closing_details()
                                flag = False


#check for order of last_trend verse new_trend