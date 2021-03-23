import sys
sys.path.append("..")
import database.database as db
from model.calc import Calc
import json
import datetime

total_profit_loss = 0
total_number_trades = 0

calc = Calc()

def timeStamp():
    ct = datetime.datetime.now()
    print("Time: ", ct)

def updateData(nameInput, keyInput, valueInput):
    name = nameInput
    key = keyInput
    value = valueInput
    try:
        access_file = open(r"C:\Users\Plan3t\Documents\Bots\Laundromat_main\data.json", "r")
        json_object = json.load(access_file)
        access_file.close()

        json_object[name][key] = value

        access_file = open(r"C:\Users\Plan3t\Documents\Bots\Laundromat_main\data.json", "w")
        json.dump(json_object, access_file, indent=4)
        access_file.close()
    except Exception as e:
        print("an exception occured - {}".format(e))
        updateData(name, key, value)

def updateDisplayData(key, value):
    access_file = open(r"C:\Users\Plan3t\Documents\Bots\Laundromat_main\data.json", "r")
    json_object = json.load(access_file)
    access_file.close()

    json_object[key] = value

    access_file = open(r"C:\Users\Plan3t\Documents\Bots\Laundromat_main\data.json", "w")
    json.dump(json_object, access_file, indent=4)
    access_file.close()

def viewData(nameInput, keyInput):
    name = nameInput
    key = keyInput

    try:
        with open(r'C:\Users\Plan3t\Documents\Bots\Laundromat_main\data.json') as f:
            data = json.load(f)
            f.close()
        return data[name][key]
    except Exception as e:
        print("an exception occured - {}".format(e))
        viewData(name, key)

def updateDataPersistent(data):
        inputName = data['input_name']

        lastCandleHigh = data['last_candle_high']
        lastCandleLow = data['last_candle_low']
        lastCandleVwap = data['last_candle_vwap']
        wt1 = data['wt1']
        wt2 = data['wt2']
        codeRedNotice = data['code_red']

        updateData(inputName, 'last_candle_high', lastCandleHigh)
        updateData(inputName, 'last_candle_low', lastCandleLow)
        updateData(inputName, 'last_candle_vwap', lastCandleVwap)

        updateData(inputName, 'wt1', wt1)
        updateData(inputName, 'wt2', wt2)

        updateData('notice', 'code_red', codeRedNotice)

def updateDataOnAlert(data):
        inputName = data['name']
        inputKey = data['key']
        inputValue = data['value']

        updateData(inputName, inputKey, inputValue)


def logClosingDetails():
    global total_profit_loss
    global total_number_trades

    entry_price = calc.calcEntryPrice()
    exit_price = calc.calcExitPrice()
    percent_gain = db.getTotalPercentGain()
    stop_loss = db.getStopLoss()
    side = db.getSide()
    total_percent_gained = db.getTotalPercentGain()
    total_gain = calc.calcTotalGain()
    total_coin = calc.calcTotalCoin()

    total_number_trades += 1
    total_profit_loss += total_gain 

    f = open("logs.txt", "a")
    f.write(str(datetime.datetime.now()) + "\n")
    f.write("Side: " + str(side) + "\n")
    f.write("Entry Price: " + str(entry_price) + "\n")
    f.write("Exit Price: " + str(exit_price) + "\n")
    f.write("Percent Gain: " + str(total_percent_gained) + "\n")
    f.write("SL: " + str(stop_loss) + "\n")
    f.write("$ Gain: " + str(total_gain) + "\n")
    f.write("Coin Gain: " + str(total_coin) + "\n")
    f.write("#Trades: " + str(total_number_trades) + "\n")
    f.write("Running Total: " + str(total_profit_loss) + "\n")
    f.write("\n")
    f.close()
    print("Logged Closing Details")

    updateDisplayData('test1_number_Of_trades', total_number_trades)
    updateDisplayData('test1_profit_loss', round(total_profit_loss, 4))

def clearJson(flag, dataNameInput):
    if(flag == True):
        updateDisplayData('test1_number_Of_trades', 0)
        updateDisplayData('test1_profit_loss', 0)
        print("Display Cleared")

        updateData(dataNameInput, 'last_candle_high', 0)
        updateData(dataNameInput, 'last_candle_low', 0)
        updateData(dataNameInput, 'last_candle_vwap', 0)

        updateData(dataNameInput, 'active_position', 'null')
        updateData(dataNameInput, 'new_trend', 'null')
        updateData(dataNameInput, 'active_trend', 'null')
        updateData(dataNameInput, 'last_trend', 'null')

        updateData(dataNameInput, 'wt1', 0)
        updateData(dataNameInput, 'wt2', 0)


def clearLogs(flag):
    if(flag == True):
        file = open("logs.txt","r+")
        file.truncate(0)
        file.close()
        print("Logs Cleared")