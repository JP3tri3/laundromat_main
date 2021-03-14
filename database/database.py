import bybit
import config

client = bybit.bybit(test=True, api_key=config.BYBIT_TESTNET_API_KEY,
                     api_secret=config.BYBIT_TESTNET_API_SECRET)


symbol = None
symbolPair = None
keyInput = None
limitPriceDifference = None
margin = None

def setInitialValues(symbolInput, symbolPairInput, marginInput, inputKeyInput, limitPriceDifferenceInput):
    global symbol
    global symbolPair
    global keyInput
    global limitPriceDifference
    global margin

    symbol = symbolInput
    symbolPair = symbolPairInput
    keyInput = inputKeyInput
    limitPriceDifference = limitPriceDifferenceInput
    margin = marginInput

def getSymbol():
    return symbol

def getKeyInput():
    return keyInput

def getSymbolPair():
    return symbolPair

def getLimitPriceDifference():
    return limitPriceDifference

