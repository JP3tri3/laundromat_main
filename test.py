import bybit_info
import json
import time
import asyncio

# access:
# with open('data.json') as f:
#     data = json.load(f)

# for vwap in data['vwap']:
#     print(vwap['1min'], vwap['3min'])


# add data:
# def write_json(data, filename="data.json"):
#     with open(filename, "w") as f:
#         json.dump(data, f, indent=4)


# # change:

# write_json(originalData)


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


while True:
    updateData('passphrase', '1')
    time.sleep(3)
    updateData('passphrase', '2')
    time.sleep(3)
    updateData('passphrase', '3')
    time.sleep(3)
    updateData('passphrase', '4')
    time.sleep(3)
    updateData('passphrase', '5')
    time.sleep(3)
# updateData('vwap', '1min', 50)

# print(viewData('vwap', '1min'))

# async:


# def is_prime(x):
#     return not any(x//i == x/i for i in range(x-1, 1, -1))


# async def highest_prime_below(x):
#     print('Highest prime below %d' % x)
#     for y in range(x-1, 0, -1):
#         if is_prime(y):
#             print('- Highest prime below %d is %d' % (x, y))
#             return y
#         await asyncio.sleep(0)
#         # time.sleep(0.01)
#     return None


# async def main():

#     t0 = time.time()
#     await asyncio.wait([
#         highest_prime_below(100000),
#         highest_prime_below(10000),
#         highest_prime_below(1000)
#     ])
#     t1 = time.time()
#     print('Took %.2f ms' % (1000*(t1-t0)))

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# loop.close()


# data = asyncio.Queue()
