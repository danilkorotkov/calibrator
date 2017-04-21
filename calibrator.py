# -*- coding: utf-8 -*-
import numpy
import sys, spidev, os, time, string
from PyQt4 import QtCore, QtGui, uic 
from PyQt4.Qt import Qt
from PyQt4.QtGui import *
from PyQt4.QtCore import QObject, SIGNAL
import RPi.GPIO as GPIO

MainInterfaceWindow = "calibrator.ui" 
Ui_Calibrator, QtBaseClass = uic.loadUiType(MainInterfaceWindow)
#-------------GPIO---------------
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

A=21
B=20
C=16
OEBuff=23
Fan2=24
Fan1=25
SSRPwm0=12
SSRPwm1=13
Freq=2
sets={}
FI=300
FT=15

Mux=(C,B,A)
spi = spidev.SpiDev()

#--------------------ADC Thread-------------
class TempThread(QtCore.QThread): # работа с АЦП в потоке 
    def __init__(self, temp_signal, parent=None):
        super(TempThread, self).__init__(parent)
        self.temp_signal = temp_signal
        self.isRun=False
        self.Va=0
        self.SetChannel(1)

    def run(self):
        while self.isRun:
            self.Va=self.GetADC()
            self.temp_signal.emit(self.Va)
            time.sleep(1)

    def stop(self):
        self.isRun=False

    def GetADC(self): #все названия сохранены на языке автора функции
        M0 =0 
        muestras =0
        while muestras <= 49:
            adc = spi.xfer2([0, 0])
            hi = (adc[0] & 0x1F);
            low = (adc[1] & 0xFC);#FE for B, FC for C chip (MCP3201-B/C) ©Danil
            dato = (hi << 8) | low;
            M0 += dato
            muestras += 1
        dato = M0/50
        V = long(dato) * 2.5 / 8192.0;    
        return V

    def SetChannel(self,Ch):
        if Ch >= 1 or Ch <= 6:
            A=Ch>>2
            B=(Ch>>1) & 1
            C=Ch & 1
            GPIO.output(Mux,(A,B,C))



class Calibrator ( QtGui.QMainWindow, Ui_Calibrator ):
    """Calibrator inherits QMainWindow"""
    temp_signal = QtCore.pyqtSignal(float)
    
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
    #Volts=[[value, IsSet],[value, IsSet],[value, IsSet],[value, IsSet]]
    Volts=[[0, 0],[0, 0],[0, 0],[0, 0]]
    C=1
    R=0
    lineCalcked=0
    Va=0
    isItStart=0
    
    def __init__ ( self, parent = None ):
        super(Calibrator, self).__init__(parent)
        Ui_Calibrator.__init__(self)
        self.setupUi( self )
        self.move(300, 50)
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.set_adc()
        self.Exit.pressed.connect(self.close)
        self.pBtn_Channel_1.setStyleSheet(CellSelect)
        self.R0.setStyleSheet(CellSelect)

        self.R0.pressed.connect(self.RB)
        self.R1.pressed.connect(self.RB)
        self.R2.pressed.connect(self.RB)
        self.R3.pressed.connect(self.RB)

        self.pBtn_Channel_1.clicked.connect(self.changeRow)
        self.pBtn_Channel_2.clicked.connect(self.changeRow)
        self.pBtn_Channel_3.clicked.connect(self.changeRow)        
        self.pBtn_Channel_4.clicked.connect(self.changeRow)
        self.pBtn_Channel_5.clicked.connect(self.changeRow)
        self.pBtn_Channel_6.clicked.connect(self.changeRow)

        self.pushButton_2.pressed.connect(self.Get_Volts)
        self.pushButton_3.pressed.connect(self.Calc)

        
    def __del__ ( self ):
        self.ui = None


