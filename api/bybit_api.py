import sys
sys.path.append("..")
import database.database as db
import config
import bybit



class Bybit_Api():

    client = bybit.bybit(test=True, api_key=config.BYBIT_TESTNET_API_KEY,
                         api_secret=config.BYBIT_TESTNET_API_SECRET)

    # def __init__(self):
    #     return


    def getKeyInput(self):
        return db.getKeyInput()

    def myWallet(self):
        myWallet = self.client.Wallet.Wallet_getBalance(
            coin=db.getSymbol()).result()
        myBalance = myWallet[0]['result'][db.getSymbol()]['available_balance']
        print(myBalance)

#symbol:
    def getSymbolPair(self):
        return db.getSymbolPair()

    def symbolInfoResult(self):
        info = self.client.Market.Market_symbolInfo().result()
        return(info[0]['result'])

    def symbolInfoKeys(self):
        infoKeys = self.symbolInfoResult()
        return infoKeys[db.keyInput]

#price:

    def priceInfo(self):
        keys = self.symbolInfoResult()
        keyInfo = keys[db.getKeyInput()]

        lastPrice = keyInfo['last_price']
        markPrice = keyInfo['mark_price']
        askPrice = keyInfo['ask_price']
        indexPrice = keyInfo['index_price']

        print("")
        print("Last Price: " + pairSymbol + " " + lastPrice)
        print("Mark Price: " + pairSymbol + " " + markPrice)
        print("Ask Price: " + pairSymbol + " " + askPrice)
        print("Index Price: " + pairSymbol + " " + indexPrice)
        print("")

    def lastPrice(self):
        keys = self.symbolInfoResult()
        return float(keys[db.getKeyInput()]['last_price'])

#order:
    def getOrder(self):
        activeOrder = self.client.Order.Order_query(symbol=db.getSymbolPair()).result()
        order = activeOrder[0]['result']
        return(order)

    def getOrderId(self):
        try:
            order = self.getOrder()
            orderId = order[0]['order_id']
        except Exception as e:
            print("an exception occured - {}".format(e))
            return False
        return orderId

    def cancelAllOrders(self):
        print("Cancelling All Orders...")
        self.client.Order.Order_cancelAll(symbol=symbol).result()


#position:
    def getPositionResult(self):
        positionResult = self.client.Positions.Positions_myPosition(
            symbol=db.getSymbolPair()).result()
        return positionResult[0]['result']

    def getPositionSide(self):
        positionResult = self.getPositionResult()
        return positionResult['side']

    def getPositionSize(self):
        positionResult = self.getPositionResult()
        return positionResult['size']

    def getPositionValue(self):
        positionResult = self.getPositionResult()
        return positionResult['position_value']

    def getActivePositionEntryPrice(self):
        positionResult = self.getPositionResult()
        return float(positionResult['entry_price'])

#orders:
    def placeOrder(self, price, order_type, side, inputQuantity, stop_loss):

        try:
            if(order_type == 'Market'):
                print(f"sending order {side} {db.getSymbolPair()} {order_type} {stop_loss}")
                order = self.client.Order.Order_new(side=side, symbol=db.getSymbolPair(), order_type="Market",
                                            qty=inputQuantity, time_in_force="PostOnly", stop_loss=str(stop_loss)).result()
            elif(order_type == "Limit"):
                print(f"sending order {price} - {side} {db.getSymbolPair()} {order_type} {stop_loss}")
                order = self.client.Order.Order_new(side=side, symbol=db.getSymbolPair(), order_type="Limit",
                                            qty=inputQuantity, price=price, time_in_force="PostOnly", stop_loss=str(stop_loss)).result()
            else:
                print("Invalid Order")
        except Exception as e:
            print("an exception occured - {}".format(e))
            return False
        return order

    def changeOrderPrice(self, price):
        order = self.client.Order.Order_replace(symbol=db.getSymbolPair(), order_id=self.getOrderId(), p_r_price=str(price)).result()
        return order


#stop_loss

    def changeStopLoss(self, slAmount):
        self.client.Positions.Positions_tradingStop(
            symbol=db.getSymbolPair(), stop_loss=str(slAmount)).result()
        print("")
        print("Changed stop Loss to: " + str(slAmount))

