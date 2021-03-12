import bybit
import config
import database


class Bybit_Info:

    symbol = ""
    pairSymbol = ""
    keyInput = 0
    limitPriceDifference = 0.0
    # Call Client

    def __init__(self, inputSymbol):
        self.inputSymbol = inputSymbol
        global pairSymbol
        global keyInput
        global symbol
        global limitPriceDifference

        pairSymbol = inputSymbol


    def getSymbol(self):
        return self.inputSymbol

    def priceInfo(self):

        info = self.client.Market.Market_symbolInfo().result()
        keys = info[0]['result']
        keyInfo = keys[self.keyInput]

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

    def myWallet(self):
        myWallet = self.client.Wallet.Wallet_getBalance(
            coin=self.symbol).result()
        myBalance = myWallet[0]['result'][self.symbol]['available_balance']
        print(myBalance)

    def lastPrice(self):
        info = self.client.Market.Market_symbolInfo().result()
        keys = info[0]['result']
        symbolInfo = keys[self.keyInput]['last_price']
        return float(symbolInfo)

    def symbolInfo():
        info = self.client.Market.Market_symbolInfo().result()
        keys = info[0]['result']
        info = keys[self.keyInput]
        print(info)
