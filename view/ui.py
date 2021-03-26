import sys
sys.path.append("..")
import database.database as db
import controller.comms as comms
from api.bybit_api import Bybit_Api
from model.orders import Orders
from model.stop_loss import Stop_Loss
from model.calc import Calc
import sql_connector as conn

class Ui:

    # def __init__(self):
    #     return

    def start(self):
        flag = True

        #manual Setters:
        leverage = 5
        inputQuantity = 100 * leverage
        data_name = ''

        while (flag == True):
            symbol_pair = input("Enter Symbol: ").upper()
            if (symbol_pair == "BTCUSD") or (symbol_pair == "ETHUSD"):
                flag = False
            else:
                print("Invalid Input, try 'BTCUSD' or 'ETHUSD'")

        if (symbol_pair == "BTCUSD"):
            id_name = 'bybit_btcusd_manual'
            conn.updateTradeValues(id_name, 'BTC', 'BTCUSD', 0, 0.50, leverage, inputQuantity, data_name)
        elif (symbol_pair == "ETHUSD"):
            id_name = 'bybit_ethusd_manual'
            conn.updateTradeValues(id_name, 'ETH', 'ETHUSD', 1, 0.05, leverage, inputQuantity, data_name)


        self.api = Bybit_Api()
        self.orders = Orders()
        self.sl = Stop_Loss()
        self.calc = Calc()

        self.inputOptions(symbol_pair)
        self.startMenu(symbol_pair, id_name)

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

    def startMenu(self, symbol_pair, id_name):
        flag = True
        input_quantity = conn.viewDbValue('trades', id_name, 'input_quantity')

        while(flag == True):

            print("")
            taskInput = input("Input Task: ")
            comms.timeStamp()

            if(taskInput == "exit"):
                self.shutdown()

            elif(taskInput == "price info"):
                self.api.priceInfo()

            elif(taskInput == "info"):
                print(self.api.symbolInfoResult())

            elif(taskInput == "long"):
                self.orders.createOrder("Buy", 'Limit', input)

            elif(taskInput == "short"):
                self.orders.createOrder("Sell", 'Limit', input_quantity)

            elif(taskInput == "long market"):
                self.orders.createOrder('Buy', 'Market', input_quantity)

            elif(taskInput == "short market"):
                self.orders.createOrder("Sell", 'Market', input_quantity)

            elif(taskInput == "wallet"):
                self.api.myWallet()

            elif(taskInput == "stoploss"):
                self.sl.changeStopLoss(500)
                print("Updated Stop Loss")

            elif(taskInput == "closesl"):
                self.orders.closePositionSl()

            elif(taskInput == "closem"):
                self.orders.closePositionMarket()

            elif(taskInput == "cancel"):
                self.api.cancelAllOrders()
                print("Orders Cancelled")

            elif(taskInput == "active"):
                print(self.orders.activeOrderCheck())

            elif(taskInput == "position"):
                print("Position: ")
                symbol.activePositionCheck()

            elif(taskInput == "test"):
                print(self.api.symbol_pair())

            elif(taskInput == "test1"):
                print(self.api.lastPrice())

            elif(taskInput == "test2"):
                print(self.api.closedProfitLoss())

            elif(taskInput == "change"):
                flag = False
                self.start()

            elif(taskInput == "update sl"):
                flag = False
                while(flag == False):
                    slAmountInput = input("Enter SL Amount:")
                    if slAmountInput.isnumeric():
                        flag = True
                        self.sl.changeStopLoss(slAmountInput)
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

