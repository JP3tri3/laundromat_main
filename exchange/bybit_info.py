import bybit
import config


class Bybit_Info:

    symbol = ""
    pairSymbol = ""
    keyInput = 0
    client = bybit.bybit(test=True, api_key=config.BYBIT_TESTNET_API_KEY,
                         api_secret=config.BYBIT_TESTNET_API_SECRET)

    def __init__(self, inputSymbol):
        self.inputSymbol = inputSymbol
        global pairSymbol
        global keyInput
        global symbol

        pairSymbol = inputSymbol

        if (inputSymbol == "BTCUSD"):
            self.keyInput = 0
            self.symbol = "BTC"
        elif (inputSymbol == "ETHUSD"):
            self.keyInput = 1
            self.symbol = "ETH"

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
