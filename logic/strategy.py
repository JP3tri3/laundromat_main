import sys
sys.path.append("..")
# import asyncio
from logic.trade_logic import Trade_Logic
from logic.stop_loss import Stop_Loss
from logic.calc import Calc as calc
from api.bybit_api import Bybit_Api
import controller.comms as comms
from database.database import Database as db
from model.trades import Trade
from time import time, sleep

class Strategy_VWAP_Cross:

    def __init__(self, api_key, api_secret, trade_id, strat_id, symbol, symbol_pair, key_input, input_quantity, leverage, limit_price_difference, vwap_margin_neg_input, vwap_margin_pos_input):
        self.trade_id = trade_id
        self.strat_id = strat_id
        self.vwap_margin_neg = vwap_margin_neg_input
        self.vwap_margin_pos = vwap_margin_pos_input
        self.last_vwap = 0.0
        self.current_vwap = 0.0
        self.last_trend = ""
        self.input_quantity = input_quantity
        self.leverage = leverage
        self.key_input = key_input
        self.trade_record_id = 0

        self.tl = Trade_Logic(api_key, api_secret, symbol, symbol_pair, key_input, leverage, limit_price_difference)
        self.api = Bybit_Api(api_key, api_secret, symbol, symbol_pair, self.key_input)

    #single

    def create_trade_record(self, percent_gain):
        global trade_record_id

        self.trade_record_id = self.trade_record_id + 1

        trade = Trade(self.trade_id, self.trade_record_id)
        coin_gain = self.api.calc_total_coin(self.input_quantity)
        dollar_gain = self.api.calc_total_gain(self.input_quantity)
        entry_price = self.api.get_entry_price(self.input_quantity)
        exit_price = self.api.get_exit_price(self.input_quantity)

        return (trade.commit_trade_record(coin_gain, dollar_gain, entry_price, exit_price, percent_gain))

    def determine_vwap_trend(self):
        global last_vwap
        global current_vwap
        global last_trend

        new_trend = ""
        strat_kv_dict = db().get_strat_values(self.strat_id)
        last_candle_vwap = strat_kv_dict['last_candle_vwap']
        active_trend = strat_kv_dict['active_trend']

        if (last_candle_vwap != self.current_vwap):
            self.last_vwap = self.current_vwap
            print("")
            print("last_vwap: " + str(self.last_vwap))
            self.current_vwap = last_candle_vwap
            print("current vwap: " + str(self.current_vwap))
            print(self.current_vwap)
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
                    db().set_active_position(self.strat_id, 'change')
                if ((self.last_trend == 'cross_up') and (new_trend == 'cross_down')) \
                    or ((self.last_trend == 'cross_down') and (new_trend == 'cross_up')):
                    db().set_new_trend(self.strat_id, new_trend)

            db().set_new_trend(self.strat_id, new_trend)
            self.last_trend = new_trend
            db().set_last_trend(self.strat_id, self.last_trend)


    def vwap_cross_strategy(self):
        side = None
        start_flag = True
        counter = 0
        counter_condition = 60

        while (start_flag == True):
            
            sleep(1)
            counter += 1

            if (counter == counter_condition):
                print("waiting on input...")
                calc().time_stamp()
                counter = 0

            self.determine_vwap_trend()
            strat_kv_dict = db().get_strat_values(self.strat_id)
            new_trend = strat_kv_dict['new_trend']
            last_candle_wt1 = strat_kv_dict['wt1']
            last_candle_wt2 = strat_kv_dict['wt2']
            active_trend = strat_kv_dict['active_trend']

            if (new_trend != 'null') and (new_trend != active_trend):
                db().set_new_trend(self.strat_id, 'null')
                if (new_trend == 'cross_up') or (new_trend == 'cross_down'):
                    if (self.tl.active_position_check() == 1):
                        side = self.api.get_position_side()
                        db().set_side(self.trade_id, self.api.get_position_side())
                        entry_price = self.api.get_entry_price(self.input_quantity)
                        percent_gain = calc().calc_percent_gained(side, entry_price, self.api.last_price(), self.leverage)
                        db().set_stop_loss(self.trade_id, 0.0)
                        self.tl.close_position_market()
                        self.create_trade_record(percent_gain)

                    if ((new_trend == 'cross_up') and (last_candle_wt1 < 5) and (last_candle_wt2 < 5)) or (new_trend == 'cross_down') and (last_candle_wt1 > -5) and (last_candle_wt2 > -5):
                        if (new_trend == 'cross_up'):
                            print("Opening new Long:")
                            side = 'Buy'
                            self.tl.create_order(side_input=side, order_type='Market', input_quantity=self.input_quantity)

                        elif (new_trend == 'cross_down'):
                            print("Opening new Short:")
                            side = 'Sell'
                            self.tl.create_order(side_input=side, order_type='Market', input_quantity=self.input_quantity)

                        db().set_side(self.trade_id, side)

                        db().set_active_trend(self.strat_id, new_trend)
                        db().set_active_position(self.strat_id, 'null')

                        #process Stop Loss:
                        print("Checking for stop loss...")
                        flag = True
                        counter = 0
                        tempTime = 60

                        self.sl = Stop_Loss()
                        entry_price = self.api.get_entry_price(self.input_quantity)

                        while (flag == True):
                            percent_gain = calc().calc_percent_gained(side, entry_price, self.api.last_price(), self.leverage)
                            counter += 1
                            self.determine_vwap_trend()
                            #display counter
                            if (counter == tempTime):
                                counter = 0
                                print("Waiting - Update SL")
                                print("")

                            elif(counter == tempTime/6):
                                    print("Waiting")

                            elif(db().get_active_position(self.strat_id) == 'change'):
                                flag = False

                            #process SL if position is active
                            else:
                                if(self.tl.active_position_check() == 1):
                                    strat_kv = db().get_strat_values(self.strat_id)
                                    last_candle_high = strat_kv['last_candle_high']
                                    last_candle_low = strat_kv['last_candle_low']
                                    one_percent_less_entry = calc().calc_one_percent_less_entry(self.leverage, entry_price)

                                    stop_loss = self.sl.candles_stop_loss_strat(last_candle_high, last_candle_low, one_percent_less_entry, side, self.api.last_price())
                                    
                                    if (stop_loss != 0):
                                        print("Stop Loss: " + str(stop_loss))
                                        print("Last Price: " + str(self.api.last_price()))
                                        self.api.change_stop_loss(stop_loss)
                                        db().set_stop_loss(self.trade_id, stop_loss)     
                                            
                                    sleep(1)

                                else:
                                    print("Position Closed")
                                    print("")
                                    db().set_active_trend(self.strat_id, 'null')
                                    self.create_trade_record(percent_gain)
                                    flag = False


