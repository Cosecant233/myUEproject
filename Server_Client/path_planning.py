""" 
-*- coding: utf-8 -*-
Created on SAT Nov 27 15:46:30 2021
@author: ZHANG Shixiang
CopyRight:*
"""

from threading import Thread
import KR6R700_KinematicsClass
import asyncio
import numpy as np
import time
from queue import Queue
import RRTClass                               #这里会执行RRTKin(Zsx_kinematics)初始化 优先于kin

stepLength = 200

SendQueue = Queue()
ReceQueue = Queue()
kin = KR6R700_KinematicsClass.Zsx_kinematics()#这里会执行kin(Zsx_kinematics)初始化
RRT = RRTClass.Zsx_RRT()

async def AbouttoSendMsgTransHelper(commandNum, msg):
    sendMsg = np.hstack(([commandNum], msg[1:], msg[0]))
    SendQueue.put(sendMsg)

async def PathPlanningMainLoop():
    global kin,RRT
    await AbouttoSendMsgTransHelper(0,RRTClass.PosofStart)
    while(ReceQueue.empty()):
        time.sleep(1)
    print(ReceQueue.get())

    await AbouttoSendMsgTransHelper(0, kin.RefreshIKAbsolute(KR6R700_KinematicsClass.BoxLocation)[0])
    while True:
        if(not ReceQueue.empty()):
            time.sleep(1)
        ReceivMsg = ReceQueue.get()
        recvTheta = np.hstack((ReceivMsg[7],ReceivMsg[:7]))
        if(ReceivMsg[0] == 8):
            if(np.linalg.norm( kin.RefreshFKAbsolute(recvTheta) - RRTClass.PosofGoal) < 10):
                print("Action done.")
                break
            else:
                await AbouttoSendMsgTransHelper(0, kin.RefreshIKAbsolute(KR6R700_KinematicsClass.BoxLocation)[0])
        else:
            await AbouttoSendMsgTransHelper(0, RRT.Planning(recvTheta))