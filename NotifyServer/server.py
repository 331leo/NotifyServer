import asyncio;
import os
from __main__ import app
from sanic import Sanic
from sanic import response
from sanic.response import json
from sanic.response import redirect
import aiofiles
import websockets
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import NotifyServer.functions as functions
import datetime
import sys
try:
    app2 = firebase_admin.get_app()
except ValueError as e:
    cred = credentials.Certificate('./leobot-9fbb1-firebase-adminsdk-p6m4j-ff50753b80.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://leobot-9fbb1.firebaseio.com/'
    })
print(os.system("nohup python3 NotifyServer/websockettimer.py &"))
global fetched_db
dir = db.reference(f"ocnotify")
global fetched_db
fetched_db = dir.get()
'''
app = Sanic (__name__)
app.config['JSON_AS_ASCII'] = False
'''

@app.route('/getdata',methods = ['POST'])
async def getdata(request):

    try:
        data = request.json
        returndata = await functions.get_processed_data(data, fetched_db)
        return json(returndata)
    except Exception as e:
        cf = '{"school":"신사중","class":"3-2"}'
        returndata = {"iserror":True,"message":f"Wrong Data Format. "
                                               f"Correct Formet is "
                                               f"{cf} "
                                               f"Error Message: {e}"}
        return json(returndata)

@app.route("/getclassdata",methods = ['POST'])
async def getclassdata(request):
    try:
        data = request.json
        returndata = await functions.get_all_data(data, fetched_db)
        return json(returndata)
    except Exception as e:
        cf = '{"school":"신사중","class":"3-2"}'
        returndata = {"iserror":True,"message":f"Wrong Data Format. "
                                               f"Correct Formet is "
                                               f"{cf} "
                                               f"Error Message: {e} "}
        return json(returndata)

@app.route("/postdata",methods = ['POST'])
async def postdata(request):
    global fetched_db
    try:
        data = request.json
        fetched_db = await functions.post_data(data, fetched_db)
        print(fetched_db)
        dir.update(fetched_db)
        returndata = await functions.get_all_data(data, fetched_db)
        return json(returndata)

    except Exception as e:
        cf = '{"school":"신사중","class":"3-2",data:{}}'
        returndata = {"iserror": True,
                      "message": f"Wrong Data Format. "
                                 f"Correct Formet is "
                                 f"{cf} "
                                 f"Error Message: {e} "}
        return json(returndata)


@app.route("/getalldata",methods = ['GET','POST'])
async def getalldata(request):
    return json(fetched_db)

'''
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8765)

'''
