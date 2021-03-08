import bybit
import config
import comms
import json
import time
import datetime

client = bybit.bybit(test=True, api_key=config.BYBIT_TESTNET_API_KEY,
                     api_secret=config.BYBIT_TESTNET_API_SECRET)

orderId = ""
orderPrice = 0
margin = 5.0
inputQuantity = 100 * margin
entry_price = 0.0
stop_loss = 0
level = entry_price
symbol = "BTCUSD"
side = ""
percentLevel = 0.0


def setInitialValues(inputSymbol):
    global side
    position = client.Positions.Positions_myPosition(
        symbol=inputSymbol).result()
    positionResult = position[0]['result']
    side = positionResult['side']


setInitialValues(symbol)


# info = client.Market.Market_symbolInfo().result()
# keys = info[0]['result']

# btcOrderBookInfo = client.Market.Market_orderbook(symbol="BTCUSD").result()

# inverse perpetual keys
# btcInfo = keys[0]
# ethInfo = keys[1]
# eosInfo = keys[2]
# xrpInfo = keys[3]

# # usdt perpetual keys
# btcusdtInfo = keys[4]
# ethusdtInfo = keys[5]
# ltcusdtInfo = keys[6]
# linkusdtInfo = keys[7]
# xtzusdtInfo = keys[8]

# # Price Information:
# ethLastPrice = ethInfo['last_price']


# eth Balance in USD
# myEthBalanceUSD = float(ethLastPrice) * myEthBalance

# Wallet Balances:

def btcWallet():
    myBtcWallet = client.Wallet.Wallet_getBalance(coin="BTC").result()
    myBtcBalance = myBtcWallet[0]['result']['BTC']['available_balance']
    print(myBtcBalance)


def ethWallet():
    myEthWallet = client.Wallet.Wallet_getBalance(coin="ETH").result()
    myEthBalance = myEthWallet[0]['result']['ETH']['available_balance']
    print(myEthBalance)

# BTC Info:


def getSymbol():
    return symbol


def getSide():
    return side


def btcPriceInfo():
    info = client.Market.Market_symbolInfo().result()
    keys = info[0]['result']
    btcInfo = keys[0]

    btcLastPrice = btcInfo['last_price']
    btcMarkPrice = btcInfo['mark_price']
    btcAskPrice = btcInfo['ask_price']
    btcIndexPrice = btcInfo['index_price']

    print("")
    print("Last Price: " + btcLastPrice)
    print("Mark Price: " + btcMarkPrice)
    print("Ask Price: " + btcAskPrice)
    print("Index Price: " + btcIndexPrice)
    print("")


def btcLastPrice():
    info = client.Market.Market_symbolInfo().result()
    keys = info[0]['result']
    btcInfo = keys[0]['last_price']
    return float(btcInfo)


def btcInfo():
    info = client.Market.Market_symbolInfo().result()
    keys = info[0]['result']
    btcInfo = keys[0]
    print(btcInfo)

# Order Functions


def cancelAllOrders():
    client.Order.Order_cancelAll(symbol=symbol).result()


def timeStamp():
    ct = datetime.datetime.now()
    print("Time: ", ct)


def myPosition():
    position = client.Positions.Positions_myPosition(symbol=symbol).result()
    print(position)


def returnOrderID():
    print(orderId)


# Active Checks

def activeOrderCheck():
    global orderId
    activeOrder = client.Order.Order_query(symbol=symbol).result()
    order = activeOrder[0]['result']
    if (order == []):
        print("no pending orders")
        return 0
    else:
        orderId = order[0]['order_id']
        return 1


def activePositionTest(symbol):
    position = client.Positions.Positions_myPosition(symbol=symbol).result()
    positionResult = position[0]['result']
    positionSide = positionResult['side']
    positionSymbol = positionResult['symbol']
    print(positionSide)
    print(positionSymbol)


def activePositionCheck():
    try:
        position = client.Positions.Positions_myPosition(
            symbol="BTCUSD").result()
        positionResult = position[0]['result']
        positionValue = positionResult['position_value']
        if(positionValue != "0"):
            return 1
        else:
            return 0
    except Exception as e:
        print("Active Position Check Exception Occured...")
        print("Trying again...")
        time.sleep(2)
        activePositionCheck()


def getPositionSize():
    position = client.Positions.Positions_myPosition(symbol=symbol).result()
    positionResult = position[0]['result']
    return positionResult['size']

# traceback test


def printActivePosition():
    position = client.Positions.Positions_myPosition(symbol=symbol).result()
    positionResult = position[0]['result']
    positionValue = positionResult['position_value']
    return(positionValue)


