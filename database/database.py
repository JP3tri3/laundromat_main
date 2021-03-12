import bybit
import config

client = bybit.bybit(test=True, api_key=config.BYBIT_TESTNET_API_KEY,
                     api_secret=config.BYBIT_TESTNET_API_SECRET)


symbol = None
symbolPair = None
keyInput = None
limitPriceDifference = None


def setInitialValues(inputSymbol, inputSymbolPair, inputKeyInput, inputLimitPriceDifference):
    global symbol
    global symbolPair
    global keyInput
    global limitPriceDifference

    symbol = inputSymbol
    symbolPair = inputSymbolPair
    keyInput = inputKeyInput
    limitPriceDifference = inputLimitPriceDifference

def getSymbol():
    return symbol

def getSymbolPair():
    return symbolPair

def getLimitPriceDifference():
    return limitPriceDifference

