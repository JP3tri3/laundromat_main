import sys
sys.path.append("..")
import database.database as db
import controller.comms as comms
from api.bybit_api import Bybit_Api
from model.orders import Orders
from model.stop_loss import Stop_Loss
from model.calc import Calc

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
            symbolPair = input("Enter Symbol: ").upper()
            if (symbolPair == "BTCUSD") or (symbolPair == "ETHUSD"):
                flag = False
            else:
                print("Invalid Input, try 'BTCUSD' or 'ETHUSD'")

        if (symbolPair == "BTCUSD"):
            db.setInitialValues('BTC', symbolPair, leverage, 0, 0.50, inputQuantity, data_name)
        elif (symbolPair == "ETHUSD"):
            db.setInitialValues('ETH', symbolPair, leverage, 1, 0.05, inputQuantity, data_name)

        self.api = Bybit_Api()
        self.orders = Orders()
        self.sl = Stop_Loss()
        self.calc = Calc()

        self.inputOptions(symbolPair)
        self.startMenu(symbolPair)

    def inputOptions(self, symbolPair):
        print("")
        print("TESTNET - Input Options:")
        print("")
        print("Symbol: " + symbolPair)
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

    def startMenu(self, symbolPair):
        flag = True

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
                self.orders.createOrder("Buy", 'Limit', db.getInputQuantity())

            elif(taskInput == "short"):
                self.orders.createOrder("Sell", 'Limit', db.getInputQuantity())

            elif(taskInput == "long market"):
                self.orders.createOrder('Buy', 'Market', db.getInputQuantity())

            elif(taskInput == "short market"):
                self.orders.createOrder("Sell", 'Market', db.getInputQuantity())

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
                print(self.api.getSymbolPair())

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
                self.inputOptions(symbolPair)

    def shutdown(self):
        print("")
        print("Shutting down...")
        sys.exit("Program Terminated")
        print("")

