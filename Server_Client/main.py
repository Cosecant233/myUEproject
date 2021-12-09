""" 
-*- coding: utf-8 -*-
Created on SAT Nov 26 19:02:04 2021
@author: ZHANG Shixiang
CopyRight:*
"""

import websockets_server
import asyncio,threading
import path_planning

def start_main_loop(loop):
    asyncio.set_event_loop(loop)
    asyncio.run_coroutine_threadsafe(path_planning.PathPlanningMainLoop(),loop)
    loop.run_forever()

def start_websocket_loop(loop):
    asyncio.set_event_loop(loop)
    asyncio.run_coroutine_threadsafe(websockets_server.PcWebsocketsServer("127.0.0.1",8282),loop)
    loop.run_forever()

#---------websocket通信线程------------
websocket_loop = asyncio.new_event_loop()
websocketThread=threading.Thread(target = start_websocket_loop, args = (websocket_loop,))
websocketThread.start()

#---------pathPlan主线程-------------------------
newLoop = asyncio.new_event_loop()
start_main_loop(newLoop)






