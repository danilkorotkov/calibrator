# -*- coding: utf-8 -*-
import numpy
import sys, spidev, os, time, string
from PyQt4 import QtCore, QtGui, uic 
from PyQt4.Qt import Qt
from PyQt4.QtGui import *
from PyQt4.QtCore import QObject, SIGNAL

MainInterfaceWindow = "calibrator.ui" 
Ui_Calibrator, QtBaseClass = uic.loadUiType(MainInterfaceWindow)

class Calibrator ( QtGui.QMainWindow, Ui_Calibrator ):
    """Calibrator inherits QMainWindow"""
    
    a = {
    'start_prog1':1,
    'start_prog2':1,
    'OH_ctrl_1':1,
    'OH_ctrl_2':1,
    'sensor1_1':1,
    'sensor1_2':1,
    'sensor2_1':1,
    'sensor2_2':1,
    'Fan1_Allow':1,
    'Fan2_Allow':1,
    'Channel1':[3.5708,5.3255,319.73,249.65],
    'Channel2':[3.5708,5.3255,319.73,249.65],
    'Channel3':[3.5708,5.3255,319.73,249.65],
    'Channel4':[3.5708,5.3255,319.73,249.65],
    'Channel5':[3.5708,5.3255,319.73,249.65],
    'Channel6':[3.5708,5.3255,319.73,249.65],
    'Counter1':0,
    'Counter2':0}
    
    def __init__ ( self, parent = None ):
        super(Calibrator, self).__init__(parent)
        Ui_Calibrator.__init__(self)
        self.setupUi( self )
        self.move(463, 345)
        self.pushButton.pressed.connect(self.test1)
        self.Exit.pressed.connect(self.close)

    def __del__ ( self ):
        self.ui = None

    def test1(self):
        self.textEdit.setText("")
        xy=[[0.766,0.0],[1.2775,174.95],[1.5347,266.5],[2.3016,558,001]]
        A=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        
        a6=0
        a5=0
        a4=0
        a3=0
        a2=0
        a1=0
        a0=0
        b3=0
        b2=0
        b1=0
        b0=0
        
        for i in range(len(xy)):
            a6+=xy[i][0]**6
            a5+=xy[i][0]**5
            a4+=xy[i][0]**4
            a3+=xy[i][0]**3
            a2+=xy[i][0]**2
            a1+=xy[i][0]
            a0+=1.0
            b3+=xy[i][1]*xy[i][0]**3
            b2+=xy[i][1]*xy[i][0]**2
            b1+=xy[i][1]*xy[i][0]
            b0+=xy[i][1]
            
        A[0][0]=a6
        A[0][1]=a5
        A[0][2]=a4
        A[0][3]=a3
        
        A[1][0]=a5
        A[1][1]=a4
        A[1][2]=a3
        A[1][3]=a2

        A[2][0]=a4
        A[2][1]=a3
        A[2][2]=a2
        A[2][3]=a1

        A[3][0]=a3
        A[3][1]=a2
        A[3][2]=a1
        A[3][3]=a0
#In [1]: import numpy
#In [2]: M = [[1, 2], [3, 4]]
        #print numpy.linalg.det(A)
#Out[3]: -2.0000000000000004        
        detA=numpy.linalg.det(A)
        if detA != 0.0:
            #print A
            
            B3=A[:]
            B3[0][0]=b3
            B3[1][0]=b2
            B3[2][0]=b1
            B3[3][0]=b0
            #print B3
            #print A
            detB3=numpy.linalg.det(B3)
            A3=detB3/detA
            print A3
            B3[0][0]=a6
            B3[1][0]=a5
            B3[2][0]=a4
            B3[3][0]=a3
            B2=A[:]
            B2[0][1]=b3
            B2[1][1]=b2
            B2[2][1]=b1
            B2[3][1]=b0
            detB2=numpy.linalg.det(B2)
            A2=detB2/detA
            print A2
            B2[0][1]=a5
            B2[1][1]=a4
            B2[2][1]=a3
            B2[3][1]=a2
            B1=A[:]
            B1[0][2]=b3
            B1[1][2]=b2
            B1[2][2]=b1
            B1[3][2]=b0
            detB1=numpy.linalg.det(B1)
            A1=detB1/detA
            print A1
            B1[0][2]=a4
            B1[1][2]=a3
            B1[2][2]=a2
            B1[3][2]=a1
            B0=A[:]
            B0[0][3]=b3
            B0[1][3]=b2
            B0[2][3]=b1
            B0[3][3]=b0
            detB0=numpy.linalg.det(B0)
            A0=detB0/detA
            print A0
        
        self.textEdit.setText(
                "%.4fx" % A3+'\xB3'+self.sign(A2) + \
                "%.4fx" % abs(A2)+'\xB2'+self.sign(A1) + \
                "%.4fx" % abs(A1)+self.sign(A0) + \
                "%.4f" % abs(A0))

    def sign(self, tempor):
        if tempor>=0:
            out='+'
        else:
            out='-'
        return out