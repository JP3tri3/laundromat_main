import sys
sys.path.append("..")
from database.database import Database
from model.calc import Calc
import json
import datetime


# class Comms:

#     def __init__(self):
#         self.total_profit_loss = 0
#         self.total_number_trades = 0

def timeStamp():
    ct = datetime.datetime.now()
    print("Time: ", ct)
    return ct

# def updateData(nameInput, keyInput, valueInput):
#     name = nameInput
#     key = keyInput
#     value = valueInput
#     try:
#         access_file = open("data.json", "r")
#         json_object = json.load(access_file)
#         access_file.close()

#         json_object[name][key] = value

#         access_file = open("data.json", "w")
#         json.dump(json_object, access_file, indent=4)
#         access_file.close()
#     except Exception as e:
#         print("an exception occured - {}".format(e))
#         updateData(name, key, value)

def updateDisplayData(key, value):
    access_file = open("data.json", "r")
    json_object = json.load(access_file)
    access_file.close()

    json_object[key] = value

    access_file = open("data.json", "w")
    json.dump(json_object, access_file, indent=4)
    access_file.close()

def updateDisplayDataValues():
    updateDisplayData('mainTest_number_Of_trades', total_number_trades)
    updateDisplayData('mainTest_profit_loss', round(total_profit_loss, 4))


def viewData(nameInput, keyInput):
    name = nameInput
    key = keyInput

    try:
        with open('data.json') as f:
            data = json.load(f)
            f.close()
        return data[name][key]
    except Exception as e:
        print("an exception occured - {}".format(e))
        viewData(name, key)

def updateDataPersistent(data):
        input_name = data['input_name']

        last_candle_high = data['last_candle_high']
        last_candle_low = data['last_candle_low']
        last_candle_vwap = data['last_candle_vwap']
        wt1 = data['wt1']
        wt2 = data['wt2']

        conn.updateStratValues(input_name, wt1, wt2, last_candle_high, last_candle_low, last_candle_vwap)        

def updateDataOnAlert(data):
        strat_id = data['name']
        input_column = data['key']
        input_value = data['value']

        updateData(inputName, inputKey, inputValue)
        conn.updateTableValue('strategy', strat_id, input_column, input_value)

def clearJson(flag, dataNameInput):
    if(flag == True):
        updateDisplayData('mainTest_number_Of_trades', 0)
        updateDisplayData('mainTest_profit_loss', 0)
        updateDisplayData('test1_number_Of_trades', 0)
        updateDisplayData('test1_profit_loss', 0)
        updateDisplayData('test2_number_Of_trades', 0)
        updateDisplayData('test2_profit_loss', 0)
        updateDisplayData('test3_number_Of_trades', 0)
        updateDisplayData('test3_profit_loss', 0)        
        print("Display Cleared")

# def logClosingNotes(side, entry_price, exit_price, percent_gain, stop_loss, total_gain, total_coin, total_number_trades, total_p_l)
#         f = open("logs.txt", "a")
#         f.write("Time: " + time) + "\n")
#         f.write("Side: " + str(side) + "\n")
#         f.write("Entry Price: " + str(entry_price) + "\n")
#         f.write("Exit Price: " + str(exit_price) + "\n")
#         f.write("Percent Gain: " + str(percent_gain) + "\n")
#         f.write("SL: " + str(stop_loss) + "\n")
#         f.write("$ Gain: " + str(total_gain) + "\n")
#         f.write("Coin Gain: " + str(total_coin) + "\n")
#         f.write("#Trades: " + str(total_number_trades) + "\n")
#         f.write("Running Total: " + str(total_p_l) + "\n")
#         f.write("\n")
#         f.close()
#         print("Logged Closing Details")

def clearLogs(flag):
    if(flag == True):
        file = open("logs.txt","r+")
        file.truncate(0)
        file.close()
        print("Logs Cleared")