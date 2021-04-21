import sys
sys.path.append("..")
from logic.trade_logic import Trade_Logic
from logic.stop_loss import Stop_Loss
from logic.calc import Calc as calc
from api.bybit_api import Bybit_Api
from database.database import Database as db
from model.trades import Trade
from time import time, sleep


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

    #Create Trade Record
    def create_trade_record(self, profit_percent, closed_trades_list, exit_side):
        global trade_record_id
        
        #TODO: 
        #figure out capturing entry/exit/profits

        percent_gain = profit_percent * self.leverage
        profit_loss_records = self.api.closed_profit_loss()

        for x in range(len(closed_trades_list)):
            print("In trade_record loop:")
            closed_trade = closed_trades_list[x]

            if (closed_trade['side'] == exit_side):
                print('')
                print('creating trade record: ')
                index = 0
                order_record = profit_loss_records[index]
                order_id = closed_trade['order_id']
                for x in range(len(profit_loss_records)):
                    if (order_record['order_id'] == order_id):
                        trade = Trade(self.trade_id, self.trade_record_id)
                        print('')
                        print('found correct trade record: ')
                        print(order_record)
                        self.trade_record_id = self.trade_record_id + 1
                        print('trade_record_id: ' + str(self.trade_record_id))
                        exit_price = order_record['avg_exit_price']
                        entry_price = order_record['avg_entry_price'] * (1 + profit_percent)
                        coin_gain = 0
                        input_quantity = order_record['qty']
                        dollar_gain = input_quantity * percent_gain
                        print('creating trade record: ')
                        trade.commit_trade_record(coin_gain, dollar_gain, entry_price, exit_price, percent_gain, input_quantity)
                        break
                    else:
                        print('')
                        print("didn't find trade record, trying again")
                        print('index: ' + str(index))
                        index += 1
            else:
                print("not exit order, continuing")

        


    def dca_multi_position(self, side):

        entry_side = side
          
        if (entry_side == 'Buy'):
            exit_side = 'Sell'
        else:
            exit_side = 'Buy'

        #Set Trade Values
        set_profit_percent = 0.002
        percent_rollover = 0.0
        max_active_positions = self.max_active_positions
        active_secondary_orders = 10

        available_positions = max_active_positions
        available_input_quantity = self.input_quantity
        position_trade_quantity = self.input_quantity / max_active_positions

        main_pos_percenty_of_total_quantity = 0.5
        main_pos_input_quantity = position_trade_quantity * main_pos_percenty_of_total_quantity
        secondary_pos_input_quantity = position_trade_quantity - main_pos_input_quantity

        profit_percent = set_profit_percent / self.leverage
        current_active_entry_orders = 0
        current_active_exit_orders = 0
        used_input_quantity = 0
        main_pos_entry = 0

        #### TEST ####
        

        # #TEST flag
        test_flag = True

        while(test_flag == True):
            print("!! IN MAIN LOOP !!")
        # while(used_input_quantity <= (self.input_quantity - position_trade_quantity)):

            #create initial Main Pos limit order w/ Force Limit:
            # self.tl.create_limit_order(self.api.last_price() - self.limit_price_difference, entry_side, active_trade_amount, 0, False)
            # print("Forcing Main Pos Limit Order")
            # self.tl.force_limit_order(side)
            #TEST W/ MARKET:

            print('')
            print('creating main_pos entry: ')
            self.api.place_order(self.api.last_price(), 'Market', entry_side, main_pos_input_quantity, 0, False)
            
            main_pos_entry = round(self.api.get_active_position_entry_price(), 0)

            #create initial limit sell order:
            print('')
            print('creating main_pos exit: ')
            main_pos_exit_price = calc().calc_percent_difference('long', 'exit', main_pos_entry, profit_percent)
            print("SELL PRICE: " + str(main_pos_exit_price))
            self.api.place_order(main_pos_exit_price, 'Limit', exit_side, main_pos_input_quantity, 0, True)
            
            current_active_exit_orders += 1

            orders_dict = self.get_orders_dict(entry_side)

            if (orders_dict[exit_side] == []):
                main_pos_exit_order_id = 'null'
            else:
                main_pos_exit_order_info = orders_dict[exit_side][0]
                main_pos_exit_order_id = main_pos_exit_order_info['order_id']

            #calculate and create open orders below Main pos:
            # percent_spread = profit_percent / active_secondary_orders
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

            # init_orders_list = self.api.get_orders_id_and_price()
            init_orders_list = self.api.get_orders()


            ticker = 0
            timer = 30
            while (self.api.get_position_size() != 0):

                #Display Timer:
                if (ticker == timer):
                    print('')
                    print("Checking for Order Change")
                    ticker = 0

                ticker +=1
                sleep(1)
                #End Display Timer

                #init list to check against, equals maximum orders
                
                if (init_orders_list == []):
                    # init_orders_list = self.api.get_orders_id_and_price()
                    init_orders_list = self.api.get_orders()

                #create new list in loop and check for changes
                orders_list = self.api.get_orders()
                orders_waiting = self.get_orders_not_active(init_orders_list, orders_list)

                if (orders_waiting != []):
                    for x in range(len(orders_waiting)):
                        print('')
                        print('processing waiting available orders: ')
                        order_waiting = orders_waiting[x]
                        # if order_waiting['order_id'] == main_pos_exit_order_id:
                        #     #check for closed main_pos exit order
                        #     self.create_trade_record(profit_percent, orders_waiting)
                        #     print("Main Pos Closed")
                        #     print("Breaking")
                        #     print('')
                        #     break

                        if order_waiting['side'] == entry_side:
                            #create new exit order upon entry close
                            print("creating new exit order")
                            exit_price = float(orders_waiting[x]['price'])
                            print('exit_price: ' + str(exit_price))
                            print(type(exit_price))
                            price = str(calc().calc_percent_difference('long', 'exit', exit_price, profit_percent))
                            self.api.place_order(price, 'Limit', exit_side, secondary_exit_input_quantity, 0, False)

                        elif order_waiting['side'] == exit_side:
                            print('')
                            print('exit_order_id: ')
                            print(order_waiting['order_id'])
                            #create new entry order upon exit close
                            print("Creating Trade Record")
                            entry_price = float(orders_waiting[x]['price'])
                            print('creating new entry order')
                            price = calc().calc_percent_difference('long', 'entry', entry_price, profit_percent)
                            self.api.place_order(price, 'Limit', entry_side, secondary_entry_input_quantity, 0, False)                                   


                    self.create_trade_record(profit_percent, orders_waiting, exit_side)
                    self.update_main_pos_exit_order(profit_percent, main_pos_exit_order_id)
                    init_orders_list = []


    # compare lists and return difference comparing order_id
    def get_orders_not_active(self, init_orders_list, active_orders_list):
        lst = init_orders_list.copy()

        for index in active_orders_list:
            order_id = index['order_id']
            for id in lst:
                if id['order_id'] == order_id:
                    lst.remove(id)
                    break
        return lst

    # def get_orders_diff(self):
    #     return (list(list(set(price_list)-set(active_orders_list)) + list(set(active_orders_list)-set(price_list))))


    #create price list for orders
    def create_order_price_list(self, initial_price, num_of_orders, profit_percent):
        lst = []
        index = 0
        entry_price = initial_price

        lst.append(round(initial_price, 0))

        for x in range(num_of_orders):
            entry_price = calc().calc_percent_difference('long', 'entry', entry_price, profit_percent)
            lst.append(round(entry_price, 0))
        return lst


    #update main pos exit order
    def update_main_pos_exit_order(self, profit_percent, order_id):
        print('update_main_pos_exit_order')
        main_pos_entry = float(self.api.get_active_position_entry_price())
        main_pos_quantity = self.api.get_position_size()
        price = calc().calc_percent_difference('long', 'exit', main_pos_entry, profit_percent)
        self.api.change_order_price_size(price, main_pos_quantity, order_id)

    #get number of open orders
    def get_current_number_open_orders(self, open_orders_list):
        return len(open_orders_list)

    #get last input quantity
    def get_last_input_quantity_dict(self, side, order_list):
        closest_order = self.get_closest_order_to_position(entry_side, order_list)
        last_input_quantity_kv = []
        secondary_pos_input_quantity = 0
        
        for x in range(len(order_list[side])):
            price = float(order_list[x]['price'])
            if(price == closest_order):
                secondary_pos_input_quantity = order_list[x]['input_quantity']

        last_input_quantity_kv['main'] = main_pos_input_quantity = self.api.get_position_size()
        last_input_quantity_kv['secondary'] = secondary_pos_input_quantity

        return last_input_quantity_kv
        

    #get current amount of input quantity in open orders & position
    def get_used_input_quantity(self, input_quantity_list):
        input_quantity = self.api.get_position_size()

        for x in range(len(input_quantity_list)):
            input_quantity += input_quantity_list[x]
        return input_quantity

    #retreive orders & separate into dict
    def get_orders_dict(self, entry_side):
        order_list = self.api.get_orders()
        entry_orders_list = []
        exit_orders_list = []
        input_quantity_list = []


        order_list_kv = {}

        for x in range(len(order_list)):

            if (order_list[x]['side'] == entry_side):
                entry_orders_list.append(order_list[x])
                input_quantity_list.append(order_list[x]['qty'])
            else:
                exit_orders_list.append(order_list[x])

        if (entry_side == 'Buy'):
            order_list_kv['Buy'] = sorted(entry_orders_list, key=lambda k: k['price'], reverse=True)
            order_list_kv['Sell'] = sorted(exit_orders_list, key=lambda k: k['price'])

        else:
            order_list_kv['Sell'] = sorted(entry_orders_list, key=lambda k: k['price'])
            order_list_kv['Buy'] = sorted(exit_orders_list, key=lambda k: k['price'], reverse=True)

        order_list_kv['input_quantity'] = input_quantity_list
        
        return order_list_kv




    #get closest order
    # def get_closest_order_to_position(self, side, order_list):
    #     closest_order = 0

    #     if (side == 'Buy'):
    #         for x in range(len(order_list)):
    #             price = float(order_list[x]['price'])
    #             if(price > closest_order):
    #                 closest_order = price
    #     elif (side == 'Sell'):
    #         for x in range(len(order_list)):
    #             price = float(order_list[x]['price'])
    #             if(price < closest_order) or (closest_order == 0):
    #                 closest_order = price
    #     return closest_order

    #check for order changes
    def check_order_change(self, orders_list, closest_order):
        order_change_check = 1

        if (len(orders_list) == 0):
            print("Orders List Empty")
            order_change_check = 0
        else:
            for x in range(len(orders_list)):
                price = float(orders_list[x]['price'])
                if (price == closest_order):
                    order_change_check = 0
                    break

        if (order_change_check == 1):
            print("")
            print("ORDER CLOSED")

        return order_change_check