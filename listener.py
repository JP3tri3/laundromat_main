import config
from time import time, sleep
import json
import time
from sanic import Sanic
from sanic import response
from sanic.request import Request
from sanic.response import json
from sanic_jinja2 import SanicJinja2

app = Sanic(__name__)
jinja = SanicJinja2(app, pkg_name="listener")

myTime = int(time.time() * 1000)
trendFlag = False


def determineTrend(trend):
    print("determing trend:")
    global trendFlag
    if (trend == "uptrend"):
        trendFlag = True
        print("uptrend")
    elif (trend == "downtrend"):
        trendFlag = False
        print("downtrend")
    else:
        trendFlag = trendFlag
        if(trendFlag == True):
            print("uptrend")
        else:
            print("downtrend")


@app.route('/')
async def index(request):
    return jinja.render("index.html", request)


@app.route('/webhook', methods=['POST'])
async def webhook(request):

    print("test")
    data = request.json

    trend = data["strategy"]["flag"]

    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        print("invalid passphrase")
        return json({
            "code": "error",
            "message": "Invalid Passphrase"
        })
    else:
        if (trend == "uptrend"):
            print("Uptrend success")
            return json({
                "code": "success",
                "message": "order executed"
            })
        else:
            print("Uptrend failed")
            return json({
                "code": "failed"
            })

        determineTrend(trend)

        if (trendFlag == False):
            return json({
                "code": "downtrend, waiting"
            })
        else:
            side = data['strategy']['order_action'].upper()
            quantity = data['strategy']['order_contracts']
            ticker = data['ticker']
            print(side)
            return json({
                "code": "success",
                "message": "order executed"
            })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
