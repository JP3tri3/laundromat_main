import sys
sys.path.append("..")
from logic.trade_logic import Trade_Logic
from logic.stop_loss import Stop_Loss
from logic.calc import Calc as calc
from api.bybit_api import Bybit_Api
from database.database import Database as db
from model.trades import Trade
from time import time, sleep
from strategies import dca_logic

#TODO: add confirmation for orders being placed
class Strategy_DCA:

    def __init__(self, api_key, api_secret, trade_id, strat_id, symbol, symbol_pair, key_input, input_quantity, leverage, limit_price_difference, max_active_positions):
        self.trade_id = trade_id
        self.strat_id = strat_id
        self.input_quantity = input_quantity
        self.max_active_positions = max_active_positions
        self.leverage = leverage
        self.key_input = key_input
        self.trade_record_id = 0
        self.limit_price_difference = limit_price_difference
        self.trade_record_id = 0

        self.tl = Trade_Logic(api_key, api_secret, symbol, symbol_pair, key_input, leverage, limit_price_difference)
        self.api = Bybit_Api(api_key, api_secret, symbol, symbol_pair, self.key_input)

        #TEMP: 
        self.open_equity = self.api.wallet_equity()


    #Create Trade Record
    def create_trade_record(self, profit_percent, closed_trade, index):
        global trade_record_id
        global open_equity

        self.trade_record_id = self.trade_record_id + 1
        print('trade_record_id: ' + str(self.trade_record_id))

        percent_gain = profit_percent * self.leverage

        print('')
        print('creating trade record: ')
        print(closed_trade)
        trade = Trade(self.trade_id, self.trade_record_id)
        exit_price = closed_trade['price']
        entry_price = exit_price * (1 - profit_percent)
        input_quantity = closed_trade['input_quantity']
        if index == 0:
            current_last_price = self.api.last_price()
            current_equity = self.api.wallet_equity()
            coin_gain = current_equity - self.open_equity
            dollar_gain = coin_gain * current_last_price
            self.open_equity = current_equity
        else:
            coin_gain = 0
            dollar_gain = 0
            
        trade.commit_trade_record(coin_gain, dollar_gain, entry_price, exit_price, percent_gain, input_quantity)


    def dca_multi_position(self, entry_side):
         
        if (entry_side == 'Buy'):
            exit_side = 'Sell'
        else:
            exit_side = 'Buy'

        #Set Trade Values
        set_profit_percent = 0.01
        percent_rollover = 0.0
        max_active_positions = self.max_active_positions
        active_secondary_orders = 15 - 1

        available_positions = max_active_positions
        available_input_quantity = self.input_quantity
        position_trade_quantity = self.input_quantity / max_active_positions

        #TODO: add percent calculation: 
        main_pos_percent_of_total_quantity = 1 / (active_secondary_orders + 1)
        main_pos_input_quantity = round(position_trade_quantity * main_pos_percent_of_total_quantity, 0)
        secondary_pos_input_quantity = round(position_trade_quantity - main_pos_input_quantity, 0)

        profit_percent = set_profit_percent / self.leverage
        current_active_entry_orders = 0
        current_active_exit_orders = 0
        used_input_quantity = 0
        main_pos_entry = 0

        #### TEST ####
        # print(self.api.my_wallet_ttl_equity())

        # TEST flag
        test_flag = True

        while(test_flag == True):
            print("!! IN MAIN LOOP !!")
            # while(used_input_quantity <= (self.input_quantity - position_trade_quantity)):

            # TEST BALANCE at Start:
            open_p_l = self.api.wallet_realized_p_l()

            # force initial Main Pos limit close order
            print('')
            print('creating main_pos entry: ')
            limit_price_difference = self.limit_price_difference
            self.api.force_limit_order(entry_side, main_pos_input_quantity, limit_price_difference, 0, False)

            # TEST W/ MARKET Order:
            # print('')
            # print('creating main_pos entry: ')
            # self.api.place_order(self.api.last_price(), 'Market', entry_side, main_pos_input_quantity, 0, False)
            
            main_pos_entry = round(self.api.get_active_position_entry_price(), 0)

            #create initial Main Pos limit close order:
            print('')
            print('creating main_pos exit: ')
            main_pos_exit_price = calc().calc_percent_difference('long', 'exit', main_pos_entry, profit_percent)
            print("SELL PRICE: " + str(main_pos_exit_price))
            # self.api.place_order(main_pos_exit_price, 'Limit', exit_side, main_pos_input_quantity, 0, True)
            main_pos_exit_order_id = self.api.create_limit_order(main_pos_exit_price, exit_side, main_pos_input_quantity, 0, True)
            print('main_pos_exit_order_id: ' + str(main_pos_exit_order_id))

            current_active_exit_orders += 1

            orders_dict = dca_logic.get_orders_dict(entry_side, self.api.get_orders_info())

            if (orders_dict[exit_side] == []):
                main_pos_exit_order_id = 'null'
            else:
                main_pos_exit_order_info = orders_dict[exit_side][0]

            #calculate and create open orders below Main pos:
            #percent_spread = profit_percent / active_secondary_orders

            secondary_entry_input_quantity = int(secondary_pos_input_quantity / active_secondary_orders)
            secondary_exit_input_quantity = secondary_entry_input_quantity * (1 - percent_rollover)
            secondary_entry_price = main_pos_entry

            #determine active & available orders
            active_entry_orders = len(orders_dict[entry_side])
            active_exit_orders = len(orders_dict[exit_side]) - 1
            total_active_orders = active_exit_orders + active_entry_orders
            available_entry_orders = active_secondary_orders - total_active_orders
            secondary_entry_price = main_pos_entry

            #create_price_list:
            print('')
            print('checking for available entries: ')
            for x in range(available_entry_orders):
                entry_price = calc().calc_percent_difference('long', 'entry', secondary_entry_price, profit_percent)
                secondary_entry_price = entry_price
                print('')
                print("Adding Entry Order")
                self.api.place_order(entry_price, 'Limit', entry_side, secondary_entry_input_quantity, 0, False)

            print('')
            print('checking for active entries: ')
            for x in range(active_entry_orders):
                entry_price = calc().calc_percent_difference('long', 'entry', secondary_entry_price, profit_percent)
                secondary_entry_price = entry_price
                order_id = orders_dict[entry_side][x]['order_id']
                self.api.change_order_price_size(entry_price, secondary_entry_input_quantity, order_id)

            init_orders_list = self.api.get_orders_info()

            ticker = 0
            timer = 30
            while (self.tl.active_position_check() != 0):

                #Display Timer:
                if (ticker == timer):
                    print("Checking for Order Change")
                    ticker = 0

                ticker +=1
                sleep(1)
                #End Display Timer

                #init list to check against, equals maximum orders
                
                if (init_orders_list == []):
                    init_orders_list = self.api.get_orders_info()

                #create new list in loop and check for changes
                orders_list = self.api.get_orders_info()
                orders_waiting = dca_logic.get_orders_not_active(init_orders_list, orders_list)

                if (orders_waiting != []):
                    num_orders_waiting = len(orders_waiting)
                    #index for creating trade order / checking profit
                    p_l_index = 0
                    for x in range(num_orders_waiting):
                        print('')
                        print('processing waiting available orders: ')
                        #test: 
                        print('num_orders_waiting: ' + str(num_orders_waiting))
                        print('x: ' + str(x))
                        order_waiting = orders_waiting[x]

                        if order_waiting['order_id'] == main_pos_exit_order_id:
                            #check for closed main_pos exit order

                            while (x < num_orders_waiting):
                                print('in main_pos exit loop: ')
                                print('x: ' + str(x))
                                print('num_orders_waiting: ' + str(num_orders_waiting))
                                if (orders_waiting[x]['side'] == exit_side):
                                    self.create_trade_record(profit_percent, orders_waiting[x], p_l_index)
                                x += 1
                                p_l_index += 1

                            print("Main Pos Closed")
                            print("Breaking")
                            print('')
                            break

                        if order_waiting['side'] == entry_side:
                            #create new exit order upon entry close
                            print("creating new exit order")
                            exit_price = float(orders_waiting[x]['price'])
                            price = str(calc().calc_percent_difference('long', 'exit', exit_price, profit_percent))
                            # self.api.place_order(price, 'Limit', exit_side, secondary_exit_input_quantity, 0, False)
                            order = self.api.create_limit_order(price, exit_side, secondary_exit_input_quantity, 0, True)
                            if (order == 0):
                                print('create new exit order failed')
                                print('attempted price: ' + str(price))
                                print('last_price: ' + str(self.api.last_price()))
                                

                        elif order_waiting['side'] == exit_side:
                            self.create_trade_record(profit_percent, orders_waiting[x], p_l_index)
                            #create new entry order upon exit close
                            print("Creating Trade Record")
                            entry_price = float(orders_waiting[x]['price'])
                            print('creating new entry order')
                            price = calc().calc_percent_difference('long', 'entry', entry_price, profit_percent)
                            # self.api.place_order(price, 'Limit', entry_side, secondary_entry_input_quantity, 0, False)                                   
                            order = self.api.create_limit_order(price, entry_side, secondary_entry_input_quantity, 0, False)
                            p_l_index += 1
                            if (order == 0):
                                print('create new entry order failed')
                                print('attempted price: ' + str(price))
                                print('last_price: ' + str(self.api.last_price()))

                    ## TEST ##
                    if main_pos_exit_order_id == 'null':
                        print('main_pos_exit_order_id null test succesful')
                        test_flag = False
                    
                    self.api.update_main_pos_exit_order(profit_percent, main_pos_exit_order_id, 'long', 'exit')
                    init_orders_list = []

            # TEST Close
            # print('cancel_all_orders: ')
            # self.api.cancel_all_orders()
            # dca_logic.print_closed_balance_details(self.api.last_price(), open_balance, open_p_l, self.api.my_wallet(), self.api.my_wallet_realized_p_l())
            
            # test_flag = False









        