def printActivePositionResult():
    position = client.Positions.Positions_myPosition(symbol=symbol).result()
    positionResult = position[0]['result']
    positionValue = positionResult['position_value']
    return(positionResult)


def activePositionEntryPrice():
    position = client.Positions.Positions_myPosition(symbol=symbol).result()
    positionResult = position[0]['result']
    positionEntryPrice = positionResult['entry_price']
    return float(positionEntryPrice)

# Create Functions:


def inputAtr():
    global atr
    flag = False
    print("")
    while(flag == False):
        atr = input("Input ATR: ")
        if(atr.isnumeric()):
            print("ATR input accepted for SL: " + str(atr))
            flag = True
        else:
            print("Invalid Input, try again...")


def placeOrder(order_type, price):
    global orderId

    if(side == "Buy"):
        stop_loss = btcLastPrice() - float(calculateOnePercentLessEntry())
    else:
        stop_loss = btcLastPrice() + float(calculateOnePercentLessEntry())
    print("Initial Stop Loss: " + str(stop_loss))
    try:
        print(
            f"sending order {price} - {side} {symbol} {order_type} {stop_loss}")
        order = client.Order.Order_new(side=side, symbol=symbol, order_type=order_type,
                                       qty=inputQuantity, price=price, time_in_force="PostOnly", stop_loss=str(stop_loss)).result()
        orderId = str(order[0]['result']['order_id'])
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False
    return order


def changeOrderPrice(price, orderId):
    global orderPrice
    if (price != orderPrice):
        client.Order.Order_replace(
            symbol=symbol, order_id=orderId, p_r_price=str(price)).result()
        timeStamp()
        print("Updating Order Price")


def forceOrder(orderId):
    flag = False
    currentPrice = btcLastPrice()
    price = limitPriceDifference()

    while(flag == False):
        if (activeOrderCheck() == 1):
            if (btcLastPrice() != currentPrice) and (btcLastPrice() != price):
                print("btcLastPrice: " + str(btcLastPrice()))
                print("currentPrice: " + str(currentPrice))
                print("price: " + str(price))
                currentPrice = btcLastPrice()
                price = limitPriceDifference()
                changeOrderPrice(price, orderId)
                print("Order Price Updated: " + str(price))
                print("")
            time.sleep(2)
        else:
            flag = True


def createOrder(sideInput, symbolInput, order_type):
    global orderPrice
    global entry_price
    global level
    global side
    global symbol
    global percentLevel

    percentLevel = 0.0
    symbol = symbolInput
    side = sideInput
    flag = False
    entry_price = limitPriceDifference()

    while(flag == False):
        if ((activeOrderCheck() == 0) and (activePositionCheck() == 0)):
            print("Attempting to place order...")
            placeOrder(order_type=order_type, price=limitPriceDifference())
            orderPrice = limitPriceDifference
        else:
            forceOrder(orderId)
            print("")
            print("Confirming Order...")
            if ((activeOrderCheck() == 0) and (activePositionCheck() == 0)):
                print("Order Failed")
            else:
                entry_price = float(activePositionEntryPrice())
                level = entry_price
                print("Entry Price: " + str(entry_price))
                print("Order Successful")
                flag = True

    updateStopLoss()
    print("Entry Price: " + str(entry_price))
    print("Exit Price: " + str(stop_loss))
    print("Percent Level: " + str(percentLevel))
    comms.logClosingDetails(entry_price, level, percentLevel, stop_loss, side)
    comms.updateData("vwap", "1min", 0)

# Close & Stoploss


def limitPriceDifference():
    if(side == "Buy"):
        limitPriceDifference = btcLastPrice() - 0.50
    else:
        limitPriceDifference = btcLastPrice() + 0.50
    return limitPriceDifference


def updateStopLoss():
    flag = True

    while (flag == True):
        if(activePositionCheck() == 1):
            if(side == "Buy"):
                if(btcLastPrice() > level):
                    calculateStopLoss()
                    time.sleep(4)
                else:
                    print("Waiting...")
                    print("Percent Gained: " + str(calculatePercentGained()))
                    print("Level: " + str(level))
                    print("BTC Price: " + str(btcLastPrice()))
                    print("")
                    time.sleep(4)
            else:
                if(btcLastPrice() < level):
                    calculateStopLoss()
                    time.sleep(4)
                else:
                    print("Waiting...")
                    print("Percent Gained: " + str(calculatePercentGained()))
                    print("Level: " + str(level))
                    print("BTC Price: " + str(btcLastPrice()))
                    print("")
                    time.sleep(4)
        else:
            print("Position Closed")
            print("")
            flag = False


def changeStopLoss(slAmount):
    client.Positions.Positions_tradingStop(
        symbol=symbol, stop_loss=str(slAmount)).result()
    print("")
    print("Changed stop Loss to: " + str(stop_loss))