#check for order of last_trend verse new_trend

class Strategy_DCA:

    def __init__(self, api_key, api_secret, trade_id, strat_id, symbol, symbol_pair, key_input, input_quantity, leverage, limit_price_difference):
        self.trade_id = trade_id
        self.strat_id = strat_id
        self.input_quantity = input_quantity
        self.max_number_of_trades = 12
        self.leverage = leverage
        self.key_input = key_input
        self.trade_record_id = 0
        self.limit_price_difference = limit_price_difference

        self.tl = Trade_Logic(api_key, api_secret, symbol, symbol_pair, key_input, leverage, limit_price_difference)
        self.api = Bybit_Api(api_key, api_secret, symbol, symbol_pair, self.key_input)

    def dca_multi_position(self, side):

        trade_amount_percent_difference = 0.10
        
        # self.tl.create_order()


        #Determine Trade amount
        number_of_trades = 0
        safety_trade_amount = 1
        final_position = 0

        while (number_of_trades > self.max_number_of_trades) or (number_of_trades == 0):
            number_of_trades = 1
            position = safety_trade_amount
            # print("POS OUTSIDE " + str(position))
            trade_amount = safety_trade_amount            

            while (position < self.input_quantity) or (number_of_trades == 0):
                trade_amount = trade_amount * (trade_amount_percent_difference + 1)
                position += trade_amount
                number_of_trades += 1
                # print("Num Trades: " + str(number_of_trades))
                # print("Pos: " + str(position))
                # print("Trade Amount: " + str(trade_amount))

            if(number_of_trades > self.max_number_of_trades):
                safety_trade_amount += 0.2
                final_position = position
                # print("Starting Trade Amount: " + str(starting_trade_amount))
            else:
                print("Starting Trade Amount: ")
                print(safety_trade_amount)
                print(final_position)

        #Set Trade Values
        profit_percent = 0.0025
        max_active_open_orders = 5
        active_trade_amount = 0
        main_pos_entry = 0
        secondary_pos_entry = 0

        if (side == 'Buy'):
            #create initial Main Pos limit order:
            # self.tl.create_limit_order(self.api.last_price() - self.limit_price_difference, 'Buy', active_trade_amount, 0, False)
            # print("Forcing Main Pos Limit Order")
            # self.tl.force_limit_order(side)
            #TEST W/ MARKET:
            self.api.place_order(self.api.last_price(), 'Market', 'Buy', safety_trade_amount, 0, 'PostOnly', False)
            print("Main Pos Entry: " + str(self.api.get_active_position_entry_price()))
            main_pos_entry = float(self.api.get_active_position_entry_price())

            #create initial limit sell order:
            price = calc().calc_percent_above(main_pos_entry, profit_percent)
            print(price)
            print(self.api.last_price())
            print("SELL PRICE: " + str(price))
            self.api.place_order(price, 'Limit', 'Sell', safety_trade_amount, 0, 'PostOnly', True)

            #calculate and create open orders below Main pos:
            percent_spread = profit_percent / max_active_open_orders
            secondary_trade_amount = safety_trade_amount / max_active_open_orders

            for i in range(1, max_active_open_orders + 1):
                price = calc().calc_percent_below(main_pos_entry, profit_percent * i)
                self.api.place_order(price, 'Limit', 'Buy', secondary_trade_amount, 0, 'PostOnly', False)

                print(str(i) + ": Secondary Pos Price: " + str(price))

            # self.api.change_order_price(self.api.last_price() - 300, buy_order_1['order_id'])

            #check for active Main position:
            flag = True
            
            while (flag == True):
            # while (self.tl.active_position_check == 1):
                #check for active order changes:
                closest_open_order = 0
                
                order_list = self.api.get_orders_id_and_price()
                open_orders_list = []
                close_orders_list = []

                #Separate order_list
                for x in range(len(order_list)):
                    if (order_list[x]['side'] == 'Buy'):
                        open_orders_list.append(order_list[x])
                        if(order_list[x]['price']) > str(closest_open_order):
                            closest_open_order = order_list[x]['price']
                    else:
                        close_orders_list.append(order_list[x])

                #check for open order change:
                if (self.check_open_order_change(open_orders_list, closest_open_order) == True):
                    print("break")
                    flag = False

            print("OPEN")
            print(open_orders_list)
            print("CLOSE")
            print(close_orders_list)
                # for x in range(len(order_list)):
                #     check_price = order_list[x]['price']
                #     if 


    def check_open_order_change(self, open_orders_list, closest_open_order):
        order_change_check = True
        print("Checking")
        for x in range(len(open_orders_list)):
            print(x)
            if (open_orders_list[x]['price'] == closest_open_order):
                print(closest_open_order)
                order_change_check = False
                break
            
            if (order_change_check == True):
                print("ORDER CLOSED")
                print(order_change_check)
            
        return order_change_check


