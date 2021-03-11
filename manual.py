import config
import orders
from time import time, sleep
import json
import time
import datetime
import bybit
import sys
import asyncio
from exchange.bybit_info import Bybit_Info
from orders import Orders

myTime = int(time.time() * 1000)
inputSymbol = ""

# client = bybit.bybit(test=True, api_key=config.BYBIT_TESTNET_API_KEY,
#                      api_secret=config.BYBIT_TESTNET_API_SECRET)


async def shutdown():
    print("")
    print("Shutting down...")
    sys.exit("Program Terminated")
    print("")


async def inputOptions(symbol):
    print("")
    print("TESTNET - Input Options:")
    print("")
    print("Symbol: " + symbol)
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
    print("Order Id: 'order id'")
    print("Update SL: 'update sl'")
    print("Exit: 'exit'")


async def main():
    global inputSymbol
    flag = True
    inputFlag = True
    print("")
    inputSymbol = ""

    while (inputFlag == True):
        inputSymbol = input("Enter Symbol: ").upper()
        if (inputSymbol == "BTCUSD") or (inputSymbol == "ETHUSD"):
            inputFlag = False
        else:
            print("Invalid Input, try 'BTCUSD' or 'ETHUSD'")

    # symbol = Bybit_Info(inputSymbol)
    symbol = Orders(inputSymbol)

    await inputOptions(inputSymbol)

    while(flag == True):

        print("")
        taskInput = input("Input Task: ")
        symbol.timeStamp()

        if(taskInput == "exit"):
            await shutdown()

        elif(taskInput == "price info"):
            symbol.priceInfo()

        elif(taskInput == "info"):
            symbol.btcInfo()

        elif(taskInput == "long"):
            symbol.createOrder("Buy", inputSymbol, "Limit")

        elif(taskInput == "short"):
            symbol.createOrder("Sell", inputSymbol, "Limit")

        elif(taskInput == "long market"):
            symbol.createOrder("Buy", inputSymbol, "Market")

        elif(taskInput == "short market"):
            symbol.createOrder("Sell", inputSymbol, "Market")

        elif(taskInput == "wallet"):
            symbol.myWallet()

        elif(taskInput == "active"):
            print(symbol.activeOrderCheck())

        elif(taskInput == "stoploss"):
            orders.changeStopLoss(500)
            print("Updated Stop Loss")

        elif(taskInput == "closesl"):
            symbol.closePositionSl()

        elif(taskInput == "closem"):
            symbol.closePositionMarket()

        elif(taskInput == "cancel"):
            symbol.cancelAllOrders()
            print("Orders Cancelled")

        elif(taskInput == "order id"):
            print("Order ID: ")
            symbol.returnOrderID()

        elif(taskInput == "position"):
            print("Position: ")
            symbol.activePositionCheck()

        elif(taskInput == "atr"):
            symbol.inputAtr()

        elif(taskInput == "test"):
            print(symbol.printLimit())

        elif(taskInput == "symbol"):
            print(symbol.getSymbol())

        elif(taskInput == "side"):
            print(symbol.getSide())

        elif(taskInput == "changesymbol"):
            symbol.setInitialValues()

        elif(taskInput == "update sl"):
            flag = False
            while(flag == False):
                slAmountInput = input("Enter SL Amount:")
                if slAmountInput.isnumeric():
                    flag = True
                    orders.changeStopLoss(slAmountInput)
                else:
                    print("Invalid Entry...")

        else:
            print("Invalid Input, try again...")
            await inputOptions()


# def priceTest():
#     while(flag == True):
#         timeStamp()
#         info = client.Market.Market_symbolInfo().result()
#         keys = info[0]['result']
#         btcInfo = keys[0]['last_price']
#         print(btcInfo)
#         sleep(1)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
