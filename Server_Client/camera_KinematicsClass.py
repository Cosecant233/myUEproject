"""
-*- coding: utf-8 -*-
Created on SAT Nov 26 19:01:38 2021
@author: ZHANG Shixiang
CopyRight:*
"""

import numpy as np
from copy import deepcopy

DH      = [ [  90.,   0.,    0.,    0.],        #+      KUKA KR6 R700
            [ -90.,  25.,  400.,    0.],        #-
            [   0., 315.,    0.,  -90.],        #-90+
            [ -90.,  35.,    0.,    0.],        #+
            [  90.,   0.,  365.,    0.],        #-
            [ -90.,   0.,    0.,    0.]  ]      #+ 
WF      =   [   0.,   0.,    0.,    0.,   0.,  -90.]
TF      =   [   0.,   0.,   40.,    0.,   0.,  -90.]    
Limit   = [ [   0., 1500,  999.,  999.],
            [-170., 170.,  999.,  999.], 
            [-190.,  45.,  999.,  999.],
            [-120., 156.,  999.,  999.],
            [-185., 185.,  999.,  999.],
            [-120., 120.,  999.,  999.],
            [-350., 350.,  999.,  999.]  ]

class Camera_kinematics():
    FKInput             = np.zeros([7])
    FKDHCache           = np.zeros([6,4])
    FKDHTrans           = np.zeros([6,4,4])
    WFTrans             = np.zeros([4,4])
    TFTrans             = np.zeros([4,4])
    FKTransResult       = np.zeros([4,4])
    FKOutput            = np.zeros([6])

    def TransMatrixStandard(self,Din):
        OutArray = np.zeros([4,4])
        OutArray = [[np.cos(Din[3]),-np.sin(Din[3])*np.cos(Din[0]), np.sin(Din[3])*np.sin(Din[0]), Din[1]*np.cos(Din[3])],
                    [np.sin(Din[3]), np.cos(Din[3])*np.cos(Din[0]),-np.cos(Din[3])*np.sin(Din[0]), Din[1]*np.sin(Din[3])],
                    [            0.,                np.sin(Din[0]),                np.cos(Din[0]),                Din[2]],
                    [            0.,                            0.,                            0.,                   1.0]  ]
        return OutArray
    
    def TransMatrixFixedAnglesXYZ(self,Din):
        OutArray = np.zeros([4,4])
        OutArray = [[np.cos(np.radians(Din[3]))*np.cos(np.radians(Din[4])), np.cos(np.radians(Din[3]))*np.sin(np.radians(Din[4]))*np.sin(np.radians(Din[5]))-np.sin(np.radians(Din[3]))*np.cos(np.radians(Din[5])), np.cos(np.radians(Din[3]))*np.sin(np.radians(Din[4]))*np.cos(np.radians(Din[5]))+np.sin(np.radians(Din[3]))*np.sin(np.radians(Din[5])), Din[0] ],
                    [np.sin(np.radians(Din[3]))*np.cos(np.radians(Din[4])), np.sin(np.radians(Din[3]))*np.sin(np.radians(Din[4]))*np.sin(np.radians(Din[5]))+np.cos(np.radians(Din[3]))*np.cos(np.radians(Din[5])), np.sin(np.radians(Din[3]))*np.sin(np.radians(Din[4]))*np.cos(np.radians(Din[5]))-np.cos(np.radians(Din[3]))*np.sin(np.radians(Din[5])), Din[1] ],
                    [                          -np.sin(np.radians(Din[4])),                                                                                  np.cos(np.radians(Din[4]))*np.sin(np.radians(Din[5])),                                                                                  np.cos(np.radians(Din[4]))*np.cos(np.radians(Din[5])), Din[2] ],
                    [                                                   0.,                                                                                                                                     0.,                                                                                                                                     0.,    1.0 ]  ]
        return OutArray

    def TransMatrixFixedAnglesXYZReverse(self,Din):
        OutArray = np.zeros([6])
        OutArray[0] = Din[0][3]
        OutArray[1] = Din[1][3]
        OutArray[2] = Din[2][3]
        if(Din[2][0] == -1.0):
            OutArray[4] = 90.
            OutArray[3] = 0.
            OutArray[5] = np.degrees(np.arctan2(Din[0][1], Din[1][1]))
        elif(Din[2][0] == 1.0):
            OutArray[4] = -90.
            OutArray[3] = 0.
            OutArray[5] = np.degrees(-np.arctan2(Din[0][1], Din[1][1]))
        else:
            OutArray[4] = np.degrees(np.arctan2(-Din[2][0],np.sqrt((Din[0][0] ** 2) + (Din[1][0] ** 2))))
            OutArray[3] = np.degrees(np.arctan2((Din[1][0] / np.cos(OutArray[4])),(Din[0][0] / np.cos(OutArray[4]))))
            OutArray[5] = np.degrees(np.arctan2((Din[2][1] / np.cos(OutArray[4])),(Din[2][2] / np.cos(OutArray[4]))))
        return OutArray

    def __init__(self):
        self.FKDHCache = deepcopy(DH)
        for i in range(len(DH)):
            self.FKDHCache[i][0] = np.radians(DH[i][0])
            self.FKDHCache[i][3] = np.radians(DH[i][3])
            self.FKDHTrans[i] = self.TransMatrixStandard(self.FKDHCache[i])
        self.WFTrans  = self.TransMatrixFixedAnglesXYZ(WF)
        self.TFTrans  = self.TransMatrixFixedAnglesXYZ(TF)
        self.FKTransResult = deepcopy(self.WFTrans)
        for i in range(len(DH)):
            self.FKTransResult = np.dot(self.FKTransResult, self.FKDHTrans[i])
        self.FKTransResult = np.dot(self.FKTransResult, self.TFTrans)
        self.FKOutput = self.TransMatrixFixedAnglesXYZReverse(self.FKTransResult)
        #print("initFKOutput \n",self.FKOutput)

    def RefreshFKRelative(self,FKInputRelativeRe):   
        for i in range(len(DH)):
            if(FKInputRelativeRe[i]):
                self.FKInput[i] += FKInputRelativeRe[i]
                if(self.CheckLimitPermit2(i,self.FKInput)):    
                    if (i):
                        self.FKDHCache[i][3] = np.radians(self.FKInput[i])
                    else:    
                        self.FKDHCache[i][2] = self.FKInput[i]
                    self.FKDHTrans[i] = self.TransMatrixStandard(self.FKDHCache[i])
                else:
                    self.FKInput[i] -= FKInputRelativeRe[i]
        self.FKTransResult = deepcopy(self.WFTrans)
        for i in range(len(DH)):
            self.FKTransResult = np.dot(self.FKTransResult, self.FKDHTrans[i])
        self.FKTransResult = np.dot(self.FKTransResult, self.TFTrans)
        self.FKOutput = self.TransMatrixFixedAnglesXYZReverse(self.FKTransResult)
        return self.FKOutput

    def RefreshFKAbsolute(self,FKInputAbsoluteRe):
        for i in range(len(DH)):
            if(FKInputAbsoluteRe[i] != self.FKInput[i]):
                if(self.CheckLimitPermit2(i,FKInputAbsoluteRe)):
                    self.FKInput[i] = FKInputAbsoluteRe[i]
                    if (i):
                        self.FKDHCache[i][3] = np.radians(self.FKInput[i])
                    else:    
                        self.FKDHCache[i][2] = self.FKInput[i]
                    self.FKDHTrans[i] = self.TransMatrixStandard(self.FKDHCache[i])
        self.FKTransResult = deepcopy(self.WFTrans)
        for i in range(len(DH)):
            self.FKTransResult = np.dot(self.FKTransResult, self.FKDHTrans[i])
        self.FKTransResult = np.dot(self.FKTransResult, self.TFTrans)
        self.FKOutput = self.TransMatrixFixedAnglesXYZReverse(self.FKTransResult)
        return self.FKOutput

    def GetFKOutput(self):
        return self.FKOutput


if __name__ == '__main__':
    kin = Camera_kinematics()
    print("new FK\n",kin.RefreshFKAbsolute([0,-8.04,-119.04,54.65,0,64.76,-188.03]))