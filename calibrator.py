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
    A3=0
    A2=0
    A1=0
    A0=0
    Volts=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    
    def __init__ ( self, parent = None ):
        super(Calibrator, self).__init__(parent)
        Ui_Calibrator.__init__(self)
        self.setupUi( self )
        self.move(463, 345)
        self.setWindowModality(QtCore.Qt.WindowModal)
        #self.pushButton.pressed.connect(self.test1)
        self.Exit.pressed.connect(self.close)
        self.pBtn_Channel_1.pressed.connect(self.Btn1)
        self.pBtn_Channel_2.pressed.connect(self.Btn2)
        self.pBtn_Channel_3.pressed.connect(self.Btn3)
        self.pBtn_Channel_4.pressed.connect(self.Btn4)
        self.pBtn_Channel_5.pressed.connect(self.Btn5)
        self.pBtn_Channel_6.pressed.connect(self.Btn6)
        self.pushButton_2.pressed.connect(self.Get_Volts)
        self.pushButton_3.pressed.connect(self.Calc)
        #self.test1()
        self.Show_Volts()
        
    def __del__ ( self ):
        self.ui = None

    def init(self):
        pass
#        for p in range(1,7):
#            for i in range (4):
#                getattr(self, 'listWidget_'+ str(p)).addItem(str(self.a['Channel'+str(p)][i]))

    def Calc(self):
        if self.pBtn_Channel_1.isChecked():
            self.test1(0)
        elif self.pBtn_Channel_2.isChecked():
            self.test1(1)
        elif self.pBtn_Channel_3.isChecked():
            self.test1(2)
        elif self.pBtn_Channel_4.isChecked():
            self.test1(3)
        elif self.pBtn_Channel_5.isChecked():
            self.test1(4)
        elif self.pBtn_Channel_6.isChecked():
            self.test1(5)
        else:
            pass


    def Show_Volts(self):
        self.lineEdit_1.setText(str(self.Volts[0][0]))
        self.lineEdit_2.setText(str(self.Volts[0][1]))
        self.lineEdit_3.setText(str(self.Volts[0][2]))
        self.lineEdit_4.setText(str(self.Volts[0][3]))
        self.lineEdit_5.setText(str(self.Volts[1][0]))
        self.lineEdit_6.setText(str(self.Volts[1][1]))
        self.lineEdit_7.setText(str(self.Volts[1][2]))
        self.lineEdit_8.setText(str(self.Volts[1][3]))
        self.lineEdit_9.setText(str(self.Volts[2][0]))
        self.lineEdit_10.setText(str(self.Volts[2][1]))
        self.lineEdit_11.setText(str(self.Volts[2][2]))
        self.lineEdit_12.setText(str(self.Volts[2][3]))
        self.lineEdit_13.setText(str(self.Volts[3][0]))
        self.lineEdit_14.setText(str(self.Volts[3][1]))
        self.lineEdit_15.setText(str(self.Volts[3][2]))
        self.lineEdit_16.setText(str(self.Volts[3][3]))
        self.lineEdit_17.setText(str(self.Volts[4][0]))
        self.lineEdit_18.setText(str(self.Volts[4][1]))
        self.lineEdit_19.setText(str(self.Volts[4][2]))
        self.lineEdit_20.setText(str(self.Volts[4][3]))
        self.lineEdit_21.setText(str(self.Volts[5][0]))
        self.lineEdit_22.setText(str(self.Volts[5][1]))
        self.lineEdit_23.setText(str(self.Volts[5][2]))
        self.lineEdit_24.setText(str(self.Volts[5][3]))

    def Get_Volts(self):
        self.Volts[0][0]=float(self.lineEdit_1.text())
        self.Volts[0][1]=float(self.lineEdit_2.text())
        self.Volts[0][2]=float(self.lineEdit_3.text())
        self.Volts[0][3]=float(self.lineEdit_4.text())
        self.Volts[1][0]=float(self.lineEdit_5.text())
        self.Volts[1][1]=float(self.lineEdit_6.text())
        self.Volts[1][2]=float(self.lineEdit_7.text())
        self.Volts[1][3]=float(self.lineEdit_8.text())
        self.Volts[2][0]=float(self.lineEdit_9.text())
        self.Volts[2][1]=float(self.lineEdit_10.text())
        self.Volts[2][2]=float(self.lineEdit_11.text())
        self.Volts[2][3]=float(self.lineEdit_12.text())
        self.Volts[3][0]=float(self.lineEdit_13.text())
        self.Volts[3][1]=float(self.lineEdit_14.text())
        self.Volts[3][2]=float(self.lineEdit_15.text())
        self.Volts[3][3]=float(self.lineEdit_16.text())
        self.Volts[4][0]=float(self.lineEdit_17.text())
        self.Volts[4][1]=float(self.lineEdit_18.text())
        self.Volts[4][2]=float(self.lineEdit_19.text())
        self.Volts[4][3]=float(self.lineEdit_20.text())
        self.Volts[5][0]=float(self.lineEdit_21.text())
        self.Volts[5][1]=float(self.lineEdit_22.text())
        self.Volts[5][2]=float(self.lineEdit_23.text())
        self.Volts[5][3]=float(self.lineEdit_24.text())
        
        self.Show_Volts()
        
    def test1(self, x):
        self.textEdit.setText("")
        xy=[[0.766,0.0],[1.2775,174.95],[1.5347,266.5],[2.3016,558,001]]
        A=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        
        xy[0][0]=self.Volts[x][0]
        xy[1][0]=self.Volts[x][1]
        xy[2][0]=self.Volts[x][2]
        xy[3][0]=self.Volts[x][3]
        
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
            self.A3=detB3/detA
            #print A3
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
            self.A2=detB2/detA
            #print A2
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
            self.A1=detB1/detA
            #print A1
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
            self.A0=detB0/detA
            #print A0
        
            if x==0:
                self.a['Channel1'][0]=self.A3
                self.a['Channel1'][1]=self.A2
                self.a['Channel1'][2]=self.A1
                self.a['Channel1'][3]=abs(self.A0)
            elif x==1:    
                self.a['Channel2'][0]=self.A3
                self.a['Channel2'][1]=self.A2
                self.a['Channel2'][2]=self.A1
                self.a['Channel2'][3]=abs(self.A0)
            elif x==2:
                self.a['Channel3'][0]=self.A3
                self.a['Channel3'][1]=self.A2
                self.a['Channel3'][2]=self.A1
                self.a['Channel3'][3]=abs(self.A0)
            elif x==3:
                self.a['Channel4'][0]=self.A3
                self.a['Channel4'][1]=self.A2
                self.a['Channel4'][2]=self.A1
                self.a['Channel4'][3]=abs(self.A0)
            elif x==4:
                self.a['Channel5'][0]=self.A3
                self.a['Channel5'][1]=self.A2
                self.a['Channel5'][2]=self.A1
                self.a['Channel5'][3]=abs(self.A0)
            elif x==5:
                self.a['Channel6'][0]=self.A3
                self.a['Channel6'][1]=self.A2
                self.a['Channel6'][2]=self.A1
                self.a['Channel6'][3]=abs(self.A0)
            else:
                pass
                
        
            self.textEdit.setText(
                "%.4fx" % self.A3+'\xB3'+self.sign(self.A2) + \
                "%.4fx" % abs(self.A2)+'\xB2'+self.sign(self.A1) + \
                "%.4fx" % abs(self.A1)+self.sign(self.A0) + \
                "%.4f" % abs(self.A0))
        else:
            self.textEdit.setText('detA=0')
        self.textEdit.setAlignment(Qt.AlignCenter)

    def sign(self, tempor):
        if tempor>=0:
            out='+'
        else:
            out='-'
        return out
        
    def Btn1(self):
        pass
        
    def Btn2(self):
        pass
        
    def Btn3(self):
        pass
        
    def Btn4(self):
        pass
        
    def Btn5(self):
        pass
        
    def Btn6(self):
        pass
        
        