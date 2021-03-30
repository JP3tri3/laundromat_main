import sys
sys.path.append("..")
import controller.comms as comms
from api.bybit_api import Bybit_Api
import config
from model.orders import Orders
from model.stop_loss import Stop_Loss
from model.calc import Calc
import database.sql_connector as conn

class Ui:

    def start(self):
        flag = True

        #manual Setters:
        leverage = 5
        input_quantity = 100 * leverage
        data_name = ''
        trade_id = 'bybit_manual'
        api_key = config.BYBIT_TESTNET_API_KEY
        api_secret = config.BYBIT_TESTNET_API_SECRET

        while (flag == True):
            symbol_pair = input("Enter Symbol: ").upper()
            if (symbol_pair == "BTCUSD") or (symbol_pair == "ETHUSD"):
                flag = False
            else:
                print("Invalid Input, try 'BTCUSD' or 'ETHUSD'")

        if (symbol_pair == "BTCUSD"):

            symbol = 'BTC'
            key_input = 0
            limit_price_difference = 0.50
            conn.updateTradeValues(trade_id, 'manual', symbol, symbol_pair,  0, limit_price_difference, leverage, input_quantity, 'empty', 0, 0, 0)

        elif (symbol_pair == "ETHUSD"):

            symbol = 'ETH'
            key_input = 1
            limit_price_difference = 0.05
            conn.updateTradeValues(trade_id, 'manual', symbol, key_input, 1, limit_price_difference, leverage, input_quantity, 'empty', 0, 0, 0)


        self.api = Bybit_Api(api_key, api_secret, symbol, symbol_pair, key_input, input_quantity, leverage)
        self.orders = Orders(api_key, api_secret, symbol, symbol_pair, key_input, input_quantity, leverage, limit_price_difference)
        self.sl = Stop_Loss()
        self.calc = Calc()

        self.inputOptions(symbol_pair)
        self.startMenu(symbol_pair, trade_id)

    def inputOptions(self, symbol_pair):
        print("")
        print("TESTNET - Input Options:")
        print("")
        print("Symbol: " + symbol_pair)
        print("")
        print("Market Actions:")
        print("")
        print("Create Long Order: 'long'")
        print("Create Short Order: 'short'")
        print("Create Long Market Order: 'long market'")
        print("Create Short Market Order: 'short market'")
        print("Cancel Pending Orders: 'cancel'")
        print("SL Close: 'closesl'")
        print("Market Close: 'closem'")
        print("")
        print("Development Info:")
        print("")
        print("Stop Loss: 'stoploss'")
        print("Price Info: 'price info'")
        print("Symbol Info: 'info'")
        print("Wallet: 'wallet'")
        print("Active Orders: 'active'")
        print("Position: 'position'")
        print("Update SL: 'update sl'")
        print("Change Currency: change")
        print("Exit: 'exit'")

    def startMenu(self, symbol_pair, trade_id):
        flag = True
        input_quantity = conn.viewDbValue('trades', trade_id, 'input_quantity')

        while(flag == True):

            print("")
            taskInput = input("Input Task: ")
            comms.time_stamp()

            if(taskInput == "exit"):
                self.shutdown()

            elif(taskInput == "price info"):
                self.api.price_info()

            elif(taskInput == "info"):
                print(self.api.symbol_info_result())

            elif(taskInput == "long"):
                self.orders.create_order("Buy", 'Limit', input)

            elif(taskInput == "short"):
                self.orders.create_order("Sell", 'Limit', input_quantity)

            elif(taskInput == "long market"):
                self.orders.create_order('Buy', 'Market', input_quantity)

            elif(taskInput == "short market"):
                self.orders.create_order("Sell", 'Market', input_quantity)

            elif(taskInput == "wallet"):
                self.api.my_wallet()

            elif(taskInput == "stoploss"):
                self.sl.change_stop_loss(500)
                print("Updated Stop Loss")

            elif(taskInput == "closesl"):
                self.orders.close_position_sl()

            elif(taskInput == "closem"):
                self.orders.close_position_market()

            elif(taskInput == "cancel"):
                self.api.cancel_all_orders()
                print("Orders Cancelled")

            elif(taskInput == "active"):
                print(self.orders.active_order_check())

            elif(taskInput == "position"):
                print("Position: ")
                self.orders.active_position_check()

            elif(taskInput == "test"):
                print(self.orders.testOrder())

            elif(taskInput == "test1"):
                print(self.orders.active_position_check())

            elif(taskInput == "test2"):
                print(self.api.closed_profit_loss())

            elif(taskInput == "change"):
                flag = False
                self.start()

            elif(taskInput == "update sl"):
                flag = False
                while(flag == False):
                    sl_amountInput = input("Enter SL Amount:")
                    if sl_amountInput.isnumeric():
                        flag = True
                        self.sl.change_stop_loss(sl_amountInput)
                    else:
                        print("Invalid Entry...")

            else:
                print("Invalid Input, try again...")
                self.inputOptions(symbol_pair)

    def shutdown(self):
        print("")
        print("Shutting down...")
        sys.exit("Program Terminated")
        print("")

