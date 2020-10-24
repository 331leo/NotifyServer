import asyncio;
# 웹 소켓 모듈을 선언한다.
import websockets;
import discord
import sys
import os
import json
async def accept(websocket, path):
  while True:
    # 클라이언트로부터 메시지를 대기한다.
    data = await websocket.recv();
    try:
      datad = json.loads(data)
      await websocket.send(f"Dict/ path: {path} , \n학교: {datad['school']}\n반: {datad['class']['num']}\nZoom여부: {datad['class']['isZoom']}\nZoom 링크: {datad['class']['url']}");
    except:
      await websocket.send(f"No dict/ path: {path} , receive : {data}" );
    # 클라인언트로 echo를 붙여서 재 전송한다.


start_server = websockets.serve(accept, '0.0.0.0', 9876);
asyncio.get_event_loop().run_until_complete(start_server);
asyncio.get_event_loop().run_forever();



