import bybit
import config

client = bybit.bybit(test=True, api_key=config.BYBIT_TESTNET_API_KEY,
                     api_secret=config.BYBIT_TESTNET_API_SECRET)


symbol = None
symbolPair = None
keyInput = None
limitPriceDifference = None
margin = None
level = None
entry_price = None
stop_loss = None
exit_price = None
side = None
total_percent_gained = 0

def setInitialValues(symbolInput, symbolPairInput, marginInput, inputKeyInput, limitPriceDifferenceInput, inputQuantityInput):
    global symbol
    global symbolPair
    global keyInput
    global limitPriceDifference
    global margin
    global inputQuantity

    symbol = symbolInput
    symbolPair = symbolPairInput
    keyInput = inputKeyInput
    limitPriceDifference = limitPriceDifferenceInput
    margin = marginInput
    inputQuantity = inputQuantityInput


def getSymbol():
    return symbol

def getKeyInput():
    return keyInput

def getSymbolPair():
    return symbolPair

def getLimitPriceDifference():
    return limitPriceDifference

def setSide(sideInput):
    global side
    side = sideInput

def getSide():
    return side

def getInputQuantity():
    return inputQuantity

def setInputQuantity(inputQuantityInput):
    global inputQuantity
    inputQuantity = inputQuantityInput

def setLevel(levelInput):
    global level
    level = levelInput

def getLevel():
    return level

def setEntryPrice(entryPriceInput):
    global entry_price
    entry_price = entryPriceInput

def getEntryPrice():
    return entry_price

def setStopLoss(stopLossInput):
    global stop_loss
    stop_loss = stopLossInput

def getStopLoss():
    return stop_loss

def setExitPrice(exitPriceInput):
    global exit_price
    exit_price = exitPriceInput

def getExitPrice():
    return exit_price

def setTotalPercentGain(totalPercentGainInput):
    global total_percent_gained
    total_percent_gained = percentGainInput

def getTotalPercentGain():
    return total_percent_gained

def getMargin():
    return margin

def setMargin(marginInput):
    global margin
    margin = marginInput