""" 
-*- coding: utf-8 -*-
Created on SAT Dec 2 16:43:45 2021
@author: ZHANG Shixiang
CopyRight:*
"""
import KR6R700_KinematicsClass 
import numpy as np

PosofStart = np.array([500, 0, 90, 0, 0, 0, 0])
PosofGoal = KR6R700_KinematicsClass.BoxLocation
VelocityLimit = [KR6R700_KinematicsClass.Limit[i][2] for i in range(len(KR6R700_KinematicsClass.Limit))]
StepLang = 200.
RRTKin = KR6R700_KinematicsClass.Zsx_kinematics()   #这里会执行RRTKin(Zsx_kinematics)初始化 优先于kin

class Node(object):
    global ThetaPos, EulerPos
    ThetaPos = np.zeros([7])
    EulerPos = np.zeros([6])
    ParentDistanec = 0.
    def __init__(self, pos1, pos2):
        self.ThetaPos = pos1
        self.EulerPos = pos2
        self.parent = None
        
class Zsx_RRT():
    global RRTKin

    def __init__(self):
        self.StartNode = Node(PosofStart, RRTKin.RefreshFKAbsolute(PosofStart))
        self.EndNode   = Node(RRTKin.RefreshIKAbsolute(PosofGoal)[0], PosofGoal)
        self.NodeList  = [self.StartNode]
        self.ThetaVectorFromStartToGoal = (RRTKin.RefreshIKAbsolute(PosofGoal)[0] - PosofStart) / np.linalg.norm((RRTKin.RefreshIKAbsolute(PosofGoal)[0] - PosofStart))
        self.EulerVectorFromStartToGoalXYZ = ((PosofGoal - RRTKin.RefreshFKAbsolute(PosofStart)) / np.linalg.norm((PosofGoal - RRTKin.RefreshFKAbsolute(PosofStart))))[:3]

    def GenerateARRTNode(self,collisionPos):
        EulerVectorColposToGoalXYZ = ((PosofGoal - RRTKin.RefreshFKAbsolute(collisionPos)) / np.linalg.norm((PosofGoal - RRTKin.RefreshFKAbsolute(collisionPos))))[:3]
        EulerVectorNewXYZ = np.cross(self.EulerVectorFromStartToGoalXYZ, EulerVectorColposToGoalXYZ)
        NewNodeEulerXYZ = collisionPos[:3] - (collisionPos[:3] - self.NodeList[(len(self.NodeList)-1)].EulerPos[:3])/np.linalg.norm(collisionPos[:3] - self.NodeList[(len(self.NodeList)-1)].EulerPos[:3])*50 + EulerVectorNewXYZ*StepLang
        NewNodeEuler = np.hstack((NewNodeEulerXYZ , collisionPos[3:]))
        NewNdeTmp = Node(RRTKin.RefreshIKAbsolute(NewNodeEuler),NewNodeEuler)
        return NewNdeTmp

    def GetNearestListIndex(self,nodeList ,newNode):
        distanceList = [np.linalg.norm(newNode.EulerPos[:3] - node.EulerPos[:3]) for node in nodeList]
        minIndex = distanceList.index(min(distanceList))
        return minIndex

    def Planning(self,collisionRecv):
        newNode = self.GenerateARRTNode(collisionRecv)
        newNode.parent = self.GenerateARRTNode(self.NodeList, newNode)
        return newNode.ThetaPos

if __name__ == '__main__':
    kin = KR6R700_KinematicsClass.Zsx_kinematics()
    RRT = Zsx_RRT(kin.GetIKFixed7AxisOutput(),kin.GetFKOutput(),kin.RefreshIKAbsolute(PosofGoal),PosofGoal)