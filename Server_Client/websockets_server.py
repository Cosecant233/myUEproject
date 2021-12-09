""" 
-*- coding: utf-8 -*-
Created on SAT Nov 26 19:01:03 2021
@author: ZHANG Shixiang
CopyRight:*
"""

import camera_KinematicsClass
import path_planning
import asyncio ,threading
import websockets
from queue import Queue
#from queue import PriorityQueue

def StartLoop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

camera1 = camera_KinematicsClass.Camera_kinematics()

async def RecvMsg(websocket):
    recvText = await websocket.recv()
    if(recvText[0]=='{'):
        return
    cmd=recvText.split(',',1)[0]
    if(cmd == '10'):
        cameraPos = camera1.RefreshFKAbsolute(recvText[7] + recvText[1:7])
        cameraMsg = [12] + cameraPos + recvText[1:8]
        await websocket.send(cameraMsg)
    elif(cmd  == '11'):
        cameraPos = camera1.RefreshFKRelative(recvText[7] + recvText[1:7])
        cameraMsg = [12] + cameraPos + recvText[1:8]
        await websocket.send(cameraMsg)
    elif(int(cmd)>=1 and int(cmd)<=8):
        path_planning.ReceQueue.put(recvText)
    else:
        pass

async def SendMsg(websocket):
    if(not path_planning.SendQueue.empty()):
        message = path_planning.SendQueue.get()            #"0,0,0,0,0,0,0"
        message = [str(j) for j in message]
        message =','.join(message)
        print("test:",message)
        await websocket.send(message)

async def mainLogic(websocket,path):
    while(1):
        await SendMsg(websocket)
        await RecvMsg(websocket)
    
def PcWebsocketsServer(ipaddr,port):
    pcServer=websockets.serve(mainLogic,ipaddr,port)
    asyncio.get_event_loop().run_until_complete(pcServer)
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    PcWebsocketsServer("127.0.0.1",8282)