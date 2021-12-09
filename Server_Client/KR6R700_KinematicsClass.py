"""
-*- coding: utf-8 -*-
Created on SAT Nov 13 10:38:28 2021
@author: ZHANG Shixiang
CopyRight:*
"""

import numpy as np
from copy import deepcopy

DH      = [ [  90.,   0.,  500.,    0.],        #+      KUKA KR6 R700
            [ -90.,  25.,  400.,    0.],        #-
            [   0., 315.,    0.,  -90.],        #-90+
            [ -90.,  35.,    0.,    0.],        #+
            [  90.,   0.,  365.,    0.],        #-
            [ -90.,   0.,    0.,    0.],        #+
            [   0.,   0.,    0.,    0.]  ]      #-    
WF      =   [   0.,   0.,    0.,    0.,   0.,  -90.]
TF      =   [   0.,   0.,  115.,   90.,   0.,  180.]    #When first tset use >>208, for example 350,instead of 208.
Limit   = [ [   0., 1500,  300.,  999.],
            [-170., 170.,  154.,  999.], 
            [-190.,  45.,  154.,  999.],
            [-120., 156.,  228.,  999.],
            [-185., 185.,  343.,  999.],
            [-120., 120.,  384.,  999.],
            [-350., 350.,  721.,  999.]  ]
BoxLocation = [453., 45.,320.64,    0.,   0.,    0.]

