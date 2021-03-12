import sys
sys.path.append("..")
import database.database as db
import config
import bybit



class Bybit_Api():

    client = bybit.bybit(test=True, api_key=config.BYBIT_TESTNET_API_KEY,
                         api_secret=config.BYBIT_TESTNET_API_SECRET)

    symbol = None
    symbolPair = None
    keyInput = None

    def __init__(self, inputSymbol, inputSymbolPair):
        global symbol
        global symbolPair

        symbol = inputSymbol
        symbolPair = inputSymbolPair

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
    def getPosition(self):
        print("Getting Position...")
        position = self.client.Positions.Positions_myPosition(
            symbol=symbolPair).result()
        return position[0]['result']

    def getPositionSide(self):
        positionResult = self.getPosition()
        positionSide = positionResult['side']
        return positionSide

    def getPositionSize(self):
        positionResult = self.getPosition()
        positionResult = positionResult['size']
        return positionResult

