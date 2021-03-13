import sys
sys.path.append("..")
import database.database as db
import config
import bybit



class Bybit_Api():

    client = bybit.bybit(test=True, api_key=config.BYBIT_TESTNET_API_KEY,
                         api_secret=config.BYBIT_TESTNET_API_SECRET)

    def __init__(self, inputSymbolPair):
        global symbol
        global symbolPair

        symbolPair = inputSymbolPair

        if  (symbolPair == "BTCUSD"):
            symbol = 'BTC'            
        elif (symbolPair == "ETHUSD"):
            symbol = "ETH"

    symbol = None
    symbolPair = None
    keyInput = None

    def myWallet(self):
        myWallet = self.client.Wallet.Wallet_getBalance(
            coin=self.symbol).result()
        myBalance = myWallet[0]['result'][self.symbol]['available_balance']
        print(myBalance)

#symbol:
    def getSymbolPair(self):
        return symbolPair

    def lastPrice(self):
        info = self.client.Market.Market_symbolInfo().result()
        keys = info[0]['result']
        symbolInfo = keys[db.keyInput]['last_price']
        return float(symbolInfo)

#order:
    def getOrder(self):
        print("Retrieving Order...")
        activeOrder = self.client.Order.Order_query(symbol=symbolPair).result()
        order = activeOrder[0]['result']
        return(order)

    def getOrderId(self):
        print("Retrieving Order ID...")
        order = self.getOrder()
        orderId = order[0]['order_id']
        print("Order ID: " + str(orderId))
        return orderId

    def cancelAllOrders(self):
        print("Cancelling All Orders...")
        self.client.Order.Order_cancelAll(symbol=symbol).result()


#position:
    def getPositionResult(self):
        print("Getting Position...")
        positionResult = self.client.Positions.Positions_myPosition(
            symbol=self.symbolPair).result()
        return positionResult[0]['result']

    def getPositionSide(self):
        positionResult = self.getPosition()
        return positionResult['side']

    def getPositionSize(self):
        positionResult = self.getPosition()
        return positionResult['size']

    def getPositionValue(self):
        positionResult = self.getPositionResult()
        return positionResult['position_value']

    def getActivatePositionEntryPrice(self):
        positionResult = self.getPositionResult()
        return float(positionResult['entry_price'])

#trades:
    def placeOrder(self, price, side, order_type, inputQuantity, stop_loss):
        try:
            print(f"sending order {price} - {side} {symbolPair} {order_type} {stop_loss}")
            order = self.client.Order.Order_new(side=side, symbol=symbolPair, order_type=order_type,
                                        qty=inputQuantity, price=price, time_in_force="PostOnly", stop_loss=str(stop_loss)).result()
        except Exception as e:
            print("an exception occured - {}".format(e))
            return False
        return order   

#stop_loss

    def changeStopLoss(self, slAmount):
        client.Positions.Positions_tradingStop(
            symbol=symbol, stop_loss=str(slAmount)).result()
        print("")
        print("Changed stop Loss to: " + str(slAmount))

