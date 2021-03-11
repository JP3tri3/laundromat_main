from exchange.bybit_info import Bybit_Info
from trade.orders import Orders
import json
import time
import asyncio


def updateData(name, key, value):
    access_file = open("data.json", "r")
    json_object = json.load(access_file)
    print(json_object)
    access_file.close()

    json_object[name][key] = value

    access_file = open("data.json", "w")
    json.dump(json_object, access_file, indent=4)
    access_file.close()
    print(json_object)


def updateData(key, value):
    access_file = open("data.json", "r")
    json_object = json.load(access_file)
    access_file.close()

    json_object[key] = value

    access_file = open("data.json", "w")
    json.dump(json_object, access_file, indent=4)
    access_file.close()
    print(json_object)


def viewData(name, key):
    output = ''
    with open('data.json') as f:
        data = json.load(f)
        f.close()
    return data[name][key]


test1 = Orders("ETHUSD")
# print(Bybit_Info.lastPrice(self))