def closePositionSl():
    flag = True
    stopLossInputPrice = btcLastPrice()
    print("Forcing Close")
    changeStopLoss(btcLastPrice() - float(2))
    time.sleep(5)

    while(flag == True):
        if(activePositionCheck() == 1):
            if (btcLastPrice() > stopLossInputPrice):
                stopLossInputPrice = btcLastPrice()
                print("")
                print("Forcing Close")
                timeStamp()
                changeStopLoss(btcLastPrice() - float(2))
                time.sleep(5)
        else:
            print("Position Closed")
            flag = False


def closePositionMarket():
    positionSize = getPositionSize()

    if(side == "Sell"):
        client.Order.Order_new(side="Buy", symbol=symbol, order_type="Market",
                               qty=positionSize, time_in_force="GoodTillCancel").result()
    else:
        client.Order.Order_new(side="Sell", symbol=symbol, order_type="Market",
                               qty=positionSize, time_in_force="GoodTillCancel").result()

    if (activePositionCheck() == 1):
        print("Error Closing Position")
    else:
        print("Position Closed at: " + str(btcLastPrice()))


def calculateOnePercentLessEntry():
    onePercentDifference = (float(entry_price) * 0.01) / margin
    return onePercentDifference


def calculatePercentGained():
    if(side == "Buy"):
        difference = (btcLastPrice() - float(entry_price))
    else:
        difference = (float(entry_price) - btcLastPrice())

    percent = (difference/btcLastPrice()) * 100
    percentWithMargin = (percent) * margin
    return float(percentWithMargin)


def calculateStopLoss():
    global level
    global stop_loss
    global percentLevel
    processTrigger = percentLevel
    percentGained = calculatePercentGained()

    print("calculating Stop Loss:")

    if (percentLevel < 0.25):
        if (side == "Buy"):
            stop_loss = (entry_price - calculateOnePercentLessEntry())
        else:
            stop_loss = (entry_price + calculateOnePercentLessEntry())
        percentLevel = 0.25
    elif (percentGained >= 0.25) and (percentLevel >= 0.25) and (percentLevel < 0.5):
        stop_loss = entry_price
        percentLevel = 0.5
        level = btcLastPrice()
    elif (percentGained >= 0.5) and (percentLevel < 0.75):
        stop_loss = level
        percentLevel = 0.75
        level = btcLastPrice()
    elif (percentGained >= 0.75) and (percentLevel < 1.0):
        stop_loss = level
        percentLevel = 1.0
        level = btcLastPrice()
    elif (percentGained > (percentLevel + 0.5)):
        stop_loss = level
        percentLevel += 0.5
        level = btcLastPrice()

    if (processTrigger != percentLevel):
        print("Changing Stop Loss")
        changeStopLoss(stop_loss)
        print("Percent Gained: " + str(percentGained))
        print("Percent Level: " + str(percentLevel))
        print("Level: " + str(level))
        print("Stop Loss: " + str(stop_loss))
        print("")
        processTrigger = percentLevel

# def calculateStopLoss50():
#     global level
#     global stop_loss
#     global percentLevel
#     processTrigger = percentLevel
#     percentGained = calculatePercentGained()

#     print("calculating Stop Loss:")

#     if (percentLevel < 0.50):
#         if (side == "Buy"):
#             stop_loss = (entry_price - calculateOnePercentLessEntry())
#         else:
#             stop_loss = (entry_price + calculateOnePercentLessEntry())
#         percentLevel = 0.50
#         print("Percent Gained: " + str(percentGained))
#         print("Percent Level: " + str(percentLevel))
#         print("Level: " + str(level))
#         print("Stop Loss: " + str(stop_loss))
#         print("")
#     elif (percentGained >= 0.5) and (percentLevel >= 0.5) and (percentLevel < 1.0):
#         stop_loss = entry_price
#         percentLevel = 1
#         level = btcLastPrice()
#         print("Percent Gained: " + str(percentGained))
#         print("Percent Level: " + str(percentLevel))
#         print("Level: " + str(level))
#         print("Stop Loss: " + str(stop_loss))
#         print("")
#     elif (percentGained > (percentLevel + 1.0)):
#         stop_loss = level
#         percentLevel += 0.5
#         level = btcLastPrice()
#         print("Percent Gained: " + str(percentGained))
#         print("Percent Level: " + str(percentLevel))
#         print("Level: " + str(level))
#         print("Stop Loss: " + str(stop_loss))
#         print("")

#     if (processTrigger != percentLevel):
#         print("Changing Stop Loss")
#         print(str(stop_loss))
#         changeStopLoss(stop_loss)