class Zsx_kinematics():
    FKInput             = np.zeros([7])
    IKFixed7AxisIntput  = np.zeros([6])

    FKDHCache           = np.zeros([7,4])
    FKDHTrans           = np.zeros([7,4,4])
    WFTrans             = np.zeros([4,4])
    TFTrans             = np.zeros([4,4])
    WFTransInv          = np.zeros([4,4])
    TFTransInv          = np.zeros([4,4])
    FKTransResult       = np.zeros([4,4])
    IKFixed7AxisJoint0TransInv = np.zeros([4,4])
    IKFixed7AxisJ1toJ6Trans = np.zeros([4,4])
    IKFixed7AxisJ1toJ3Trans = np.zeros([2,4,4])
    IKFixed7AxisJ4toJ6Trans = np.zeros([2,4,4])

    FKOutput            = np.zeros([6])
    IKFixed7AxisOutput  = np.zeros([4,7]) 
    IKFixed7AxisOutputEmptyFlag = np.zeros([4])

    def TransMatrixStandard(self,Din):
        OutArray = np.zeros([4,4])
        OutArray = [[np.cos(Din[3]),-np.sin(Din[3])*np.cos(Din[0]), np.sin(Din[3])*np.sin(Din[0]), Din[1]*np.cos(Din[3])],
                    [np.sin(Din[3]), np.cos(Din[3])*np.cos(Din[0]),-np.cos(Din[3])*np.sin(Din[0]), Din[1]*np.sin(Din[3])],
                    [            0.,                np.sin(Din[0]),                np.cos(Din[0]),                Din[2]],
                    [            0.,                            0.,                            0.,                   1.0]  ]
        return OutArray
    
    def TransMatrixCraig(self,Din):
        OutArray = np.zeros([4,4])
        OutArray = [[               np.cos(Din[3]),               -np.sin(Din[3]),              0.,                 Din[1]],
                    [np.sin(Din[3])*np.cos(Din[0]), np.cos(Din[3])*np.cos(Din[0]), -np.sin(Din[0]), -Din[2]*np.sin(Din[0])],
                    [np.sin(Din[3])*np.sin(Din[0]), np.cos(Din[0])*np.sin(Din[0]),  np.cos(Din[0]),  Din[2]*np.cos(Din[0])],
                    [                           0.,                            0.,              0.,                    1.0]  ]
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

    def TransMatrixEulerAnglesZYZ(self,Din):
        OutArray = np.zeros([4,4])
        OutArray = [[ np.cos(np.radians(Din[3]))*np.cos(np.radians(Din[4]))*np.cos(np.radians(Din[5]))-np.sin(np.radians(Din[3]))*np.sin(np.radians(Din[5])),-np.cos(np.radians(Din[3]))*np.cos(np.radians(Din[4]))*np.sin(np.radians(Din[5]))-np.sin(np.radians(Din[3]))*np.cos(np.radians(Din[5])), np.cos(np.radians(Din[3]))*np.sin(np.radians(Din[4])), Din[0] ],
                    [ np.sin(np.radians(Din[3]))*np.cos(np.radians(Din[4]))*np.cos(np.radians(Din[5]))+np.cos(np.radians(Din[3]))*np.sin(np.radians(Din[5])),-np.sin(np.radians(Din[3]))*np.cos(np.radians(Din[4]))*np.sin(np.radians(Din[5]))+np.cos(np.radians(Din[3]))*np.cos(np.radians(Din[5])), np.sin(np.radians(Din[3]))*np.sin(np.radians(Din[4])), Din[1] ],
                    [                                                                                 -np.sin(np.radians(Din[4]))*np.cos(np.radians(Din[5])),                                                                                  np.sin(np.radians(Din[4]))*np.sin(np.radians(Din[5])),                           -np.cos(np.radians(Din[4])), Din[2] ],
                    [                                                                                                                                     0.,                                                                                                                                     0.,                                                    0.,    1.0 ]  ]
        return OutArray

    def TransMatrixEulerAnglesZYZReverse(self,Din):
        OutArray = np.zeros([6])
        OutArray[0] = Din[0][3]
        OutArray[1] = Din[1][3]
        OutArray[2] = Din[2][3]
        if(Din[2][2] == 1.0):
            OutArray[4] = 0.
            OutArray[3] = 0.
            OutArray[5] = np.degrees(np.arctan2(-Din[0][1], Din[0][0]))
        elif(Din[2][0] == -1.0):
            OutArray[4] = 180.
            OutArray[3] = 0.
            OutArray[5] = np.degrees(np.arctan2(Din[0][1], -Din[0][0]))
        else:
            OutArray[4] = np.degrees(np.arctan2(np.sqrt((Din[2][0] ** 2) + (Din[2][1] ** 2)), Din[2][2]))
            OutArray[3] = np.degrees(np.arctan2( (Din[1][2] / np.sin(OutArray[4])), (Din[0][2] / np.sin(OutArray[4]))))
            OutArray[5] = np.degrees(np.arctan2( (Din[2][1] / np.sin(OutArray[4])), -(Din[2][0] / np.sin(OutArray[4]))))
        return OutArray

    def CheckLimitPermit(self,num,Din):         #Din7*4
        if(num):
            if(Din[num][3] >= Limit[num][0] and Din[num][3] <= Limit[num][1]):
                return 1
            else:
                #print("Input ",num," is denied.")
                return 0
        else:
            if(Din[num][2] >= Limit[num][0] and Din[num][3] <= Limit[num][1]):
                return 1
            else:
                #print("Input ",num," is denied.")
                return 0

    def CheckLimitPermit2(self,num,Din):        #Din 1*7, 1pos to Check
            if(Din[num] >= Limit[num][0] and Din[num] <= Limit[num][1]):
                return 1
            else:
                #print("Input ",num," is denied.")
                return 0

    def CheckLimitPermit3(self,Din):            #Din 1*7, all to Check
        for i in range(len(DH)):
            if(Din[i] < Limit[i][0] or Din[i] > Limit[i][1]):
                print("Par ",i," is denied.")
                print(Din)
                return 0
        return 1


    def IKFIxed7AxisCaculate(self,Din):
        IKFixed7AxisOutputSe = np.zeros([4,7])
        self.IKFixed7AxisOutputEmptyFlag = np.zeros([5])        #[4] = sum(0-3)
        for i in range(4):
            IKFixed7AxisOutputSe[i][0] = self.FKDHCache[0][2]
        self.IKFixed7AxisJoint0TransInv = np.linalg.inv(self.FKDHTrans[0])
        self.IKFixed7AxisJ1toJ6Trans = np.dot((np.dot(np.dot(self.WFTransInv,self.IKFixed7AxisJoint0TransInv),self.TransMatrixFixedAnglesXYZ(Din))),self.TFTransInv)
        IKFixed7AxisOutputSe[0][1] = np.degrees(np.arctan2(self.IKFixed7AxisJ1toJ6Trans[1][3],self.IKFixed7AxisJ1toJ6Trans[0][3]))
        for i in range(1,4):
            IKFixed7AxisOutputSe[i][1] = IKFixed7AxisOutputSe[0][1]
        HJ2toJ6 = self.IKFixed7AxisJ1toJ6Trans[2][3] - DH[1][2]
        LJ2toJ6 = np.sqrt((self.IKFixed7AxisJ1toJ6Trans[0][3] ** 2) + (self.IKFixed7AxisJ1toJ6Trans[1][3] ** 2)) - DH[1][1]
        HLJ2toJ6 = np.sqrt((HJ2toJ6 ** 2) + (LJ2toJ6 ** 2))
        HLJ3toJ6 = np.sqrt((DH[3][1] ** 2) + (DH[4][2] ** 2))       #366.7
        ThetaJ2toJ6 = np.degrees(np.arctan2(HJ2toJ6,LJ2toJ6))
        HLJ2toJ3 = DH[2][1]
        ThetaMidAtJ2 = np.degrees(np.arccos(((HLJ2toJ3 ** 2) + (HLJ2toJ6 ** 2) - (HLJ3toJ6 ** 2)) / (2 * HLJ2toJ3 * HLJ2toJ6)))
        ThetaMidAtJ3 = np.degrees(np.arccos(((HLJ2toJ3 ** 2) + (HLJ3toJ6 ** 2) - (HLJ2toJ6 ** 2)) / (2 * HLJ2toJ3 * HLJ3toJ6)))
        ThetaJ3AtTriangleofJ3toJ6 = np.degrees(np.arctan2(DH[3][1],DH[4][2]))
        IKFixed7AxisOutputSe[0][2] = -ThetaJ2toJ6 - ThetaMidAtJ2
        IKFixed7AxisOutputSe[1][2] = -ThetaJ2toJ6 - ThetaMidAtJ2
        IKFixed7AxisOutputSe[2][2] = -ThetaJ2toJ6 + ThetaMidAtJ2
        IKFixed7AxisOutputSe[3][2] = -ThetaJ2toJ6 + ThetaMidAtJ2
        IKFixed7AxisOutputSe[0][3] = 90 - ThetaMidAtJ3 + ThetaJ3AtTriangleofJ3toJ6
        IKFixed7AxisOutputSe[1][3] = 90 - ThetaMidAtJ3 + ThetaJ3AtTriangleofJ3toJ6
        IKFixed7AxisOutputSe[2][3] = -270 + ThetaMidAtJ3 + ThetaJ3AtTriangleofJ3toJ6
        IKFixed7AxisOutputSe[3][3] = -270 + ThetaMidAtJ3 + ThetaJ3AtTriangleofJ3toJ6
        for i in range(len(self.IKFixed7AxisJ4toJ6Trans)):
            self.IKFixed7AxisJ1toJ3Trans[i] = np.dot(np.dot(self.TransMatrixStandard([np.radians(DH[1][0]),DH[1][1],DH[1][2],np.radians(IKFixed7AxisOutputSe[2*i][1])]),self.TransMatrixStandard([np.radians(DH[2][0]),DH[2][1],DH[2][2],np.radians(IKFixed7AxisOutputSe[2*i][2])])),self.TransMatrixStandard([np.radians(DH[3][0]),DH[3][1],DH[3][2],np.radians(IKFixed7AxisOutputSe[2*i][3])]))
            self.IKFixed7AxisJ4toJ6Trans[i] = np.dot(np.linalg.inv(self.IKFixed7AxisJ1toJ3Trans[i]),self.IKFixed7AxisJ1toJ6Trans)
            IKJ4toJ6InvTmp = self.TransMatrixEulerAnglesZYZReverse(self.IKFixed7AxisJ4toJ6Trans[i])
            IKFixed7AxisOutputSe[2*i][4] = IKJ4toJ6InvTmp[3]
            IKFixed7AxisOutputSe[2*i][5] = IKJ4toJ6InvTmp[4]
            IKFixed7AxisOutputSe[2*i][6] = IKJ4toJ6InvTmp[5]
            IKFixed7AxisOutputSe[2*i+1][4] = (IKJ4toJ6InvTmp[3]-180) if (IKJ4toJ6InvTmp[3]>0) else (IKJ4toJ6InvTmp[3]+180)
            IKFixed7AxisOutputSe[2*i+1][5] = -IKJ4toJ6InvTmp[4]
            IKFixed7AxisOutputSe[2*i+1][6] = (IKJ4toJ6InvTmp[5]-180) if (IKJ4toJ6InvTmp[5]>0) else (IKJ4toJ6InvTmp[5]+180)    
        for i in range(len(IKFixed7AxisOutputSe)):
            if( self.CheckLimitPermit3(IKFixed7AxisOutputSe[i]) == 0):
                IKFixed7AxisOutputSe[i] = np.zeros([7])
                self.IKFixed7AxisOutputEmptyFlag[i] = 1
                self.IKFixed7AxisOutputEmptyFlag[len(IKFixed7AxisOutputSe)] += 1
        return IKFixed7AxisOutputSe

    def __init__(self):
        self.FKDHCache = deepcopy(DH)
        for i in range(len(DH)):
            self.FKDHCache[i][0] = np.radians(DH[i][0])
            self.FKDHCache[i][3] = np.radians(DH[i][3])
            self.FKDHTrans[i] = self.TransMatrixStandard(self.FKDHCache[i])
        self.WFTrans  = self.TransMatrixFixedAnglesXYZ(WF)
        self.TFTrans  = self.TransMatrixFixedAnglesXYZ(TF)
        self.WFTransInv = np.linalg.inv(self.WFTrans)
        self.TFTransInv = np.linalg.inv(self.TFTrans)
        self.FKTransResult = deepcopy(self.WFTrans)
        for i in range(len(DH)):
            self.FKTransResult = np.dot(self.FKTransResult, self.FKDHTrans[i])
        self.FKTransResult = np.dot(self.FKTransResult, self.TFTrans)
        self.FKOutput = self.TransMatrixFixedAnglesXYZReverse(self.FKTransResult)
        #print("initFKOutput \n",self.FKOutput)
        self.IKFixed7AxisOutput = self.IKFIxed7AxisCaculate(self.FKOutput)
        #print("initIKOutput \n",self.IKFixed7AxisOutput)

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

    def RefreshIKRelative(self,IKInputRelativeRe):
        self.IKFixed7AxisIntput = [self.IKFixed7AxisIntput[i] + IKInputRelativeRe[i] for i in range(len(IKInputRelativeRe))]
        self.IKFixed7AxisOutput = self.IKFIxed7AxisCaculate(self.IKFixed7AxisIntput)
        if(self.IKFixed7AxisOutputEmptyFlag[len(self.IKFixed7AxisOutput)] > 3):
            self.IKFixed7AxisIntput = [self.IKFixed7AxisIntput[i] - IKInputRelativeRe[i] for i in range(len(IKInputRelativeRe))]
        return self.IKFixed7AxisOutput

    def RefreshIKAbsolute(self,IKInputAbsoluteRe):
        self.IKFixed7AxisOutput = self.IKFIxed7AxisCaculate(IKInputAbsoluteRe)
        if(self.IKFixed7AxisOutputEmptyFlag[len(self.IKFixed7AxisOutput)] < 4):
            self.IKFixed7AxisIntput  = IKInputAbsoluteRe
        return self.IKFixed7AxisOutput

    

    def GetFKOutput(self):
        return self.FKOutput

    def GetIKFixed7AxisOutput(self):
        return self.IKFixed7AxisOutput


if __name__ == '__main__':
    kin = Zsx_kinematics()
    print("new FK\n",kin.RefreshFKAbsolute([0,-8.04,-119.04,54.65,0,64.76,-188.03]))
    print("new IK\n",kin.RefreshIKAbsolute(kin.GetFKOutput()))
    #print("new IK\n",kin.RefreshIKAbsolute([492.52,-69.54,651.84,0.,0.,180.]))
    #print("new2 IK\n",kin.RefreshIKAbsolute([494.0594,-69.7873,649.7911,89.99,-0.05169,0.36637]))
    #print("new2 FK\n",kin.RefreshFKAbsolute([0,-8.04,21.50366,-212.7419,-0.0,168.3918,-171.9698]))
    #print("new3 FK\n",kin.RefreshFKAbsolute([0,-8.04,-119.04,54.65,0,64.76,-171.9698]))