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

    def __init__(self, api_key, api_secret, trade_id, strat_id, symbol, symbol_pair, key_input, input_quantity, leverage, limit_price_difference):
        self.trade_id = trade_id
        self.strat_id = strat_id
        self.input_quantity = input_quantity
        self.max_number_of_trades = 20
        self.leverage = leverage
        self.key_input = key_input
        self.trade_record_id = 0
        self.limit_price_difference = limit_price_difference
        self.trade_record_id = 0

        self.tl = Trade_Logic(api_key, api_secret, symbol, symbol_pair, key_input, leverage, limit_price_difference)
        self.api = Bybit_Api(api_key, api_secret, symbol, symbol_pair, self.key_input)

    #Create Trade Record
    #TODO: Fix gain calculation
    def create_trade_record(self, input_quantity, profit_percent, entry_price, exit_price):
        global trade_record_id

        self.trade_record_id = self.trade_record_id + 1

        trade = Trade(self.trade_id, self.trade_record_id)
        
        #TEMP VALUES
        percent_gain = 0
        coin_gain = 0

        dollar_gain = input_quantity * (profit_percent * self.leverage)

        return (trade.commit_trade_record(coin_gain, dollar_gain, entry_price, exit_price, percent_gain, input_quantity))


    def dca_multi_position(self, side):

        entry_side = side
          
        if (entry_side == 'Buy'):
            exit_side = 'Sell'
        else:
            exit_side = 'Buy'


        available_trades = self.max_number_of_trades
        available_input_quantity = self.input_quantity
        safety_trade_amount = available_input_quantity / available_trades

        closest_entry_price = 0
        closest_exit_price = 0

        #Set Trade Values
        profit_percent = 0.0025
        percent_rollover = 0.05
        max_active_open_orders = 5

        current_active_entry_orders = 0
        current_active_exit_orders = 0
        used_input_quantity = 0
        main_pos_entry = 0

        # secondary_pos_entry = 0

        while(used_input_quantity <= (self.input_quantity - safety_trade_amount)):
            main_entry_input_quantity = 0
            secondary_entry_input_quantity = 0

            print("Used Input Quantity: ")
            print(used_input_quantity)
            print("Available Input Quantity: ")
            print(self.input_quantity - safety_trade_amount)
            #create initial Main Pos limit order w/ Force Limit:
            # self.tl.create_limit_order(self.api.last_price() - self.limit_price_difference, entry_side, active_trade_amount, 0, False)
            # print("Forcing Main Pos Limit Order")
            # self.tl.force_limit_order(side)
            #TEST W/ MARKET:

            main_entry_input_quantity = safety_trade_amount
            self.api.place_order(self.api.last_price(), 'Market', entry_side, main_entry_input_quantity, 0, False)
            
            main_pos_entry = float(self.api.get_active_position_entry_price())

            #create initial limit sell order:
            price = calc().calc_percent_difference('long', 'exit', main_pos_entry, profit_percent)
            print("SELL PRICE: " + str(price))
            self.api.place_order(price, 'Limit', exit_side, safety_trade_amount, 0, True)
            
            current_active_exit_orders += 1

            #calculate and create open orders below Main pos:
            percent_spread = profit_percent / max_active_open_orders
            secondary_entry_input_quantity = safety_trade_amount / max_active_open_orders
            secondary_exit_input_quantity = secondary_entry_input_quantity * (1 - percent_rollover)
            secondary_entry_price = main_pos_entry

            orders_dict = self.get_orders_dict(entry_side)

            
            active_open_orders = len(orders_dict[side])
            available_orders = max_active_open_orders - active_open_orders
            print("ACTIVE OPEN ORDERS")
            print(active_open_orders)
            print("AVAILABLE ORDERS")
            print(available_orders)

            if (available_orders >= 0):
                print('active open orders range: ')
                print(range(active_open_orders))
                print("Pre-change Orders: ")
                print(print(orders_dict[entry_side]))
                for x in range(active_open_orders):
                    i = (active_open_orders - x) -1
                    order_id = orders_dict[entry_side][i]['order_id']
                    price = calc().calc_percent_difference('long', 'entry', secondary_entry_price, profit_percent)
                    print(str(x + 1) + ": Secondary Pos Change Order Price: " + str(price))
                    self.api.change_order_price(price, secondary_entry_input_quantity, order_id)
                    secondary_entry_price = price
                    print("")

                for x in range(available_orders):
                    price = calc().calc_percent_difference('long', 'entry', secondary_entry_price, profit_percent)
                    print(str(x + 1) + ": Secondary Pos Price: " + str(price))
                    self.api.place_order(price, 'Limit', entry_side, secondary_entry_input_quantity, 0, False)
                    secondary_entry_price = price


            #Loop check for active Main position:

            while (self.tl.active_position_check() == 1):
                print("In active pos loop")
                (print(""))

                orders_dict = self.get_orders_dict(entry_side)
                main_pos_order_id = orders_dict[exit_side][0]['order_id']

                #update initial values:
                current_active_entry_orders = self.get_current_number_open_orders(orders_dict)
                main_pos_entry = float(self.api.get_active_position_entry_price())
                used_input_quantity = self.get_used_input_quantity(orders_dict['input_quantity'])

                #pull open orders & closest open:
                if (len(orders_dict[entry_side]) == 0):
                    closest_entry_price = 0
                else:
                    closest_entry_price = orders_dict[entry_side][0]['price']
                    print("Closest Entry Price: ")
                    print(closest_entry_price)

                if(len(orders_dict[exit_side]) == 0):
                    closest_exit_price = 0
                else:
                    closest_exit_price = orders_dict[exit_side][0]['price']
                    print("Closest Exit Price: ")
                    print(closest_exit_price)

                #Loop check for secondary orderschange:
                ticker = 0
                timer = 60
                while (True):
                    
                    #Display Timer:
                    if (ticker == timer):
                        print("Checking for Order Change")
                        ticker = 0

                    ticker +=1
                    sleep(2)

                    #TEST PRINTS
                    # print("# of Entrys:")
                    # print(len(orders_dict[entry_side]))
                    # print("# of Exits:")
                    # print(len(orders_dict[exit_side]))

                    if (len(orders_dict[exit_side]) == 0):
                        if (self.tl.active_position_check() == 0):
                            print("No Valid Exit Orders")
                            break
                    # elif (len(orders_dict[entry_side]) == 0):
                    #     print("No Valid Entry Orders")
                    #     continue
                    else:
                    #check for open order change
                        if (self.check_order_change(orders_dict[entry_side], closest_entry_price) == 1):
                            print("Buy order added")
                            #create new secondary exit order after entry order is hit:
                            main_entry_input_quantity += (secondary_entry_input_quantity - secondary_exit_input_quantity)
                            print("main_entry_input_quantity: ")
                            print(main_entry_input_quantity)
                            print('')

                            closest_exit_price = calc().calc_percent_difference('long', 'exit', closest_entry_price, profit_percent)
                            main_pos_entry = float(self.api.get_position_entry_price())

                            if(closest_exit_price > self.api.last_price()):
                                self.api.place_order(closest_exit_price, 'Limit', exit_side, secondary_exit_input_quantity, 0, True)
                                print("new close order created")

                            #TEST PRINT
                            print("Exit Orders:")
                            orders_dict = self.get_orders_dict(entry_side)
                            print(orders_dict[exit_side])
                            break

                        #check for close order change:
                        elif (self.check_order_change(orders_dict[exit_side], closest_exit_price) == 1):
                            self.create_trade_record(secondary_entry_input_quantity, profit_percent, closest_entry_price, closest_exit_price)
                            print("Position closed")
                            #create new secondary entry after exit order is hit:
                            closest_entry_price = calc().calc_percent_difference('long', 'entry', self.api.last_price(), profit_percent)
                            print("new closest entry price: ")
                            print(closest_entry_price)
                            print("Last Price: ")
                            print(self.api.last_price())

                            if (self.api.last_price() > closest_entry_price):
                                self.api.place_order(closest_entry_price, 'Limit', entry_side, secondary_entry_input_quantity, 0, True)
                                print("new open order created")

                            #Update Main Pos exit:
                            self.update_main_pos_exit_order(profit_percent)

                            #TEST PRINT
                            print("Entry Orders")
                            orders_dict = self.get_orders_dict(entry_side)
                            print(orders_dict[entry_side])
                            break

                        orders_dict = self.get_orders_dict(entry_side)
                    

                self.create_trade_record(main_entry_input_quantity, profit_percent, closest_entry_price, closest_exit_price)


    #update main pos exit order
    def update_main_pos_exit_order(self, profit_percent):
        #TODO: fix input quantity calculation
        main_pos_entry = float(self.api.get_active_position_entry_price())
        main_pos_quantity = self.api.get_position_size()
        price = calc().calc_percent_difference('long', 'exit', main_pos_entry, profit_percent)
        self.api.change_order_price_size(price, main_pos_quantity, main_pos_order_id)

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
        order_list = self.api.get_orders_id_and_price()
        entry_orders_list = []
        exit_orders_list = []
        input_quantity_list = []

        order_list_kv = {}

        for x in range(len(order_list)):
            if (order_list[x]['side'] == entry_side):
                entry_orders_list.append(order_list[x])
                input_quantity_list.append(order_list[x]['input_quantity'])
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