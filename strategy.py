import comms
import bybit_info
import asyncio

vwap1min = 0


def checkInputs():
    global vwap1min

    vwap1min = comms.viewData('vwap', '1min')
    return vwap1min


def initiateTrade():
    global vwap1min
    if vwap1min > 5:
        bybit_info.createOrder('Buy', 'BTCUSD', 'Limit')
        vwap1min = 0
    elif vwap1min < -5:
        bybit_info.createOrder('Sell', 'BTCUSD', "Limit")
        vwap1min = 0