#----------------------methods-------------------------------
    def changeRow(self):
        sender=self.sender()
        name=sender.objectName()
        s=len(name)

        if self.isItStart==0:
            getattr(self, 'lineEdit_'+str((self.C-1)*4 +self.R +1)).setStyleSheet(CellWait)
            getattr(self, 'pBtn_Channel_'+str(self.C)).setStyleSheet(CellWait)
            self.C=int(name[s-1])
            self.tempthread.SetChannel(self.C)
            sender.setStyleSheet(CellSelect)
            return
        elif self.checkRow() & self.lineCalcked == 0:
            self.textEdit.setText(u'Не все ячейки записаны или калибровка не посчитана')
            self.textEdit.setAlignment(Qt.AlignCenter)
            self.GroupChannel.checkedButton().setChecked(False)
            getattr(self, 'pBtn_Channel_'+str(self.C)).setChecked(True)
            return
        
        getattr(self, 'pBtn_Channel_'+str(self.C)).setStyleSheet(CellWait)
        self.C=int(name[s-1])
        self.lineCalcked=0
        sender.setStyleSheet(CellSelect)

    def checkRow(self):
        out=self.Volts[0][1] & self.Volts[1][1] & self.Volts[2][1] & self.Volts[3][1] 
        return out
        

    def got_worker_msg(self, Va):#ловля сигнала от АЦП
        self.Va=Va
        getattr(self, 'lineEdit_'+str((self.C-1)*4 +self.R +1)).setText('')
        getattr(self, 'lineEdit_'+str((self.C-1)*4 +self.R +1)).setText("%.4f"%self.Va)
        if not self.Volts[self.R][1]:
            getattr(self, 'lineEdit_'+str((self.C-1)*4 +self.R +1)).setStyleSheet(CellSelect)


    def set_adc(self):#запуск ацп в потоке
        GPIO.setup(Mux, GPIO.OUT)
        GPIO.output(Mux,(0,0,0))

        spi.open(0,0)
        spi.max_speed_hz = 40000
        self.tempthread=TempThread(self.temp_signal)
        self.temp_signal.connect(self.got_worker_msg, QtCore.Qt.QueuedConnection)
        self.tempthread.isRun=True
        self.tempthread.start()



    def Calc(self):
        if self.checkRow() == 0:
            self.textEdit.setText(u'Не все ячейки записаны')
            self.textEdit.setAlignment(Qt.AlignCenter)
            return
        self.lineCalcked=1
        self.isItStart=0
        
        for x in range(4):
            self.Volts[x][1]=0
        self.test1()
    

    def Get_Volts(self):
        self.isItStart=1
        self.Volts[self.R][1]=True
        self.Volts[self.R][0]=float(self.Va)
        self.textEdit.setText(u'Записано '+"%.4f"%self.Va)
        self.textEdit.setAlignment(Qt.AlignCenter)
        getattr(self, 'lineEdit_'+str((self.C-1)*4 +self.R +1)).setStyleSheet(CellStored)
        
        
    def test1(self):
        self.textEdit.setText("")

        A=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        xy=[[0,0],[0,0],[0,0],[0,0]]
        
        xy[0][0]=self.Volts[0][0]
        xy[1][0]=self.Volts[1][0]
        xy[2][0]=self.Volts[2][0]
        xy[3][0]=self.Volts[3][0]
        
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
        
            Chann='Channel'+str(self.C)
            self.a[Chann][0]=self.A3
            self.a[Chann][1]=self.A2
            self.a[Chann][2]=self.A1
            self.a[Chann][3]=self.A0
            
            self.textEdit.setText(
                "%.4fx" % self.A3+'\xB3'+self.sign(self.A2) + \
                "%.4fx" % abs(self.A2)+'\xB2'+self.sign(self.A1) + \
                "%.4fx" % abs(self.A1)+self.sign(self.A0) + \
                "%.4f" % abs(self.A0))
        else:
            self.textEdit.setText('detA=0')
        self.textEdit.setAlignment(Qt.AlignCenter)
        
        getattr(self, 'lineEdit_'+str((self.C-1)*4 + 0+1)).setStyleSheet(CellWait)
        getattr(self, 'lineEdit_'+str((self.C-1)*4 + 1+1)).setStyleSheet(CellWait)
        getattr(self, 'lineEdit_'+str((self.C-1)*4 + 2+1)).setStyleSheet(CellWait)
        getattr(self, 'lineEdit_'+str((self.C-1)*4 + 3+1)).setStyleSheet(CellWait)

    def sign(self, tempor):
        if tempor>=0:
            out='+'
        else:
            out='-'
        return out
        
    def RB(self):
        sender=self.sender()
        name=sender.objectName()
        s=len(name)
        sender.setStyleSheet(CellSelect)
        getattr(self, 'R'+str(self.R)).setStyleSheet(CellWait)
        if not self.Volts[self.R][1]:
            getattr(self, 'lineEdit_'+str((self.C-1)*4 +self.R +1)).setStyleSheet(CellWait)
        
        self.R=int(name[s-1])
#---------------------------StyleSheet---------------------------------------
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
        

CellWait=_fromUtf8("font: 22pt \"HelveticaNeueCyr\";\n"
"background-color: rgb(114, 208, 244);")

CellSelect=_fromUtf8("font: 22pt \"HelveticaNeueCyr\";\n"
"background-color: rgb(231, 126, 35);")

CellStored=_fromUtf8("font: 22pt \"HelveticaNeueCyr\";\n"
"background-color: rgb(63, 179, 79);")