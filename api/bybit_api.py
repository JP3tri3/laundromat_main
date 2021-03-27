import sys
sys.path.append("..")
import database.database as db
import config
import bybit
import sql_connector as conn

class Bybit_Api():

    def __init__(self, trade_id_input):

        self.trade_id = trade_id_input
        self.client = bybit.bybit(test=True, api_key=config.BYBIT_TESTNET_API_KEY, api_secret=config.BYBIT_TESTNET_API_SECRET)
        self.symbol_pair = conn.viewDbValue('trades', self.trade_id, 'symbol_pair')
        self.key_input = conn.viewDbValue('trades', self.trade_id, 'key_input')

    def getKeyInput(self):
        return self.key_input

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
        print("Last Price: " + symbol_pair + " " + lastPrice)
        print("Mark Price: " + symbol_pair + " " + markPrice)
        print("Ask Price: " + symbol_pair + " " + askPrice)
        print("Index Price: " + symbol_pair + " " + indexPrice)
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
                print(f"sending order {side} {db.getSymbolPair()} {order_type} {stop_loss}")
                order = self.client.Order.Order_new(side=side, symbol=db.getSymbolPair(), order_type="Market",
                                            qty=inputQuantity, time_in_force="PostOnly", stop_loss=str(stop_loss), reduce_only=reduce_only).result()
            elif(order_type == "Limit"):
                print(f"sending order {price} - {side} {db.getSymbolPair()} {order_type} {stop_loss}")
                order = self.client.Order.Order_new(side=side, symbol=db.getSymbolPair(), order_type="Limit",
                                            qty=inputQuantity, price=price, time_in_force="PostOnly", stop_loss=str(stop_loss), reduce_only=reduce_only).result()
            else:
                print("Invalid Order")
        except Exception as e:
            print("an exception occured - {}".format(e))
            return False
        return order

    def changeOrderPrice(self, price):
        order = self.client.Order.Order_replace(symbol=db.getSymbolPair(), order_id=str(self.getOrderId()), p_r_price=str(price)).result()
        return order

#Leverage
 
    def getPositionLeverage(self):
        position = self.getPositionResult()
        return position['leverage']

    def setLeverage(self):
        setLeverage = self.client.Positions.Positions_saveLeverage(symbol=db.getSymbolPair(), leverage=str(db.getLeverage())).result()
        print("Leverage set to: " + str(db.getLeverage()))
        return setLeverage    
#stop_loss

    def changeStopLoss(self, slAmount):
        self.client.Positions.Positions_tradingStop(
            symbol=db.getSymbolPair(), stop_loss=str(slAmount)).result()

#Profit & Loss
    def closedProfitLoss(self):
        records = self.client.Positions.Positions_closePnlRecords(symbol=db.getSymbolPair()).result()
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