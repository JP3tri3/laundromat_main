import sys
sys.path.append("..")
import config
import strategy
from time import time, sleep
import time
import datetime

import asyncio
import controller.comms as comms


async def main():
    flag = True
    temp = 0
    tempCondition = 30

    while(flag == True):

        strategy.checkInputs()

        strategy.initiateMarketTradeVwap()
        time.sleep(1)
        temp += 1
        if (temp == tempCondition):
            print("waiting on input...")
            comms.timeStamp()
            temp = 0


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
