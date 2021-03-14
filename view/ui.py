import sys
sys.path.append("..")
import database.database as db
import controller.comms as commms
from api.bybit_api import Bybit_Api
from model.orders import Orders
from model.stop_loss import Stop_Loss

class Ui:

    # def __init__(self):
    #     return

    def start(self):
        flag = True

        #manual Setters:
        margin = 5

        while (flag == True):
            symbolPair = input("Enter Symbol: ").upper()
            if (symbolPair == "BTCUSD") or (symbolPair == "ETHUSD"):
                flag = False
            else:
                print("Invalid Input, try 'BTCUSD' or 'ETHUSD'")

        if (symbolPair == "BTCUSD"):
            db.setInitialValues('BTC', symbolPair, margin, 0, 0.50)
        elif (symbolPair == "ETHUSD"):
            db.setInitialValues('ETH', symbolPair, margin, 1, 0.05)

        self.api = Bybit_Api()
        self.orders = Orders()
        self.sl = Stop_Loss()

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
            commms.timeStamp()

            if(taskInput == "exit"):
                self.shutdown()

            elif(taskInput == "price info"):
                self.api.priceInfo()

            elif(taskInput == "info"):
                self.api.symbolInfoResult()

            elif(taskInput == "long"):
                self.orders.createOrder("Buy", symbolPair, "Limit")

            elif(taskInput == "short"):
                self.orders.createOrder("Sell", symbolPair, "Limit")

            elif(taskInput == "long market"):
                self.orders.createOrder("Buy", symbolPair, "Market")

            elif(taskInput == "short market"):
                self.orders.createOrder("Sell", symbolPair, "Market")

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
                self.orders.createOrder("Buy", "Limit", 100, 100)

            elif(taskInput == "test1"):
                print(self.api.getOrderId())           

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
