import config
import bybit_info
from time import time, sleep
import json
import time
import datetime
import bybit
import sys
import asyncio

myTime = int(time.time() * 1000)

client = bybit.bybit(test=True, api_key=config.BYBIT_TESTNET_API_KEY,
                     api_secret=config.BYBIT_TESTNET_API_SECRET)

flag = True


async def shutdown():
    print("")
    print("Shutting down...")
    sys.exit("Program Terminated")
    print("")


async def inputOptions():
    print("")
    print("TESTNET - Input Options:")
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
    print("BTC Price info: 'btc price'")
    print("BTC Info: 'btc info'")
    print("BTC Wallet: 'btc wallet'")
    print("Eth Wallet: 'eth wallet'")
    print("Active Orders: 'active'")
    print("Position: 'position'")
    print("Order Id: 'order id'")
    print("Update SL: 'update sl'")
    print("Exit: 'exit'")


async def main():
    global flag

    print("")

    await inputOptions()

    while(flag == True):

        print("")
        taskInput = input("Input Task: ")
        bybit_info.timeStamp()

        if(taskInput == "exit"):
            await shutdown()

        elif(taskInput == "btc price"):
            bybit_info.btcPriceInfo()

        elif(taskInput == "btc info"):
            bybit_info.btcInfo()

        elif(taskInput == "long"):
            bybit_info.createOrder("Buy", "BTCUSD", "Limit")

        elif(taskInput == "short"):
            bybit_info.createOrder("Sell", "BTCUSD", "Limit")

        elif(taskInput == "long market"):
            bybit_info.createOrder("Buy", "BTCUSD", "Market")

        elif(taskInput == "short market"):
            bybit_info.createOrder("Sell", "BTCUSD", "Market")

        elif(taskInput == "btc wallet"):
            bybit_info.btcWallet()

        elif(taskInput == "eth wallet"):
            bybit_info.ethWallet()

        elif(taskInput == "active"):
            print(bybit_info.activeOrderCheck())

        elif(taskInput == "stoploss"):
            bybit_info.changeStopLoss(500)
            print("Updated Stop Loss")

        elif(taskInput == "closesl"):
            bybit_info.closePositionSl()

        elif(taskInput == "closem"):
            bybit_info.closePositionMarket()

        elif(taskInput == "cancel"):
            bybit_info.cancelAllOrders()
            print("Orders Cancelled")

        elif(taskInput == "order id"):
            print("Order ID: ")
            bybit_info.returnOrderID()

        elif(taskInput == "position"):
            print("Position: ")
            bybit_info.activePositionCheck()

        elif(taskInput == "atr"):
            bybit_info.inputAtr()

        elif(taskInput == "test"):
            print(bybit_info.getPositionSize())

        elif(taskInput == "symbol"):
            print(bybit_info.getSymbol())

        elif(taskInput == "side"):
            print(bybit_info.getSide())

        elif(taskInput == "changesymbol"):
            bybit_info.setInitialValues()

        elif(taskInput == "update sl"):
            flag = False
            while(flag == False):
                slAmountInput = input("Enter SL Amount:")
                if slAmountInput.isnumeric():
                    flag = True
                    bybit_info.changeStopLoss(slAmountInput)
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
