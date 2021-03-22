import sys
sys.path.append("..")
import controller.comms as comms
import config
from time import time, sleep
import json
import time
import asyncio
from sanic import Sanic
from sanic import response
from sanic.request import Request
from sanic.response import json
from sanic_jinja2 import SanicJinja2
from strategy import Strategy

app = Sanic(__name__)
jinja = SanicJinja2(app, pkg_name="listener")

myTime = int(time.time() * 1000)
trendFlag = False

data_name = '1_min'
vwapMarginNeg = -10.5
vwapMarginPos = 10.5

strat = Strategy(vwapMarginNeg, vwapMarginPos, data_name)

@app.route('/')
async def index(request):
    return jinja.render("index.html", request)


@app.route('/webhook', methods=['POST'])
async def webhook(request):

    data = request.json

    persistent_data = data['persistent_data']

    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        print("invalid passphrase")
        return json({
            "code": "error",
            "message": "Invalid Passphrase"
        })
    else:
        if(persistent_data == 'True'):

            comms.updateDataPersistent(data)

        else:

            comms.updateDataOnAlert(data)

        #strategy:
        strat.determineVwapTrend()

        return json({
            "code": "success",
            "message": "json updated"
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
