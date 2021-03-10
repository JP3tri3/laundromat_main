import config
import bybit_info
import strategy
from time import time, sleep
import json
import time
import datetime
import bybit
import sys
import asyncio

client = bybit.bybit(test=True, api_key=config.BYBIT_TESTNET_API_KEY,
                     api_secret=config.BYBIT_TESTNET_API_SECRET)


async def main():
    flag = True
    temp = 0
    tempCondition = 60

    while(flag == True):

        strategy.checkInputs()
        strategy.initiateMarketTrade()
        time.sleep(1)
        temp += 1
        if (temp == tempCondition):
            print("waiting on input...")
            bybit_info.timeStamp()
            temp = 0


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
