import sys
sys.path.append("..")
import database.database as db
import json
import datetime

def timeStamp():
    ct = datetime.datetime.now()
    print("Time: ", ct)


def updateData(name, key, value):
    access_file = open("data.json", "r")
    json_object = json.load(access_file)
    access_file.close()

    json_object[name][key] = value

    access_file = open("data.json", "w")
    json.dump(json_object, access_file, indent=4)
    access_file.close()
    print("Json Updated")
    print(json_object)


def viewData(name, key):
    output = ''
    with open('data.json') as f:
        data = json.load(f)
        f.close()
    return data[name][key]


def logClosingDetails():
    entry_price = db.getEntryPrice()
    exit_price = db.getEntryPrice()
    percent_gain = db.getPercentGain()
    stop_loss = db.getStopLoss()
    side = db.getSide()
    total_percent_gained = db.getTotalPercentGain()

    f = open("logs.txt", "a")
    f.write(str(datetime.datetime.now()) + "\n")
    f.write("Side: " + str(side) + "\n")
    f.write("Entry Price: " + str(entry_price) + "\n")
    f.write("Exit Price: " + str(exit_price) + "\n")
    f.write("Percent Gain: " + str(total_percent_gained) + "\n")
    f.write("SL: " + str(stop_loss) + "\n")
    f.write("Total Gain: " + str(total_gain) + "\n")
    f.write("\n")
    f.close()
