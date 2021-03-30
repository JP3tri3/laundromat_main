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
# from test.min9.strategy import Strategy as Strategy9min
# from test.min16.strategy import Strategy as Strategy16min
# from test.min30.strategy import Strategy as Strategy30min

app = Sanic(__name__)
jinja = SanicJinja2(app, pkg_name="listener")

myTime = int(time.time() * 1000)
trendFlag = False

strat = Strategy(-10.5, 10.5)
# strat9min = Strategy9min(-10.5, 10.5, '9_min')
# strat16min = Strategy16min(-8, 8, '16_min')
# strat30min = Strategy30min(-7, 7, '30_min')

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

            comms.update_data_persistent(data)

        else:

            comms.update_data_on_alert(data)

        #strategy:
        strat.determine_vwap_trend()

        # if (data['input_name'] == '9_min'):
        #     strat9min.determine_vwap_trend()
        # elif (data['input_name'] == '16_min'):
        #     strat16min.determine_vwap_trend()
        # elif (data['input_name'] == '30_min'):  
        #     strat30min.determine_vwap_trend()

        return json({
            "code": "success",
            "message": "json updated"
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
