import sys
sys.path.append("..")
from database.database import Database
import config
import bybit

class Bybit_Api():

    def __init__(self):

        self.db = Database()
        self.client = bybit.bybit(test=True, api_key=config.BYBIT_TESTNET_API_KEY, api_secret=config.BYBIT_TESTNET_API_SECRET)
        self.trades_kv_dict = self.db.get_trade_values()
        self.symbol_pair = self.trades_kv_dict['symbol_pair']
        self.key_input = self.trades_kv_dict['key_input']
        self.symbol = self.trades_kv_dict['symbol']
        self.leverage = self.trades_kv_dict['leverage']

    def getKeyInput(self):
        return self.key_input

    def myWallet(self):
        myWallet = self.client.Wallet.Wallet_getBalance(
            coin=db.getSymbol()).result()
        myBalance = myWallet[0]['result'][db.getSymbol()]['available_balance']
        print(myBalance)

#symbol:

    def symbolInfoResult(self):
        info = self.client.Market.Market_symbolInfo().result()
        return(info[0]['result'])

    def symbolInfoKeys(self):
        infoKeys = self.symbolInfoResult()
        return infoKeys[db.keyInput]

#price:

    def priceInfo(self):
        keys = self.symbolInfoResult()
        keyInfo = keys[self.key_input]

        lastPrice = keyInfo['last_price']
        markPrice = keyInfo['mark_price']
        askPrice = keyInfo['ask_price']
        indexPrice = keyInfo['index_price']

        print("")
        print("Last Price: " + self.symbol_pair + " " + lastPrice)
        print("Mark Price: " + self.symbol_pair + " " + markPrice)
        print("Ask Price: " + self.symbol_pair + " " + askPrice)
        print("Index Price: " + self.symbol_pair + " " + indexPrice)
        print("")

    def lastPrice(self):
        keys = self.symbolInfoResult()
        return float(keys[self.key_input]['last_price'])

#order:
    def getOrder(self):
        activeOrder = self.client.Order.Order_query(symbol=self.symbol_pair).result()
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
        self.client.Order.Order_cancelAll(symbol=self.symbol).result()


#position:
    def getPositionResult(self):
        positionResult = self.client.Positions.Positions_myPosition(
            symbol=self.symbol_pair).result()
        return positionResult[0]['result']

    def getPositionSide(self):
        try:
            positionResult = self.getPositionResult()
            return positionResult['side']
        except Exception as e:
            print("an exception occured - {}".format(e))   
            return 'null'     

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
    def placeOrder(self, price, order_type, side, inputQuantity, stop_loss, reduce_only):

        try:
            if(order_type == 'Market'):
                print(f"sending order {side} {self.symbol_pair} {order_type} {stop_loss}")
                order = self.client.Order.Order_new(side=side, symbol=self.symbol_pair, order_type="Market",
                                            qty=inputQuantity, time_in_force="PostOnly", stop_loss=str(stop_loss), reduce_only=reduce_only).result()
            elif(order_type == "Limit"):
                print(f"sending order {price} - {side} {self.symbol_pair} {order_type} {stop_loss}")
                order = self.client.Order.Order_new(side=side, symbol=self.symbol_pair, order_type="Limit",
                                            qty=inputQuantity, price=price, time_in_force="PostOnly", stop_loss=str(stop_loss), reduce_only=reduce_only).result()
            else:
                print("Invalid Order")
        except Exception as e:
            print("an exception occured - {}".format(e))
            return False
        return order

    def changeOrderPrice(self, price):
        order = self.client.Order.Order_replace(symbol=self.symbol_pair, order_id=str(self.getOrderId()), p_r_price=str(price)).result()
        return order

#Leverage
 
    def getPositionLeverage(self):
        position = self.getPositionResult()
        return position['leverage']

    def setLeverage(self):
        setLeverage = self.client.Positions.Positions_saveLeverage(symbol=self.symbol_pair, leverage=str(self.leverage)).result()
        print("Leverage set to: " + str(self.leverage))
        return setLeverage    
#stop_loss

    def changeStopLoss(self, slAmount):
        self.client.Positions.Positions_tradingStop(
            symbol=self.symbol_pair, stop_loss=str(slAmount)).result()

#Profit & Loss
    def closedProfitLoss(self):
        records = self.client.Positions.Positions_closePnlRecords(symbol=self.symbol_pair).result()
        return records[0]['result']['data']

    def closedProfitLossQuantity(self, index):
        recordResults = self.closedProfitLoss()
        return recordResults[index]['closed_size']

    def lastProfitLoss(self, index):
        recordResult = self.closedProfitLoss()
        return recordResult[index]['closed_pnl']

    def lastExitPrice(self, index):
        recordResult = self.closedProfitLoss()
        return recordResult[index]['avg_exit_price']

    def lastEntryPrice(self, index):
        recordResult = self.closedProfitLoss()
        return recordResult[index]['avg_entry_price']