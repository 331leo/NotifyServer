import asyncio;

import websockets;
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import util
import json

try:
    app = firebase_admin.get_app()
except ValueError as e:
    cred = credentials.Certificate('bot/etc/leobot-9fbb1-firebase-adminsdk-p6m4j-ff50753b80.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://leobot-9fbb1.firebaseio.com/'
    })

global fetched_db
dir = db.reference(f"ocnotify")
fetched_db = dir.get()



async def accept(websocket, path):
  while True:
    # 클라이언트로부터 메시지를 대기한다.
    data = await websocket.recv();
    try:
      data = json.loads(data)
      await util.process_data(data,fetched_db)
      await websocket.send(f"Dict/ path: {path} , \n학교: {pd(data)}\n반: {datad['class']['num']}\nZoom여부: {datad['class']['isZoom']}\nZoom 링크: {datad['class']['url']}");
    except:
      await websocket.send(f"Wrong Data Format. Contant support@leok.kr " );



start_server = websockets.serve(accept, '0.0.0.0', 9876);
asyncio.get_event_loop().run_until_complete(start_server);
asyncio.get_event_loop().run_forever();


