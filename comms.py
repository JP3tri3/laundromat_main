import json


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


def viewData(name, key):
    output = ''
    with open('data.json') as f:
        data = json.load(f)
    for k in data[name]:
        output = k[key]
    f.close()
    return output
