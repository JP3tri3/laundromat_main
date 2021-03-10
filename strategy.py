import comms
import bybit_info
import asyncio

vwap1min = ""


def checkInputs():
    global vwap1min

    vwap1min = comms.viewData('vwap', '1min')
    return vwap1min


def initiateMarketTrade():
    global vwap1min
    if (vwap1min == "crossover"):
        vwap1min = "null"
        bybit_info.createMarketOrder('Buy', 'BTCUSD')
    elif (vwap1min == "crossunder"):
        vwap1min = "null"
        bybit_info.createMarketOrder('Sell', 'BTCUSD')

# add close order if vwap changes
