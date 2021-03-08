import json
import datetime


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


def logClosingDetails(entryPrice, exitPrice, percentGain, stopLoss):
    f = open("logs.txt", "a")
    f.write(str(datetime.datetime.now()) + "\n")
    f.write("Entry Price: " + str(entryPrice) + "\n")
    f.write("Exit Price: " + str(exitPrice) + "\n")
    f.write("Percent Gain: " + str(percentGain) + "\n")
    f.write("SL: " + str(stopLoss) + "\n")
    f.write("\n")
    f.close()
