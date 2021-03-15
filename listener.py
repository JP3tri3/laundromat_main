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

app = Sanic(__name__)
jinja = SanicJinja2(app, pkg_name="listener")

myTime = int(time.time() * 1000)
trendFlag = False


@app.route('/')
async def index(request):
    return jinja.render("index.html", request)


@app.route('/webhook', methods=['POST'])
async def webhook(request):

    data = request.json

    inputName = data['name']
    inputKey = data['key']
    inputValue = data['value']

    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        print("invalid passphrase")
        return json({
            "code": "error",
            "message": "Invalid Passphrase"
        })
    else:
        comms.updateData(inputName, inputKey, inputValue)
        return json({
            "code": "success",
            "message": "json updated"
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
