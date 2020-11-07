import asyncio;

from sanic import Sanic
from sanic import response
from sanic.response import json
from sanic.response import redirect
import aiofiles
import websockets;
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import functions
import json
import datetime

try:
    app = firebase_admin.get_app()
except ValueError as e:
    cred = credentials.Certificate('./leobot-9fbb1-firebase-adminsdk-p6m4j-ff50753b80.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://leobot-9fbb1.firebaseio.com/'
    })

global fetched_db
dir = db.reference(f"ocnotify")
global fetched_db
fetched_db = dir.get()

async def accept(websocket, path):
    while True:
        data = await websocket.recv()
        print(path,data)
        if path == "/regtimer":
            try:
                data = json.loads(data)
                timers = await functions.get_timers(data,fetched_db)
                c=0
                await websocket.send("Timer Running")
                for t in timers:
                    a = await wait_until(t)
                    if "LATETIME":
                        print("ERROR: CurrentTime is Bigger Than TargetTime")
                    else:
                        await websocket.send(str(await functions.get_processed_data(data,fetched_db,c)))
                    c+=1
                await websocket.send("Timer Done")
            except Exception as e:
                cf='{"school":"신사중","class":"3-2"} or {"school":"신사중","class":"3-2","timers":["08:55", "09:50", "10:45", "11:40", "13:15", "14:10", "15:05"]}'
                await websocket.send(f"\nERROR: Wrong Data Format. \nCorrect Formet is \n{cf} \n\nError Message: {e} " )
        else:
            await websocket.send("ERROR: Please Request on Right Route.\nRoute List: /getdata, /getclassdata, /getalldata, /postdata, /regtimer")

async def wait_until(runTime):
    startTime = datetime.time(*(map(int, runTime.split(':'))))
    print(startTime)
    if startTime < datetime.datetime.today().time():
        return "LATETIME"
    while startTime > datetime.datetime.today().time():
        await asyncio.sleep(1)
    return "OK"

start_server = websockets.serve(accept, '0.0.0.0', 9876);
asyncio.get_event_loop().run_until_complete(start_server);
asyncio.get_event_loop().run_forever();