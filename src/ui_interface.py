# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'HorusNewjrlSeY.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from msilib.schema import ListView
from re import S
from lie import DeceptionDetectionVoice
from VideoThread import ScreenCaptureThread, VideoMultiThread, VideoSingleThread, LieDetectionThread, View_Analysis
import PyQt5
from PyQt5 import QtTest
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog
from functools import partial
import cv2
import time
import pickle
import os
import startscreen_rc
try:
    from PyQt5.QtChart import QChartView, QChart, QBarSet, QBarSeries, QBarCategoryAxis, QPercentBarSeries, QPieSeries, QLineSeries
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QPainter
    from PyQt5.QtWidgets import QApplication
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtGui import QPainter
    from PySide2.QtWidgets import QApplication
    from PySide2.QtCharts import QtCharts
    QChartView = QtCharts.QChartView
    QChart = QtCharts.QChart
    QBarSet = QtCharts.QBarSet
    QBarSeries = QtCharts.QBarSeries
    QBarCategoryAxis = QtCharts.QBarCategoryAxis


class Ui_MainWindow(object):
    def __init__(self):
        self.voicePreds = None
        self.decVidResult = None
        self.thread_specific_anal = []
        self.comingFrom = None
                
    def on_click_to_menu(self, sender):
        self.stackedWidget.setCurrentIndex(1)
        if sender == "back_button_6":
            self.videoSingleThread.stop()
        elif sender == "back_button_5":
            self.multiThread.stop_threads()
        elif sender == "back_button_4":
            try: 
                self.deceptionThread.stop()
                self.deceptionDetectionVoice.stop()
                self.leftCounterLabel.setText(QCoreApplication.translate("Horus", u"28", None))
                self.rightCounterLabel.setText(QCoreApplication.translate("Horus", u"28", None))
            except:
                pass
        elif sender == "back_button_3":
            self.screenCapture.stop()
        elif sender == "back_button_2":
            self.comingFrom = None #sorun çıakrıyo mu test et
        
    def on_click_single_user(self):
        self.stackedWidget.setCurrentIndex(2)
        self.videoSingleThread = VideoSingleThread()
        self.videoSingleThread.start()
        self.videoSingleThread.ImageUpdate.connect(self.ImageUpdateSlot)
        self.videoSingleThread.ValChanged.connect(self.CameraCheckSlot)
        self.videoSingleThread.EmotionUpdate.connect(self.EmotionSlot)
        self.videoSingleThread.RandomSender.connect(self.RandomSlot)
        self.videoSingleThread.Analysis.connect(self.AnalysisSlot_2)
        self.p3_screen_label.setPixmap(QPixmap(u":/Horus Main Page/loading.png")) #bunu asağıdan aldık buraya koyduk herbirininkini al kendi butonuna koy
    
    def pauseVidBtn(self, sender):
        if sender == "pause_button":
            self.screenCapture.pause()
            self.screenCapScanLabel.setText(QCoreApplication.translate("Horus", u"PAUSED...", None))
        elif sender == "pause_button_2":
            self.multiThread.pause()
            self.scanLabelp4.setText(QCoreApplication.translate("Horus", u"PAUSED...", None))
        elif sender == "pause_button_3":
            self.videoSingleThread.pause()
            self.scanLabelp3.setText(QCoreApplication.translate("Horus", u"PAUSED...", None))
        
    def playVidBtn(self, sender):
        if sender == "play_button":
            self.screenCapture.play()
            self.screenCapScanLabel.setText(QCoreApplication.translate("Horus", u"SCANNING...", None))
        elif sender == "play_button_2":
            self.multiThread.play()
            self.scanLabelp4.setText(QCoreApplication.translate("Horus", u"SCANNING...", None))
        elif sender == "play_button_3":
            self.videoSingleThread.play()
            self.scanLabelp3.setText(QCoreApplication.translate("Horus", u"SCANNING...", None))
    
    def replayVidBtn(self):
        self.scanLabelp3.setText(QCoreApplication.translate("Horus", u"SCANNING...", None))
        self.videoSingleThread.replay()
    
    def on_click_list_analyses(self):
        self.namesInListSaved = self.list_saved_analysis()
        self.stackedWidget.setCurrentIndex(9)
        
    def on_click_crowd_control(self):
        self.p4_screen_label.setPixmap(QPixmap(u":/Horus Main Page/loading.png"))
        self.camCount = self.countCameras()
        print(self.camCount)
        ff = QFont("Times")
        ff.setPointSize(16)
        self.model = PyQt5.QtGui.QStandardItemModel()
        self.listView.setModel(self.model)
        
        for i in range(self.camCount):
            item = PyQt5.QtGui.QStandardItem()
            strr = "Camera " + str(i)
            item.setText(strr)
            item.setFont(ff)
            item.setEditable(False)
            item.setCheckable(True)
            self.model.appendRow(item)   
            
        if self.camCount == 0:
            item = PyQt5.QtGui.QStandardItem()
            item.setText("No Cameras Detected")
            item.setFont(ff)
            item.setEditable(False)
            self.model.appendRow(item)         
        self.stackedWidget.setCurrentIndex(8)
    
    def on_click_delete(self):
        dirpath = r'save_files'
        for index in self.listView_2.selectedIndexes():
            item = self.listView_2.model().itemFromIndex(index)
            fname = item.text()
        
        ind = self.namesInListSaved.index(fname)
        namesArr = []
        for root, dirs, files in os.walk(dirpath):
            for file in files:
                namesArr.append(file)
        arrfilename = "save_files/" + namesArr[ind]
        os.chmod(arrfilename, int('0777'))
        os.remove(arrfilename)
        if namesArr[ind][0] == "C":
            vidfilename = namesArr[ind][18:]
        elif namesArr[ind][0] == "M":
            vidfilename = namesArr[ind][16:]
        else:
            vidfilename = namesArr[ind][17:]
        vidfilename = "saved_videos/" + vidfilename
        os.chmod(vidfilename, int('0777'))
        os.remove(vidfilename)
    
    def on_click_view_saved(self):
        dirpath = r'save_files'
        for index in self.listView_2.selectedIndexes():
            item = self.listView_2.model().itemFromIndex(index)
            fname = item.text()
        try:
            ind = self.namesInListSaved.index(fname)
            namesArr = []
            for root, dirs, files in os.walk(dirpath):
                for file in files:
                    namesArr.append(file)
            filename = "save_files/" + namesArr[ind]
            with open(filename, 'rb') as f:
                if filename[0] == "C":
                    self.analysis_screen = pickle.load(f)
                    self.comingFrom = "Capture"
                    self.randomName = filename[18:]
                    print(self.randomName)
                elif filename[0] == "M":
                    self.total_analysis_multi = pickle.load(f)
                    self.comingFrom = "Multi"
                    self.randomName = filename[16:]
                    print(self.randomName)
                else:
                    self.analysis_single = pickle.load(f)
                    self.comingFrom = "Single"
                    self.randomName = filename[17:]
                    print(self.randomName)
            self.stackedWidget.setCurrentIndex(6)
        except:
            pass
        
    def list_saved_analysis(self):
        dirpath = r'save_files'
        namesArr = []
        for root, dirs, files in os.walk(dirpath):
            for file in files:
                namesArr.append(file)
        count = len(namesArr)
        arr = []        
        ff2 = QFont("Times")
        ff2.setPointSize(16)
        model = PyQt5.QtGui.QStandardItemModel()
        self.listView_2.setModel(model)
        
        single = 1
        multi = 1
        capture = 1
        for i in range(count):
            item = PyQt5.QtGui.QStandardItem()
            strr = namesArr[i]
            if strr[0] == "C":
                fname = "Capture Camera Mode Save " + str(capture)
                capture += 1
            elif strr[0] == "M":
                fname = "Multiple Camera Mode Save " + str(multi)
                multi += 1 
            else:
                fname = "Single Camera Mode Save " + str(single)
                single += 1 
            arr.append(fname)
            item.setText(fname)
            item.setFont(ff2)
            item.setEditable(False)
            #item.setCheckable(True)
            model.appendRow(item) 
            
        if count == 0:
            item = PyQt5.QtGui.QStandardItem()
            item.setText("No Save File Detected")
            item.setFont(ff2)
            item.setEditable(False)
            model.appendRow(item)         
        return arr  
                
    def on_click_change_cam(self):
        if self.multiThread.currentThread == (self.multiThread.threadCount - 1):
            self.multiThread.choose_thread(0)
            self.multiThread.currentThread = 0
            self.multiThread.getCurrentImageUpdate().connect(self.ImageUpdateSlot_2)#   ImageUpdate.connect(self.ImageUpdateSlot)
            self.multiThread.getCurrentValChanged().connect(self.CameraCheckSlot)
            print("Chosen camera 0")
        else:
            self.multiThread.choose_thread(self.multiThread.currentThread + 1)
            self.multiThread.currentThread += 1
            self.multiThread.getCurrentImageUpdate().connect(self.ImageUpdateSlot_2)#   ImageUpdate.connect(self.ImageUpdateSlot)
            self.multiThread.getCurrentValChanged().connect(self.CameraCheckSlot)
            print("Chosen camera ", self.multiThread.currentThread)
    
    def on_click_crowd_control_run(self):
        self.checkedCameraInds = []
        for index in range(self.model.rowCount()):
            item = self.model.item(index)
            isChecked = item.checkState()
            if isChecked:
                self.checkedCameraInds.append(index)
        if len(self.checkedCameraInds) > 0:
            self.multiThread = VideoMultiThread(self.checkedCameraInds)
            self.frame_multi = 0
            self.multiThread.RandomSender.connect(self.RandomSlot)
            self.multiThread.startThreads()
            self.multiThread.getCurrentImageUpdate().connect(self.ImageUpdateSlot_2)#   ImageUpdate.connect(self.ImageUpdateSlot)
            self.multiThread.getCurrentValChanged().connect(self.CameraCheckSlot)#   ValChanged.connect(self.CameraCheckSlot)
            
            self.multiThread.Analysis.connect(self.AnalysisSlot_3)
            self.multiThread.Thread_specific_anal.connect(self.AnalysisSlot_4)
            self.stackedWidget.setCurrentIndex(3)
            self.p4_screen_label.setPixmap(QPixmap(u":/Horus Main Page/loading.png"))
        else:
            print("No camera Selected")
            
    def on_click_deception_detection(self):        
        self.p5_screen_label.setPixmap(QPixmap(u":/Horus Main Page/clickstart.png"))
        self.stackedWidget.setCurrentIndex(4)
        
    def on_click_screen_capture(self):
        self.screenCapture = ScreenCaptureThread()
        self.screenCapture.start()
        self.screenCapture.ImageUpdate.connect(self.ImageUpdateSlot_3)
        self.screenCapture.ValChanged.connect(self.CameraCheckSlot)
        self.screenCapture.Analysis.connect(self.AnalysisSlot)
        self.screenCapture.RandomSender.connect(self.RandomSlot)
        self.screen_frame =0
        self.screenCapture.Real_time_analysis.connect(self.AnalysisSlot_5)
        self.p21_screen_label.setPixmap(QPixmap(u":/Horus Main Page/loading.png"))
        self.stackedWidget.setCurrentIndex(5)   
    
    def on_click_goto_result(self, sender):
        self.stackedWidget.setCurrentIndex(6)
        if sender == "back_button_10": #histogram page
            self.p7_histogramlayout.takeAt(0).widget().deleteLater()
        elif sender == "back_button_9":
            self.p6_pielayout.takeAt(0).widget().deleteLater()
        elif sender == "back_button_11":
            self.p8_donutlayout.takeAt(0).widget().deleteLater()
        elif sender == "back_button_12":
            self.p9_linelayout.takeAt(0).widget().deleteLater()
        elif sender == "back_button_13":
            self.videoPlayer.stop()
        elif sender == "pushButton_3":
            self.comingFrom = "Single"
            self.videoSingleThread.stop()
            fname = 'save_files/Single_' + self.randomName
            with open(fname, 'wb') as f:
                pickle.dump(self.analysis_single, f)
        elif sender == "pushButton_2":
            self.multiThread.stop_threads()
            self.comingFrom = "Multi"
            fname = 'save_files/Multi_' + self.randomName
            with open(fname, 'wb') as f:
                pickle.dump(self.total_analysis_multi, f)
        elif sender == "pushButton":
            self.screenCapture.stop()
            self.comingFrom = "Capture"
            fname = 'save_files/Capture_' + self.randomName
            with open(fname, 'wb') as f:
                pickle.dump(self.analysis_screen, f)      
    
    def on_click_pie_button(self):
        if self.comingFrom == "Single":
            anal = self.analysis_single
            analList = [element * 100 for element in anal]
            self.chartViewPieChart, self.seriesPieChart = self.drawPieChart(happy=analList[3], sad=analList[4], disgust=analList[1], anger=analList[0], neutral=analList[6], suprised=analList[5], fear=analList[2], width=1000, height=700)
        elif self.comingFrom == "Multi":
            anal = self.total_analysis_multi
            analList = [element * 100 for element in anal]
            self.chartViewPieChart, self.seriesPieChart = self.drawPieChart(happy=analList[3], sad=analList[4], disgust=analList[1], anger=analList[0], neutral=analList[6], suprised=analList[5], fear=analList[2], width=1000, height=700)
        elif self.comingFrom == "Capture":
            anal = self.analysis_screen
            analList = [element * 100 for element in anal]
            self.chartViewPieChart, self.seriesPieChart = self.drawPieChart(happy=analList[3], sad=analList[4], disgust=analList[1], anger=analList[0], neutral=analList[6], suprised=analList[5], fear=analList[2], width=1000, height=700)
        self.p6_pielayout.addWidget(self.chartViewPieChart, 0, Qt.AlignHCenter|Qt.AlignVCenter)   
        self.stackedWidget.setCurrentIndex(10)
        
    def on_click_histogram_button(self):
        if self.comingFrom == "Single":
            anal = self.analysis_single
            analList = [element * 100 for element in anal]
            self.chartViewBarChart, self.seriesBarChart = self.drawBarChart(happy=analList[3], sad=analList[4], disgust=analList[1], anger=analList[0], neutral=analList[6], suprised=analList[5], fear=analList[2], width=1000, height=600)
        elif self.comingFrom == "Multi":
            anal = self.total_analysis_multi
            analList = [element * 100 for element in anal]
            self.chartViewBarChart, self.seriesBarChart = self.drawBarChart(happy=analList[3], sad=analList[4], disgust=analList[1], anger=analList[0], neutral=analList[6], suprised=analList[5], fear=analList[2], width=1000, height=600)
        elif self.comingFrom == "Capture":
            anal = self.analysis_screen
            analList = [element * 100 for element in anal]
            self.chartViewBarChart, self.seriesBarChart = self.drawBarChart(happy=analList[3], sad=analList[4], disgust=analList[1], anger=analList[0], neutral=analList[6], suprised=analList[5], fear=analList[2], width=1000, height=600)
        self.p7_histogramlayout.addWidget(self.chartViewBarChart, 0, Qt.AlignHCenter|Qt.AlignVCenter)   
        self.stackedWidget.setCurrentIndex(11)
        
    def on_click_donut_button(self):
        if self.comingFrom == "Single":
            anal = self.analysis_single
            analList = [element * 100 for element in anal]
            self.chartViewDonutChart, self.seriesDonutChart = self.drawPieChart(happy=analList[3], sad=analList[4], disgust=analList[1], anger=analList[0], neutral=analList[6], suprised=analList[5], fear=analList[2], width=1000, height=700, donut = True)
        elif self.comingFrom == "Multi":
            anal = self.total_analysis_multi
            analList = [element * 100 for element in anal]
            self.chartViewDonutChart, self.seriesDonutChart = self.drawPieChart(happy=analList[3], sad=analList[4], disgust=analList[1], anger=analList[0], neutral=analList[6], suprised=analList[5], fear=analList[2], width=1000, height=700, donut = True)
        elif self.comingFrom == "Capture":
            anal = self.analysis_screen
            analList = [element * 100 for element in anal]
            self.chartViewDonutChart, self.seriesDonutChart = self.drawPieChart(happy=analList[3], sad=analList[4], disgust=analList[1], anger=analList[0], neutral=analList[6], suprised=analList[5], fear=analList[2], width=1000, height=700, donut = True)
        self.p8_donutlayout.addWidget(self.chartViewDonutChart, 0, Qt.AlignHCenter|Qt.AlignVCenter) 
        self.stackedWidget.setCurrentIndex(12)  
        
    def on_click_line_button(self):
        if self.comingFrom == "Single":
            anal = self.analysis_single
            analList = [element * 100 for element in anal]
            self.chartViewLineChart, self.seriesLineChart = self.drawLineChart(happy=analList[3], sad=analList[4], disgust=analList[1], anger=analList[0], neutral=analList[6], suprised=analList[5], fear=analList[2], width=1000, height=700)
        elif self.comingFrom == "Multi":
            anal = self.total_analysis_multi
            analList = [element * 100 for element in anal]
            self.chartViewLineChart, self.seriesLineChart = self.drawLineChart(happy=analList[3], sad=analList[4], disgust=analList[1], anger=analList[0], neutral=analList[6], suprised=analList[5], fear=analList[2], width=1000, height=700)
        elif self.comingFrom == "Capture":
            anal = self.analysis_screen
            analList = [element * 100 for element in anal]
            self.chartViewLineChart, self.seriesLineChart = self.drawLineChart(happy=analList[3], sad=analList[4], disgust=analList[1], anger=analList[0], neutral=analList[6], suprised=analList[5], fear=analList[2], width=1000, height=700)
        self.p9_linelayout.addWidget(self.chartViewLineChart, 0, Qt.AlignHCenter|Qt.AlignVCenter) 
        self.stackedWidget.setCurrentIndex(13)
    
    # def on_click_table_button(self):
    #     self.stackedWidget.setCurrentIndex(14)
    #     if self.comingFrom == "Single":
    #         pass
    #     elif self.comingFrom == "Multi":
    #         pass
    #     elif self.comingFrom == "Capture":
    #         pass
        
    def on_click_view_data(self):
        self.videoPlayer = View_Analysis(fileName=self.randomName)
        self.videoPlayer.start()
        self.videoPlayer.ImageUpdate.connect(self.ImageUpdateSlot_videoplayer)
        self.stackedWidget.setCurrentIndex(15)
    
    def ImageUpdateSlot_videoplayer(self, Image):
        self.label_9.setPixmap(PyQt5.QtGui.QPixmap.fromImage(Image))
    
    def AnalysisSlot(self, anal):
        self.analysis_screen = anal
        print("last analy: ", self.analysis_screen) #Screen Capture Analysis
        
    def AnalysisSlot_5(self, anal):
        self.screen_frame += 1
        self.real_time_analysis_screen = [element * 100 for element in anal]
        print("Screen Capture Analysis: ", self.real_time_analysis_screen) #Real Time Screen Capture Analysis
        if self.screen_frame > 4:
            self.updateBarChart(self.seriesBarCapture, self.real_time_analysis_screen[3], self.real_time_analysis_screen[4], self.real_time_analysis_screen[1], self.real_time_analysis_screen[0], self.real_time_analysis_screen[6], self.real_time_analysis_screen[5], self.real_time_analysis_screen[2])
            self.screen_frame = 0
        
    def AnalysisSlot_2(self, anal):
        self.analysis_single = anal
        print("last analy: ", self.analysis_single) #Single User Analysis
    
    def AnalysisSlot_3(self, anal):
        self.total_analysis_multi = anal
        print("Total analysis from multi thread: ", self.total_analysis_multi) #Crowd Control Last Analysis
     
    def AnalysisSlot_4(self, thread_name, anal):
        self.frame_multi += 1
        self.thread_specific_anal = [element *100 for element in anal]
        #print("Real Time Analysis from thread: ",thread_name, " :", self.thread_specific_anal) #Real Time Thread Analysis, with Thread Name
        if self.frame_multi > 4:
            self.updateBarChart(self.seriesBarMulti, self.thread_specific_anal[3], self.thread_specific_anal[4], self.thread_specific_anal[1], self.thread_specific_anal[0], self.thread_specific_anal[6], self.thread_specific_anal[5], self.thread_specific_anal[2])
            self.frame_multi = 0
     
    def ImageUpdateSlot(self, Image):
        self.p3_screen_label.setPixmap(PyQt5.QtGui.QPixmap.fromImage(Image))

    def ImageUpdateSlot_2(self, Image):
        self.p4_screen_label.setPixmap(PyQt5.QtGui.QPixmap.fromImage(Image))
        
    def ImageUpdateSlot_3(self, Image):
        self.p21_screen_label.setPixmap(PyQt5.QtGui.QPixmap.fromImage(Image))
    
    def ImageUpdateSlot_dec(self, Image):
        self.p5_screen_label.setPixmap(PyQt5.QtGui.QPixmap.fromImage(Image))
    
    def CameraCheckSlot(self, val):
        if val == 1:
            stt = u":/Horus Main Page/nocam.png"
        self.p3_screen_label.setPixmap(QPixmap(stt))
        self.p4_screen_label.setPixmap(QPixmap(stt))
        self.p5_screen_label.setPixmap(QPixmap(stt))
        self.p21_screen_label.setPixmap(QPixmap(stt))
        
    def RandomSlot(self, rand):
        self.randomName = rand
        print(self.randomName)
        
    def EmotionSlot(self, emotion):
        if len(emotion) == 0:
            angry, disgust, fear, happy, sad, suprised, neutral = 0,0,0,0,0,0,0
        else:
            angry, disgust, fear, happy, sad, suprised, neutral = emotion[0][0],emotion[0][1],emotion[0][2],emotion[0][3],emotion[0][4],emotion[0][5],emotion[0][6]
            self.updateBarChart(self.seriesBarSingle, happy, sad, disgust, angry, neutral, suprised, fear)
            
    def EmotionSlot_deception(self, decVidResult):
        self.decVidResult = decVidResult
        print(self.decVidResult)
        self.finishDeceptionControl()
        
    def VoiceUpdateSlot(self, voicePreds):
        self.voicePreds = voicePreds
        print(self.voicePreds)
        self.finishDeceptionControl()
    
    def finishDeceptionControl(self):
        if self.decVidResult != None and self.voicePreds != None:
            if abs(self.voicePreds[0][0][1] - self.voicePreds[0][0][0]) <= 0.2:
                lie = self.decVidResult
            else:
                lie = self.voicePreds[1][0]
            # contrib = 0.2 if self.decVidResult else 0 #May change the coef
            # lie = True if (self.voicePreds[0][0][1] * 0.80 + contrib) >= 0.70 else False
            if lie:
                self.p5_screen_label.setPixmap(QPixmap(u":/Horus Main Page/lie.png"))
            else:
                self.p5_screen_label.setPixmap(QPixmap(u":/Horus Main Page/truth.png"))
            self.detectionStartButton.setEnabled(True)
    def countCameras(self):
        camera = 0
        while True:
            if (cv2.VideoCapture(camera,cv2.CAP_DSHOW).grab()) is True:
                camera = camera + 1
            else:
                cv2.destroyAllWindows()
                return(int(camera))        
    
    def on_click_upload(self):
        self.pauseVidBtn("pause_button_3")
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(None,"Select Video File", "","Video File (*.mp4 *.avi *.mov *.mpeg *.flv *.wmv)", options=options)
        if filePath != "":
            self.videoSingleThread.open(filePath)
    
    def start_deception_Detection(self):
        self.deceptionThread = LieDetectionThread()
        self.deceptionThread.start()
        self.deceptionThread.ImageUpdate.connect(self.ImageUpdateSlot_dec)
        self.deceptionThread.ValChanged.connect(self.CameraCheckSlot)
        self.deceptionThread.EmotionUpdate.connect(self.EmotionSlot_deception)
        self.deceptionDetectionVoice = DeceptionDetectionVoice()
        self.deceptionDetectionVoice.start()
        self.deceptionDetectionVoice.LieVoiceResult.connect(self.VoiceUpdateSlot)
        # t = 28
        self.detectionStartButton.setEnabled(False)
        self.detectionLabel.setText(QCoreApplication.translate("Horus", u"Stand Still...", None))
        # while t:
        #     QtTest.QTest.qWait(1000)   u""+ str(t)
        self.leftCounterLabel.setText(QCoreApplication.translate("Horus", u"Listening|Recording", None))
        self.rightCounterLabel.setText(QCoreApplication.translate("Horus", u"Listening|Recording", None))
            # t -= 1
    
    def drawBarChart(self, happy=0, sad=0, disgust=0, anger=0, neutral=100, suprised=0, fear=0, width=600, height=500):
        set0 = QBarSet("Happy")
        set1 = QBarSet('Sad')
        set2 = QBarSet('Disgust')
        set3 = QBarSet('Angry')
        set4 = QBarSet('Neutral')
        set5 = QBarSet('Suprised')
        set6 = QBarSet('Fear')
        
        set0 << happy << 0 << 0 << 0 << 0 << 0 << 0
        set1 << 0 << sad << 0 << 0 << 0 << 0 << 0
        set2 << 0 << 0 << disgust << 0 << 0 << 0 << 0
        set3 << 0 << 0 << 0 << anger << 0 << 0 << 0
        set4 << 0 << 0 << 0 << 0 << neutral << 0 << 0
        set5 << 0 << 0 << 0 << 0 << 0 << suprised << 0
        set6 << 0 << 0 << 0 << 0 << 0 << 0 << fear
        
        series = QBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)
        series.append(set4)
        series.append(set5)
        series.append(set6)
        
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Emotions Bar Chart")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTheme(QChart.ChartThemeDark)
        categories = ["Happy", "Sad", "Disgust", "Angry", "Neutral", "Suprised", "Fear"]
        axis = QBarCategoryAxis()
        axis.append(categories)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)
        chartview = QChartView(chart)
        chartview.setMinimumHeight(height)
        chartview.setMinimumWidth(width)
        return chartview, series
    
    def drawPieChart(self, happy=0, sad=0, disgust=0, anger=0, neutral= 100, suprised=0, fear=0, width=600, height=500, donut=False):
        series = QPieSeries()
        arr = [happy, sad, disgust, anger, neutral, suprised, fear]
        maxone  = max(arr)
        maxind = arr.index(maxone)

        series.setPieSize(0.75)
        series.setLabelsVisible(True)
        if donut:
            series.setHoleSize(0.40)
        
        series.append("Happy", happy)
        series.append("Sad", sad)
        series.append("Disgust", disgust)
        series.append("Anger", anger)
        series.append("Neutral", neutral)
        series.append("Suprised", suprised)
        series.append("Fear", fear)
        
        mslice = series.slices()[maxind]
        mslice.setExploded(True)
        mslice.setLabelVisible(True)
        
        chart = QChart()
        chart.addSeries(series)
        if donut:
            chart.setTitle("Emotions Donut Chart")
        else:
            chart.setTitle("Emotions Pie Chart")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTheme(QChart.ChartThemeDark)
        #chart.setBackgroundBrush(QBrush(QColor("transparent")))
        chartview = QChartView(chart)
        chartview.setMinimumHeight(height)
        chartview.setMinimumWidth(width)
        return chartview, series
   
    def drawLineChart(self, happy=0, sad=0, disgust=0, anger=0, neutral= 100, suprised=0, fear=0, width=600, height=500):
        series = QLineSeries()
        series.append(10, happy)
        series.append(20, sad)
        series.append(30, disgust)
        series.append(40, anger)
        series.append(50, neutral)
        series.append(60, suprised)
        series.append(70, fear)
        series.setPointLabelsVisible(True)
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Emotions Line Chart")
        
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTheme(QChart.ChartThemeDark)
        #categories = ["Happy", "Sad", "Disgust", "Angry", "Neutral", "Suprised", "Fear"]
        #axis = QBarCategoryAxis()
        #axis.append(categories)
        chart.createDefaultAxes()
        #chart.setAxisX(axis, series)
        #series.attachAxis(axis)
        chart.legend().setVisible(True)
        chartview = QChartView(chart)
        chartview.setMinimumHeight(height)
        chartview.setMinimumWidth(width)
        return chartview, series

    
    def updatePieChart(self, series, happy, sad, disgust, anger, neutral, suprised, fear):
        series.clear()
        series.append("Happy", happy)
        series.append("Sad", sad)
        series.append("Disgust", disgust)
        series.append("Anger", anger)
        series.append("Neutral", neutral)
        series.append("Suprised", suprised)
        series.append("Fear", fear)
    
    def updateBarChart(self, series, happy, sad, disgust, anger, neutral, suprised, fear):
        series.clear()
        set0 = QBarSet("Happy")
        set1 = QBarSet('Sad')
        set2 = QBarSet('Disgust')
        set3 = QBarSet('Angry')
        set4 = QBarSet('Neutral')
        set5 = QBarSet('Suprised')
        set6 = QBarSet('Fear')
        
        set0 << (happy) << 0 << 0 << 0 << 0 << 0 << 0
        set1 << 0 << (sad) << 0 << 0 << 0 << 0 << 0
        set2 << 0 << 0 << (disgust) << 0 << 0 << 0 << 0
        set3 << 0 << 0 << 0 << (anger) << 0 << 0 << 0
        set4 << 0 << 0 << 0 << 0 << (neutral) << 0 << 0
        set5 << 0 << 0 << 0 << 0 << 0 << (suprised) << 0
        set6 << 0 << 0 << 0 << 0 << 0 << 0 << (fear)
        
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)
        series.append(set4)
        series.append(set5)
        series.append(set6)
    
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(866, 650)
        MainWindow.setStyleSheet(u"border-image: url(:/Horus Main Page/startscreen.jpg);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"border-image: url(:/Horus Main Page/startscreen.jpg);")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_2 = QGridLayout(self.page)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horus_image_label_2 = QLabel(self.page)
        self.horus_image_label_2.setObjectName(u"horus_image_label_2")
        self.horus_image_label_2.setMinimumSize(QSize(300, 150))
        self.horus_image_label_2.setStyleSheet(u"border-image: url(:/Horus Main Page/Horus.png);")

        self.verticalLayout.addWidget(self.horus_image_label_2, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.horus_name_label = QLabel(self.page)
        self.horus_name_label.setObjectName(u"horus_name_label")
        self.horus_name_label.setMinimumSize(QSize(300, 60))
        self.horus_name_label.setStyleSheet(u"border-image: url(:/Horus Main Page/HorusName.png);")

        self.verticalLayout.addWidget(self.horus_name_label, 0, Qt.AlignHCenter|Qt.AlignTop)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.start_button = QPushButton(self.page)
        self.start_button.setObjectName(u"start_button")
        self.start_button.setMinimumSize(QSize(200, 50))
        self.start_button.setStyleSheet(u"border-image: url(:/Horus Main Page/start.png);")
        self.start_button.setCheckable(False)
        self.start_button.setChecked(False)
        self.start_button.setAutoDefault(False)
        self.start_button.clicked.connect(partial(self.on_click_to_menu, "start_button"))

        self.verticalLayout_2.addWidget(self.start_button, 0, Qt.AlignHCenter|Qt.AlignBottom)


        self.gridLayout_2.addLayout(self.verticalLayout_2, 1, 0, 1, 1)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout_3 = QGridLayout(self.page_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.crowd_control_button = QPushButton(self.page_2)
        self.crowd_control_button.setObjectName(u"crowd_control_button")
        self.crowd_control_button.setMinimumSize(QSize(380, 30))
        self.crowd_control_button.setStyleSheet(u"border-image: url(:/Horus Main Page/crowdcontrol.png);")
        self.crowd_control_button.clicked.connect(self.on_click_crowd_control)

        self.verticalLayout_7.addWidget(self.crowd_control_button, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_3.addLayout(self.verticalLayout_7, 3, 0, 1, 1)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.single_user_button = QPushButton(self.page_2)
        self.single_user_button.setObjectName(u"single_user_button")
        self.single_user_button.setMinimumSize(QSize(330, 40))
        self.single_user_button.setStyleSheet(u"border-image: url(:/Horus Main Page/singleuser.png);")
        self.single_user_button.clicked.connect(self.on_click_single_user)

        self.verticalLayout_6.addWidget(self.single_user_button, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_3.addLayout(self.verticalLayout_6, 2, 0, 1, 1)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.deception_detection_button = QPushButton(self.page_2)
        self.deception_detection_button.setObjectName(u"deception_detection_button")
        self.deception_detection_button.setMinimumSize(QSize(400, 40))
        self.deception_detection_button.setStyleSheet(u"border-image: url(:/Horus Main Page/deceptiondetection.png);")
        self.deception_detection_button.clicked.connect(self.on_click_deception_detection)

        self.verticalLayout_8.addWidget(self.deception_detection_button, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_3.addLayout(self.verticalLayout_8, 4, 0, 1, 1)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.screen_capture_button = QPushButton(self.page_2)
        self.screen_capture_button.setObjectName(u"screen_capture_button")
        self.screen_capture_button.setMinimumSize(QSize(400, 30))
        self.screen_capture_button.setStyleSheet(u"border-image: url(:/Horus Main Page/screencapt\u0131ure.png);")
        self.screen_capture_button.clicked.connect(self.on_click_screen_capture)

        self.verticalLayout_11.addWidget(self.screen_capture_button, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_3.addLayout(self.verticalLayout_11, 6, 0, 1, 1)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.list_analysis_button = QPushButton(self.page_2)
        self.list_analysis_button.setObjectName(u"list_analysis_button")
        self.list_analysis_button.setMinimumSize(QSize(390, 40))
        self.list_analysis_button.setStyleSheet(u"border-image: url(:/Horus Main Page/lastanalyses.png);")
        self.list_analysis_button.clicked.connect(self.on_click_list_analyses)

        self.verticalLayout_10.addWidget(self.list_analysis_button, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_3.addLayout(self.verticalLayout_10, 5, 0, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horus_image_label = QLabel(self.page_2)
        self.horus_image_label.setObjectName(u"horus_image_label")
        self.horus_image_label.setMinimumSize(QSize(200, 100))
        self.horus_image_label.setStyleSheet(u"border-image: url(:/Horus Main Page/Horus.png);")

        self.verticalLayout_3.addWidget(self.horus_image_label, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_3.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.choose_mode_label = QLabel(self.page_2)
        self.choose_mode_label.setObjectName(u"choose_mode_label")
        self.choose_mode_label.setMinimumSize(QSize(400, 50))
        self.choose_mode_label.setStyleSheet(u"border-image: url(:/Horus Main Page/choosemode.png);")

        self.verticalLayout_4.addWidget(self.choose_mode_label, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_3.addLayout(self.verticalLayout_4, 1, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.gridLayout_4 = QGridLayout(self.page_3)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.p3_bottom_frame = QFrame(self.page_3)
        self.p3_bottom_frame.setObjectName(u"p3_bottom_frame")
        self.p3_bottom_frame.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.p3_bottom_frame.sizePolicy().hasHeightForWidth())
        self.p3_bottom_frame.setSizePolicy(sizePolicy)
        font = QFont()
        font.setKerning(True)
        self.p3_bottom_frame.setFont(font)
        self.p3_bottom_frame.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.p3_bottom_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p3_bottom_frame.setFrameShape(QFrame.NoFrame)
        self.p3_bottom_frame.setLineWidth(0)
        self.horizontalLayout = QHBoxLayout(self.p3_bottom_frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.scanLabelp3 = QLabel(self.p3_bottom_frame)
        self.scanLabelp3.setObjectName(u"scanLabelp3")
        fontscan = QFont()
        fontscan.setPointSize(16)
        self.scanLabelp3.setFont(fontscan)

        self.horizontalLayout.addWidget(self.scanLabelp3, 0, Qt.AlignHCenter|Qt.AlignBottom)

        self.replay_button_3 = QPushButton(self.p3_bottom_frame)
        self.replay_button_3.setObjectName(u"replay_button_3")
        self.replay_button_3.setMinimumSize(QSize(50, 50))
        self.replay_button_3.setStyleSheet(u"border-image: url(:/Horus Main Page/repeat.png);")
        self.replay_button_3.clicked.connect(self.replayVidBtn)

        self.horizontalLayout.addWidget(self.replay_button_3, 0, Qt.AlignHCenter|Qt.AlignBottom)

        self.pause_button_3 = QPushButton(self.p3_bottom_frame)
        self.pause_button_3.setObjectName(u"pause_button_3")
        self.pause_button_3.setMinimumSize(QSize(50, 50))
        self.pause_button_3.setStyleSheet(u"border-image: url(:/Horus Main Page/stop.png);")
        self.pause_button_3.clicked.connect(partial(self.pauseVidBtn, "pause_button_3"))

        self.horizontalLayout.addWidget(self.pause_button_3, 0, Qt.AlignHCenter|Qt.AlignBottom)
        self.play_button_3 = QPushButton(self.p3_bottom_frame)
        self.play_button_3.setObjectName(u"play_button_3")
        self.play_button_3.setMinimumSize(QSize(50, 50))
        self.play_button_3.setStyleSheet(u"border-image: url(:/Horus Main Page/play.png);")
        self.play_button_3.clicked.connect(partial(self.playVidBtn, "play_button_3"))

        self.horizontalLayout.addWidget(self.play_button_3, 0, Qt.AlignHCenter|Qt.AlignBottom)

        self.pushButton_3 = QPushButton(self.p3_bottom_frame)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(100, 50))
        self.pushButton_3.setStyleSheet(u"border-image: url(:/Horus Main Page/gotoresults.png);")
        self.pushButton_3.clicked.connect(partial(self.on_click_goto_result, "pushButton_3"))

        self.horizontalLayout.addWidget(self.pushButton_3, 0, Qt.AlignHCenter|Qt.AlignBottom)


        self.gridLayout_4.addWidget(self.p3_bottom_frame, 2, 0, 1, 1)

        self.p3_top_frame = QFrame(self.page_3)
        self.p3_top_frame.setObjectName(u"p3_top_frame")
        sizePolicy.setHeightForWidth(self.p3_top_frame.sizePolicy().hasHeightForWidth())
        self.p3_top_frame.setSizePolicy(sizePolicy)
        self.p3_top_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p3_top_frame.setLineWidth(0)
        self.horizontalLayout_2 = QHBoxLayout(self.p3_top_frame)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.back_button_6 = QPushButton(self.p3_top_frame)
        self.back_button_6.setObjectName(u"back_button_6")
        self.back_button_6.setMinimumSize(QSize(125, 50))
        self.back_button_6.setLayoutDirection(Qt.LeftToRight)
        self.back_button_6.setStyleSheet(u"border-image: url(:/Horus Main Page/backButton.png);")
        self.back_button_6.clicked.connect(partial(self.on_click_to_menu, "back_button_6"))
        
        self.horizontalLayout_2.addWidget(self.back_button_6, 0, Qt.AlignLeft|Qt.AlignTop)

        self.upload_button_3 = QPushButton(self.p3_top_frame)
        self.upload_button_3.setObjectName(u"upload_button_3")
        self.upload_button_3.setMinimumSize(QSize(80, 50))
        self.upload_button_3.setStyleSheet(u"border-image: url(:/Horus Main Page/upload.png);")
        self.upload_button_3.clicked.connect(self.on_click_upload)

        self.horizontalLayout_2.addWidget(self.upload_button_3, 0, Qt.AlignRight|Qt.AlignTop)


        self.gridLayout_4.addWidget(self.p3_top_frame, 0, 0, 1, 1)
        
        self.chartViewBarSingle, self.seriesBarSingle = self.drawBarChart()

        self.p3_middle_frame = QFrame(self.page_3)
        self.p3_middle_frame.setObjectName(u"p3_middle_frame")
        self.p3_middle_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p3_middle_frame.setLineWidth(0)
        self.screenlayout = QHBoxLayout(self.p3_middle_frame)
        self.screenlayout.setSpacing(0)
        self.screenlayout.setObjectName(u"screenlayout")
        self.screenlayout.setContentsMargins(0, 0, 0, 0)
        
        self.p3_chart_frame1 = QFrame(self.p3_middle_frame)
        self.p3_chart_frame1.setObjectName(u"p3_chart_frame1")
        self.p3_chart_frame1.setFrameShape(QFrame.StyledPanel)
        self.p3_chart_frame1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.p3_chart_frame1)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")

        self.screenlayout.addWidget(self.p3_chart_frame1)
        
        self.p3_screen_label = QLabel(self.p3_middle_frame)
        self.p3_screen_label.setObjectName(u"p3_screen_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.p3_screen_label.sizePolicy().hasHeightForWidth())
        self.p3_screen_label.setSizePolicy(sizePolicy1)

        self.verticalLayout_12.addWidget(self.chartViewBarSingle, 0, Qt.AlignHCenter|Qt.AlignVCenter)
        self.screenlayout.addWidget(self.p3_screen_label, 0, Qt.AlignRight|Qt.AlignVCenter)#Qt.AlignHCenter|Qt.AlignVCenter
        
        self.gridLayout_4.addWidget(self.p3_middle_frame, 1, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_3)
        self.p3_bottom_frame.raise_()
        self.p3_middle_frame.raise_()
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.gridLayout_14 = QGridLayout(self.page_4)
        self.gridLayout_14.setSpacing(0)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(0, 0, 0, 0)
        self.p4_bottom_frame = QFrame(self.page_4)
        self.p4_bottom_frame.setObjectName(u"p4_bottom_frame")
        sizePolicy.setHeightForWidth(self.p4_bottom_frame.sizePolicy().hasHeightForWidth())
        self.p4_bottom_frame.setSizePolicy(sizePolicy)
        self.p4_bottom_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p4_bottom_frame.setLineWidth(0)
        self.horizontalLayout_6 = QHBoxLayout(self.p4_bottom_frame)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        
        self.scanLabelp4 = QLabel(self.p4_bottom_frame)
        self.scanLabelp4.setObjectName(u"scanLabelp4")
        self.scanLabelp4.setFont(fontscan)

        self.horizontalLayout_6.addWidget(self.scanLabelp4, 0, Qt.AlignHCenter|Qt.AlignBottom)

        # self.replay_button_2 = QPushButton(self.p4_bottom_frame)
        # self.replay_button_2.setObjectName(u"replay_button_2")
        # self.replay_button_2.setMinimumSize(QSize(50, 50))
        # self.replay_button_2.setStyleSheet(u"border-image: url(:/Horus Main Page/repeat.png);")

        # self.horizontalLayout_6.addWidget(self.replay_button_2, 0, Qt.AlignHCenter|Qt.AlignBottom)

        self.pause_button_2 = QPushButton(self.p4_bottom_frame)
        self.pause_button_2.setObjectName(u"pause_button_2")
        self.pause_button_2.setMinimumSize(QSize(50, 50))
        self.pause_button_2.setStyleSheet(u"border-image: url(:/Horus Main Page/stop.png);")
        self.pause_button_2.clicked.connect(partial(self.pauseVidBtn, "pause_button_2"))

        self.horizontalLayout_6.addWidget(self.pause_button_2, 0, Qt.AlignHCenter|Qt.AlignBottom)

        self.play_button_2 = QPushButton(self.p4_bottom_frame)
        self.play_button_2.setObjectName(u"play_button_2")
        self.play_button_2.setMinimumSize(QSize(50, 50))
        self.play_button_2.setStyleSheet(u"border-image: url(:/Horus Main Page/play.png);")
        self.play_button_2.clicked.connect(partial(self.playVidBtn, "play_button_2"))
        
        self.horizontalLayout_6.addWidget(self.play_button_2, 0, Qt.AlignHCenter|Qt.AlignBottom)
        
        self.changeCamButton = QPushButton(self.p4_bottom_frame)
        self.changeCamButton.setObjectName(u"changeCamButton")
        fontCam = QFont()
        fontCam.setPointSize(12)
        self.changeCamButton.setFont(fontCam)
        self.horizontalLayout_6.addWidget(self.changeCamButton)

        self.changeCamButton.clicked.connect(self.on_click_change_cam)

        self.pushButton_2 = QPushButton(self.p4_bottom_frame)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(100, 50))
        self.pushButton_2.setStyleSheet(u"border-image: url(:/Horus Main Page/gotoresults.png);")
        self.pushButton_2.clicked.connect(partial(self.on_click_goto_result, "pushButton_2"))

        self.horizontalLayout_6.addWidget(self.pushButton_2, 0, Qt.AlignHCenter|Qt.AlignBottom)


        self.gridLayout_14.addWidget(self.p4_bottom_frame, 2, 0, 1, 1)

        self.p4_top_frame = QFrame(self.page_4)
        self.p4_top_frame.setObjectName(u"p4_top_frame")
        sizePolicy.setHeightForWidth(self.p4_top_frame.sizePolicy().hasHeightForWidth())
        self.p4_top_frame.setSizePolicy(sizePolicy)
        self.p4_top_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p4_top_frame.setLineWidth(0)
        self.horizontalLayout_3 = QHBoxLayout(self.p4_top_frame)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.back_button_5 = QPushButton(self.p4_top_frame)
        self.back_button_5.setObjectName(u"back_button_5")
        self.back_button_5.setMinimumSize(QSize(125, 50))
        self.back_button_5.setStyleSheet(u"border-image: url(:/Horus Main Page/backButton.png);")
        self.back_button_5.clicked.connect(partial(self.on_click_to_menu, "back_button_5"))


        self.horizontalLayout_3.addWidget(self.back_button_5, 0, Qt.AlignLeft|Qt.AlignTop)

        # self.upload_button_2 = QPushButton(self.p4_top_frame)
        # self.upload_button_2.setObjectName(u"upload_button_2")
        # self.upload_button_2.setMinimumSize(QSize(80, 50))
        # self.upload_button_2.setStyleSheet(u"border-image: url(:/Horus Main Page/upload.png);")

        # self.horizontalLayout_3.addWidget(self.upload_button_2, 0, Qt.AlignRight|Qt.AlignTop)


        self.gridLayout_14.addWidget(self.p4_top_frame, 0, 0, 1, 1)

        self.chartViewBarMulti, self.seriesBarMulti = self.drawBarChart()

        self.p4_middle_frame = QFrame(self.page_4)
        self.p4_middle_frame.setObjectName(u"p4_middle_frame")
        self.p4_middle_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p4_middle_frame.setLineWidth(0)
        self.screenlayout2 = QHBoxLayout(self.p4_middle_frame)
        self.screenlayout2.setSpacing(0)
        self.screenlayout2.setObjectName(u"screenlayout2")
        self.screenlayout2.setContentsMargins(0, 0, 0, 0)
        
        self.p4_chart_frame1 = QFrame(self.p4_middle_frame)
        self.p4_chart_frame1.setObjectName(u"p4_chart_frame1")
        self.p4_chart_frame1.setFrameShape(QFrame.StyledPanel)
        self.p4_chart_frame1.setFrameShadow(QFrame.Raised) 
        self.verticalLayoutp4ch = QVBoxLayout(self.p4_chart_frame1)
        self.verticalLayoutp4ch.setObjectName(u"verticalLayoutp4ch")
        
        self.screenlayout2.addWidget(self.p4_chart_frame1)
        
        self.p4_screen_label = QLabel(self.p4_middle_frame)
        self.p4_screen_label.setObjectName(u"p4_screen_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.p4_screen_label.sizePolicy().hasHeightForWidth())
        self.p4_screen_label.setSizePolicy(sizePolicy2)

        self.verticalLayoutp4ch.addWidget(self.chartViewBarMulti, 0, Qt.AlignLeft|Qt.AlignVCenter)

        self.screenlayout2.addWidget(self.p4_screen_label, 0, Qt.AlignRight|Qt.AlignVCenter)

        self.gridLayout_14.addWidget(self.p4_middle_frame, 1, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_4)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.gridLayout_15 = QGridLayout(self.page_5)
        self.gridLayout_15.setSpacing(0)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.p5_bottom_frame = QFrame(self.page_5)
        self.p5_bottom_frame.setObjectName(u"p5_bottom_frame")
        sizePolicy.setHeightForWidth(self.p5_bottom_frame.sizePolicy().hasHeightForWidth())
        self.p5_bottom_frame.setSizePolicy(sizePolicy)
        self.p5_bottom_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p5_bottom_frame.setLineWidth(0)
        self.verticalLayout_61 = QVBoxLayout(self.p5_bottom_frame)
        self.verticalLayout_61.setSpacing(0)
        self.verticalLayout_61.setObjectName(u"verticalLayout_61")
        self.verticalLayout_61.setContentsMargins(0, 0, 0, 0)       
        self.detectionLabel = QLabel(self.p5_bottom_frame)
        self.detectionLabel.setObjectName(u"detectionLabel")
        font4 = QFont()
        font4.setPointSize(18)
        self.detectionLabel.setFont(font4)

        self.verticalLayout_61.addWidget(self.detectionLabel, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_15.addWidget(self.p5_bottom_frame, 2, 0, 1, 1)

        self.p5_top_frame = QFrame(self.page_5)
        self.p5_top_frame.setObjectName(u"p5_top_frame")
        sizePolicy.setHeightForWidth(self.p5_top_frame.sizePolicy().hasHeightForWidth())
        self.p5_top_frame.setSizePolicy(sizePolicy)
        self.p5_top_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p5_top_frame.setLineWidth(0)
        self.verticalLayout_59 = QHBoxLayout(self.p5_top_frame)
        self.verticalLayout_59.setSpacing(0)
        self.verticalLayout_59.setObjectName(u"verticalLayout_59")
        self.verticalLayout_59.setContentsMargins(0, 0, 0, 0)
        self.back_button_4 = QPushButton(self.p5_top_frame)
        self.back_button_4.setObjectName(u"back_button_4")
        self.back_button_4.setMinimumSize(QSize(125, 50))
        self.back_button_4.setMaximumSize(QSize(125, 50))
        self.back_button_4.setStyleSheet(u"border-image: url(:/Horus Main Page/backButton.png);")
        self.back_button_4.clicked.connect(partial(self.on_click_to_menu, "back_button_4"))

        self.verticalLayout_59.addWidget(self.back_button_4, 0, Qt.AlignLeft|Qt.AlignTop)

        self.detectionStartButton = QPushButton(self.p5_top_frame)
        self.detectionStartButton.setObjectName(u"detectionStartButton")
        font5 = QFont()
        font5.setPointSize(16)
        font5.setBold(False)
        font5.setItalic(True)
        font5.setUnderline(False)
        font5.setWeight(50)
        font5.setStrikeOut(False)
        font5.setKerning(True)
        self.detectionStartButton.setFont(font5)
        self.detectionStartButton.clicked.connect(self.start_deception_Detection)

        self.verticalLayout_59.addWidget(self.detectionStartButton, 0, Qt.AlignRight)

        self.gridLayout_15.addWidget(self.p5_top_frame, 0, 0, 1, 1)

        self.p5_middle_frame = QFrame(self.page_5)
        self.p5_middle_frame.setObjectName(u"p5_middle_frame")
        self.p5_middle_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p5_middle_frame.setLineWidth(0)
        self.screenlayout3 = QHBoxLayout(self.p5_middle_frame)
        self.screenlayout3.setSpacing(0)
        self.screenlayout3.setObjectName(u"screenlayout3")
        self.screenlayout3.setContentsMargins(0, 0, 0, 0)
        fontCounter = QFont()
        fontCounter.setPointSize(16)
        self.leftCounterLabel = QLabel(self.p5_middle_frame)
        self.leftCounterLabel.setObjectName(u"leftCounterLabel")
        self.leftCounterLabel.setFont(fontCounter)
        self.screenlayout3.addWidget(self.leftCounterLabel, 0, Qt.AlignHCenter|Qt.AlignVCenter)
        
        self.p5_screen_label = QLabel(self.p5_middle_frame)
        self.p5_screen_label.setObjectName(u"p5_screen_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.p5_screen_label.sizePolicy().hasHeightForWidth())
        self.p5_screen_label.setSizePolicy(sizePolicy3)

        self.screenlayout3.addWidget(self.p5_screen_label, 0, Qt.AlignHCenter|Qt.AlignVCenter)
        
        self.rightCounterLabel = QLabel(self.p5_middle_frame)
        self.rightCounterLabel.setObjectName(u"rightCounterLabel")
        self.rightCounterLabel.setFont(fontCounter)

        self.screenlayout3.addWidget(self.rightCounterLabel, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.gridLayout_15.addWidget(self.p5_middle_frame, 1, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_5)
        self.page_21 = QWidget()
        self.page_21.setObjectName(u"page_21")
        self.gridLayout_16 = QGridLayout(self.page_21)
        self.gridLayout_16.setSpacing(0)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(0, 0, 0, 0)
        self.p21_bottom_frame = QFrame(self.page_21)
        self.p21_bottom_frame.setObjectName(u"p21_bottom_frame")
        sizePolicy.setHeightForWidth(self.p21_bottom_frame.sizePolicy().hasHeightForWidth())
        self.p21_bottom_frame.setSizePolicy(sizePolicy)
        self.p21_bottom_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p21_bottom_frame.setLineWidth(0)
        self.horizontalLayout_8 = QHBoxLayout(self.p21_bottom_frame)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.screenCapScanLabel = QLabel(self.p21_bottom_frame)
        self.screenCapScanLabel.setObjectName(u"screenCapScanLabel")
        self.screenCapScanLabel.setFont(fontscan)

        self.horizontalLayout_8.addWidget(self.screenCapScanLabel, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        # self.replay_button = QPushButton(self.p21_bottom_frame)
        # self.replay_button.setObjectName(u"replay_button")
        # self.replay_button.setMinimumSize(QSize(50, 50))
        # self.replay_button.setStyleSheet(u"border-image: url(:/Horus Main Page/repeat.png);")

        # self.horizontalLayout_8.addWidget(self.replay_button, 0, Qt.AlignHCenter|Qt.AlignBottom)

        self.pause_button = QPushButton(self.p21_bottom_frame)
        self.pause_button.setObjectName(u"pause_button")
        self.pause_button.setMinimumSize(QSize(50, 50))
        self.pause_button.setStyleSheet(u"border-image: url(:/Horus Main Page/stop.png);")
        self.pause_button.clicked.connect(partial(self.pauseVidBtn, "pause_button"))

        self.horizontalLayout_8.addWidget(self.pause_button, 0, Qt.AlignHCenter|Qt.AlignBottom)

        self.play_button = QPushButton(self.p21_bottom_frame)
        self.play_button.setObjectName(u"play_button")
        self.play_button.setMinimumSize(QSize(50, 50))
        self.play_button.setStyleSheet(u"border-image: url(:/Horus Main Page/play.png);")
        self.play_button.clicked.connect(partial(self.playVidBtn, "play_button"))

        self.horizontalLayout_8.addWidget(self.play_button, 0, Qt.AlignHCenter|Qt.AlignBottom)

        self.pushButton = QPushButton(self.p21_bottom_frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(100, 50))
        self.pushButton.setStyleSheet(u"border-image: url(:/Horus Main Page/gotoresults.png);")
        self.pushButton.clicked.connect(partial(self.on_click_goto_result, "pushButton"))

        self.horizontalLayout_8.addWidget(self.pushButton, 0, Qt.AlignHCenter|Qt.AlignBottom)


        self.gridLayout_16.addWidget(self.p21_bottom_frame, 2, 0, 1, 1)

        self.p21_top_frame = QFrame(self.page_21)
        self.p21_top_frame.setObjectName(u"p21_top_frame")
        sizePolicy.setHeightForWidth(self.p21_top_frame.sizePolicy().hasHeightForWidth())
        self.p21_top_frame.setSizePolicy(sizePolicy)
        self.p21_top_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p21_top_frame.setLineWidth(0)
        self.horizontalLayout_7 = QHBoxLayout(self.p21_top_frame)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.back_button_3 = QPushButton(self.p21_top_frame)
        self.back_button_3.setObjectName(u"back_button_3")
        self.back_button_3.setMinimumSize(QSize(125, 50))
        self.back_button_3.setStyleSheet(u"border-image: url(:/Horus Main Page/backButton.png);")
        self.back_button_3.clicked.connect(partial(self.on_click_to_menu, "back_button_3"))

        self.horizontalLayout_7.addWidget(self.back_button_3, 0, Qt.AlignLeft|Qt.AlignTop)

        # self.upload_button = QPushButton(self.p21_top_frame)
        # self.upload_button.setObjectName(u"upload_button")
        # self.upload_button.setMinimumSize(QSize(80, 50))
        # self.upload_button.setStyleSheet(u"border-image: url(:/Horus Main Page/upload.png);")

        # self.horizontalLayout_7.addWidget(self.upload_button, 0, Qt.AlignRight|Qt.AlignTop)

        self.gridLayout_16.addWidget(self.p21_top_frame, 0, 0, 1, 1)

        self.chartViewBarCapture, self.seriesBarCapture = self.drawBarChart()

        self.p21_middle_frame = QFrame(self.page_21)
        self.p21_middle_frame.setObjectName(u"p21_middle_frame")
        self.p21_middle_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p21_middle_frame.setLineWidth(0)
        self.screenlayout4 = QHBoxLayout(self.p21_middle_frame)
        self.screenlayout4.setSpacing(0)
        self.screenlayout4.setObjectName(u"screenlayout4")
        self.screenlayout4.setContentsMargins(0, 0, 0, 0)
        
        self.p21_chart_frame1 = QFrame(self.p21_middle_frame)
        self.p21_chart_frame1.setObjectName(u"p21_chart_frame1")
        self.p21_chart_frame1.setFrameShape(QFrame.StyledPanel)
        self.p21_chart_frame1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_21 = QVBoxLayout(self.p21_chart_frame1)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")

        self.screenlayout4.addWidget(self.p21_chart_frame1)
    
        self.p21_screen_label = QLabel(self.p21_middle_frame)
        self.p21_screen_label.setObjectName(u"p21_screen_label")
        sizePolicy2.setHeightForWidth(self.p21_screen_label.sizePolicy().hasHeightForWidth())
        self.p21_screen_label.setSizePolicy(sizePolicy2)
        
        self.verticalLayout_21.addWidget(self.chartViewBarCapture, 0, Qt.AlignHCenter|Qt.AlignVCenter)
        self.screenlayout4.addWidget(self.p21_screen_label, 0, Qt.AlignRight|Qt.AlignVCenter)

        self.gridLayout_16.addWidget(self.p21_middle_frame, 1, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_21)
        self.page_22 = QWidget()
        self.page_22.setObjectName(u"page_22")
        self.gridLayout_17 = QGridLayout(self.page_22)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.back_button_2 = QPushButton(self.page_22)
        self.back_button_2.setObjectName(u"back_button_2")
        self.back_button_2.setMinimumSize(QSize(125, 50))
        self.back_button_2.setStyleSheet(u"border-image: url(:/Horus Main Page/backButton.png);")
        self.back_button_2.clicked.connect(partial(self.on_click_to_menu, "back_button_2"))

        self.verticalLayout_13.addWidget(self.back_button_2, 0, Qt.AlignLeft|Qt.AlignTop)

        self.chooseo_output_type = QLabel(self.page_22)
        self.chooseo_output_type.setObjectName(u"chooseo_output_type")
        self.chooseo_output_type.setMinimumSize(QSize(400, 50))
        self.chooseo_output_type.setStyleSheet(u"border-image: url(:/Horus Main Page/chooseoutputtype.png);")

        self.verticalLayout_13.addWidget(self.chooseo_output_type, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_17.addLayout(self.verticalLayout_13, 0, 0, 1, 1)

        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.viewCodeButton = QPushButton(self.page_22)
        self.viewCodeButton.setObjectName(u"viewCodeButton")
        self.viewCodeButton.setMinimumSize(QSize(300, 50))
        self.viewCodeButton.setStyleSheet(u"border-image: url(:/Horus Main Page/view.png);")
        self.viewCodeButton.clicked.connect(self.on_click_view_data)

        self.verticalLayout_15.addWidget(self.viewCodeButton, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.gridLayout_17.addLayout(self.verticalLayout_15, 3, 0, 1, 1)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.linechart_button = QPushButton(self.page_22)
        self.linechart_button.setObjectName(u"linechart_button")
        self.linechart_button.setMinimumSize(QSize(150, 40))
        self.linechart_button.setStyleSheet(u"border-image: url(:/Horus Main Page/1.png);")
        self.linechart_button.clicked.connect(self.on_click_line_button)

        self.horizontalLayout_9.addWidget(self.linechart_button, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.pie_button = QPushButton(self.page_22)
        self.pie_button.setObjectName(u"pie_button")
        self.pie_button.setMinimumSize(QSize(150, 40))
        self.pie_button.setStyleSheet(u"border-image: url(:/Horus Main Page/2.png);")
        self.pie_button.clicked.connect(self.on_click_pie_button)

        self.horizontalLayout_9.addWidget(self.pie_button, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.histogram_button = QPushButton(self.page_22)
        self.histogram_button.setObjectName(u"histogram_button")
        self.histogram_button.setMinimumSize(QSize(150, 40))
        self.histogram_button.setStyleSheet(u"border-image: url(:/Horus Main Page/3.png);")
        self.histogram_button.clicked.connect(self.on_click_histogram_button)

        self.horizontalLayout_9.addWidget(self.histogram_button, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        # self.table_button = QPushButton(self.page_22)
        # self.table_button.setObjectName(u"table_button")
        # self.table_button.setMinimumSize(QSize(150, 40))
        # self.table_button.setStyleSheet(u"border-image: url(:/Horus Main Page/4.png);")
        # self.table_button.clicked.connect(self.on_click_table_button)

        # self.horizontalLayout_9.addWidget(self.table_button, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.donut_button = QPushButton(self.page_22)
        self.donut_button.setObjectName(u"donut_button")
        self.donut_button.setMinimumSize(QSize(150, 40))
        self.donut_button.setStyleSheet(u"border-image: url(:/Horus Main Page/5.png);")
        self.donut_button.clicked.connect(self.on_click_donut_button)

        self.horizontalLayout_9.addWidget(self.donut_button, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_17.addLayout(self.horizontalLayout_9, 1, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_22)
        self.page_23 = QWidget()
        self.page_23.setObjectName(u"page_23")
        self.gridLayout_18 = QGridLayout(self.page_23)
        self.gridLayout_18.setSpacing(0)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_55 = QVBoxLayout()
        self.verticalLayout_55.setObjectName(u"verticalLayout_55")
        self.edit_button = QPushButton(self.page_23)
        self.edit_button.setObjectName(u"edit_button")
        self.edit_button.setMinimumSize(QSize(70, 20))
        self.edit_button.setStyleSheet(u"border-image: url(:/Horus Main Page/edit.png);")

        self.verticalLayout_55.addWidget(self.edit_button, 0, Qt.AlignHCenter)

        self.download_button = QPushButton(self.page_23)
        self.download_button.setObjectName(u"download_button")
        self.download_button.setMinimumSize(QSize(150, 25))
        self.download_button.setStyleSheet(u"border-image: url(:/Horus Main Page/download.png);")

        self.verticalLayout_55.addWidget(self.download_button, 0, Qt.AlignHCenter)


        self.gridLayout_18.addLayout(self.verticalLayout_55, 2, 1, 1, 1)

        self.p23_bottom_frame = QFrame(self.page_23)
        self.p23_bottom_frame.setObjectName(u"p23_bottom_frame")
        self.p23_bottom_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.verticalLayout_53 = QVBoxLayout(self.p23_bottom_frame)
        self.verticalLayout_53.setObjectName(u"verticalLayout_53")

        self.gridLayout_18.addWidget(self.p23_bottom_frame, 3, 0, 1, 2)

        self.p23_middle_frame = QFrame(self.page_23)
        self.p23_middle_frame.setObjectName(u"p23_middle_frame")
        self.p23_middle_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.graphiclayout = QHBoxLayout(self.p23_middle_frame)
        self.graphiclayout.setSpacing(0)
        self.graphiclayout.setObjectName(u"graphiclayout")

        self.gridLayout_18.addWidget(self.p23_middle_frame, 2, 0, 1, 1)

        self.p23_top_frame = QFrame(self.page_23)
        self.p23_top_frame.setObjectName(u"p23_top_frame")
        self.p23_top_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.verticalLayout_14 = QVBoxLayout(self.p23_top_frame)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.back_button = QPushButton(self.p23_top_frame)
        self.back_button.setObjectName(u"back_button")
        self.back_button.setMinimumSize(QSize(125, 50))
        self.back_button.setStyleSheet(u"border-image: url(:/Horus Main Page/backButton.png);")

        self.verticalLayout_14.addWidget(self.back_button, 0, Qt.AlignLeft|Qt.AlignTop)

        self.analysis_text = QTextBrowser(self.p23_top_frame)
        self.analysis_text.setObjectName(u"analysis_text")
        self.analysis_text.setMinimumSize(QSize(0, 0))
        self.analysis_text.setMaximumSize(QSize(300, 50))
        self.analysis_text.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")

        self.verticalLayout_14.addWidget(self.analysis_text, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_18.addWidget(self.p23_top_frame, 0, 0, 1, 2)

        self.stackedWidget.addWidget(self.page_23)
        self.page_24 = QWidget()
        self.page_24.setObjectName(u"page_24")
        self.gridLayout_19 = QGridLayout(self.page_24)
        self.gridLayout_19.setSpacing(0)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.listView = QListView(self.page_24)
        self.listView.setObjectName(u"listView")
        self.listView.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")

        self.verticalLayout_5.addWidget(self.listView)

        self.gridLayout_19.addLayout(self.verticalLayout_5, 1, 0, 1, 1)

        self.p24_top_frame = QFrame(self.page_24)
        self.p24_top_frame.setObjectName(u"p24_top_frame")
        self.p24_top_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.verticalLayout_60 = QVBoxLayout(self.p24_top_frame)
        self.verticalLayout_60.setSpacing(0)
        self.verticalLayout_60.setObjectName(u"verticalLayout_60")
        self.verticalLayout_60.setContentsMargins(0, 0, 0, 0)
        self.back_button_8 = QPushButton(self.p24_top_frame)
        self.back_button_8.setObjectName(u"back_button_8")
        self.back_button_8.setMinimumSize(QSize(125, 50))
        self.back_button_8.setStyleSheet(u"border-image: url(:/Horus Main Page/backButton.png);")
        self.back_button_8.clicked.connect(partial(self.on_click_to_menu, "back_button_8"))

        self.verticalLayout_60.addWidget(self.back_button_8, 0, Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.capture_label = QLabel(self.p24_top_frame)
        self.capture_label.setObjectName(u"capture_label")
        self.capture_label.setMinimumSize(QSize(500, 50))
        self.capture_label.setStyleSheet(u"border-image: url(:/Horus Main Page/capture.png);")

        self.horizontalLayout_4.addWidget(self.capture_label, 0, Qt.AlignLeft)

        self.runbutton = QPushButton(self.p24_top_frame)
        self.runbutton.setObjectName(u"runbutton")
        self.runbutton.setMinimumSize(QSize(150, 50))
        self.runbutton.setMaximumSize(QSize(125, 50))
        font2 = QFont()
        font2.setFamily(u"PMingLiU-ExtB")
        font2.setPointSize(13)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setUnderline(False)
        font2.setWeight(50)
        font2.setStrikeOut(False)
        self.runbutton.setFont(font2)
        self.runbutton.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/Horus Main Page/play.png", QSize(), QIcon.Normal, QIcon.Off)
        self.runbutton.setIcon(icon)
        self.runbutton.setIconSize(QSize(35, 35))
        self.runbutton.clicked.connect(self.on_click_crowd_control_run)

        
        self.horizontalLayout_4.addWidget(self.runbutton, 0, Qt.AlignRight|Qt.AlignVCenter)


        self.verticalLayout_60.addLayout(self.horizontalLayout_4)


        self.gridLayout_19.addWidget(self.p24_top_frame, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_24)
        self.page_25 = QWidget()
        self.page_25.setObjectName(u"page_25")
        self.gridLayout_20 = QGridLayout(self.page_25)
        self.gridLayout_20.setSpacing(0)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_20.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.listView_2 = QListView(self.page_25)
        self.listView_2.setObjectName(u"listView_2")
        self.listView_2.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")

        self.verticalLayout_9.addWidget(self.listView_2)


        self.gridLayout_20.addLayout(self.verticalLayout_9, 1, 0, 1, 1)

        self.p25_top_frame = QFrame(self.page_25)
        self.p25_top_frame.setObjectName(u"p25_top_frame")
        self.p25_top_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.verticalLayout_62 = QVBoxLayout(self.p25_top_frame)
        self.verticalLayout_62.setObjectName(u"verticalLayout_62")
        self.back_button_7 = QPushButton(self.p25_top_frame)
        self.back_button_7.setObjectName(u"back_button_7")
        self.back_button_7.setMinimumSize(QSize(125, 50))
        self.back_button_7.setStyleSheet(u"border-image: url(:/Horus Main Page/backButton.png);")
        self.back_button_7.clicked.connect(partial(self.on_click_to_menu, "back_button_7"))

        self.verticalLayout_62.addWidget(self.back_button_7, 0, Qt.AlignLeft|Qt.AlignTop)

        self.frame_4 = QFrame(self.p25_top_frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label = QLabel(self.frame_4)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(300, 50))
        self.label.setStyleSheet(u"border-image: url(:/Horus Main Page/listanalysis.png);")

        self.horizontalLayout_15.addWidget(self.label, 0, Qt.AlignLeft)

        self.pushButton_5 = QPushButton(self.frame_4)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setMinimumSize(QSize(125, 50))
        self.pushButton_5.setSizeIncrement(QSize(125, 50))
        font77 = QFont()
        font77.setPointSize(14)
        font77.setUnderline(True)
        self.pushButton_5.setFont(font77)
        self.pushButton_5.clicked.connect(self.on_click_delete)

        self.horizontalLayout_15.addWidget(self.pushButton_5, 0, Qt.AlignRight|Qt.AlignVCenter)

        self.pushButton_4 = QPushButton(self.frame_4)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setMinimumSize(QSize(125, 50))
        self.pushButton_4.setSizeIncrement(QSize(125, 50))
        font7 = QFont()
        font7.setPointSize(14)
        font7.setItalic(True)
        self.pushButton_4.setFont(font7)
        self.pushButton_4.setIcon(icon)
        self.pushButton_4.setIconSize(QSize(35, 35))
        self.pushButton_4.clicked.connect(self.on_click_view_saved)

        self.horizontalLayout_15.addWidget(self.pushButton_4, 0, Qt.AlignRight)


        self.verticalLayout_62.addWidget(self.frame_4)


        self.gridLayout_20.addWidget(self.p25_top_frame, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_25)
        
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.gridLayout_5 = QGridLayout(self.page_6)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.page_6_Vert = QVBoxLayout()
        self.page_6_Vert.setSpacing(0)
        self.page_6_Vert.setObjectName(u"page_6_Vert")
        self.pie_top = QFrame(self.page_6)
        self.pie_top.setObjectName(u"pie_top")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.pie_top.sizePolicy().hasHeightForWidth())
        self.pie_top.setSizePolicy(sizePolicy4)
        self.pie_top.setMinimumSize(QSize(0, 0))
        self.pie_top.setMaximumSize(QSize(16777215, 200))
        self.pie_top.setSizeIncrement(QSize(0, 0))
        self.pie_top.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.pie_top.setFrameShape(QFrame.StyledPanel)
        self.pie_top.setFrameShadow(QFrame.Raised)
        self.verticalLayout_18 = QVBoxLayout(self.pie_top)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.back_button_9 = QPushButton(self.pie_top)
        self.back_button_9.setObjectName(u"back_button_9")
        self.back_button_9.setMinimumSize(QSize(125, 50))
        self.back_button_9.setStyleSheet(u"border-image: url(:/Horus Main Page/backButton.png);")
        self.back_button_9.clicked.connect(partial(self.on_click_goto_result, "back_button_9"))

        self.verticalLayout_18.addWidget(self.back_button_9, 0, Qt.AlignLeft|Qt.AlignTop)

        self.label_2 = QLabel(self.pie_top)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(300, 50))
        font7 = QFont()
        font7.setPointSize(24)
        font7.setUnderline(False)
        self.label_2.setFont(font7)
        self.label_2.setStyleSheet(u"")

        self.verticalLayout_18.addWidget(self.label_2)

        self.page_6_Vert.addWidget(self.pie_top, 0, Qt.AlignTop)

        self.p6_chart_frame = QFrame(self.page_6)
        self.p6_chart_frame.setObjectName(u"p6_chart_frame")
        sizePolicy1.setHeightForWidth(self.p6_chart_frame.sizePolicy().hasHeightForWidth())
        self.p6_chart_frame.setSizePolicy(sizePolicy1)
        self.p6_chart_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p6_chart_frame.setFrameShape(QFrame.StyledPanel)
        self.p6_chart_frame.setFrameShadow(QFrame.Raised)
        self.p6_pielayout = QVBoxLayout(self.p6_chart_frame)
        self.p6_pielayout.setObjectName(u"p6_pielayout")

        self.page_6_Vert.addWidget(self.p6_chart_frame)


        self.gridLayout_5.addLayout(self.page_6_Vert, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_6)

        self.page_7 = QWidget()
        self.page_7.setObjectName(u"page_7")
        self.verticalLayout_17 = QVBoxLayout(self.page_7)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.frame = QFrame(self.page_7)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_20 = QVBoxLayout(self.frame)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.pie_top_2 = QFrame(self.frame)
        self.pie_top_2.setObjectName(u"pie_top_2")
        sizePolicy4.setHeightForWidth(self.pie_top_2.sizePolicy().hasHeightForWidth())
        self.pie_top_2.setSizePolicy(sizePolicy4)
        self.pie_top_2.setMinimumSize(QSize(0, 0))
        self.pie_top_2.setMaximumSize(QSize(16777215, 200))
        self.pie_top_2.setSizeIncrement(QSize(0, 0))
        self.pie_top_2.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.pie_top_2.setFrameShape(QFrame.StyledPanel)
        self.pie_top_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_19 = QVBoxLayout(self.pie_top_2)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.back_button_10 = QPushButton(self.pie_top_2)
        self.back_button_10.setObjectName(u"back_button_10")
        self.back_button_10.setMinimumSize(QSize(125, 50))
        self.back_button_10.setStyleSheet(u"border-image: url(:/Horus Main Page/backButton.png);")
        self.back_button_10.clicked.connect(partial(self.on_click_goto_result, "back_button_10"))

        self.verticalLayout_19.addWidget(self.back_button_10, 0, Qt.AlignLeft|Qt.AlignTop)

        self.label_3 = QLabel(self.pie_top_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(300, 50))
        self.label_3.setFont(font7)
        self.label_3.setStyleSheet(u"")

        self.verticalLayout_19.addWidget(self.label_3)


        self.verticalLayout_20.addWidget(self.pie_top_2)

        self.p6_chart_frame_2 = QFrame(self.frame)
        self.p6_chart_frame_2.setObjectName(u"p6_chart_frame_2")
        sizePolicy1.setHeightForWidth(self.p6_chart_frame_2.sizePolicy().hasHeightForWidth())
        self.p6_chart_frame_2.setSizePolicy(sizePolicy1)
        self.p6_chart_frame_2.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p6_chart_frame_2.setFrameShape(QFrame.StyledPanel)
        self.p6_chart_frame_2.setFrameShadow(QFrame.Raised)
        self.p7_histogramlayout = QVBoxLayout(self.p6_chart_frame_2)
        self.p7_histogramlayout.setObjectName(u"p7_histogramlayout")

        self.verticalLayout_20.addWidget(self.p6_chart_frame_2)


        self.verticalLayout_16.addWidget(self.frame)


        self.verticalLayout_17.addLayout(self.verticalLayout_16)

        self.stackedWidget.addWidget(self.page_7)
        
        self.page_8 = QWidget()
        self.page_8.setObjectName(u"page_8")
        self.verticalLayout_30 = QVBoxLayout(self.page_8)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.verticalLayout_21 = QVBoxLayout()
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.p8mainframe = QFrame(self.page_8)
        self.p8mainframe.setObjectName(u"p8mainframe")
        self.p8mainframe.setFrameShape(QFrame.StyledPanel)
        self.p8mainframe.setFrameShadow(QFrame.Raised)
        self.verticalLayoutp8 = QVBoxLayout(self.p8mainframe)
        self.verticalLayoutp8.setObjectName(u"verticalLayoutp8")
        self.p8_top = QFrame(self.p8mainframe)
        self.p8_top.setObjectName(u"p8_top")
        self.p8_top.setGeometry(QRect(0, 0, 1025, 129))
        sizePolicy4.setHeightForWidth(self.p8_top.sizePolicy().hasHeightForWidth())
        self.p8_top.setSizePolicy(sizePolicy4)
        self.p8_top.setMinimumSize(QSize(0, 0))
        self.p8_top.setMaximumSize(QSize(16777215, 200))
        self.p8_top.setSizeIncrement(QSize(0, 0))
        self.p8_top.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p8_top.setFrameShape(QFrame.StyledPanel)
        self.p8_top.setFrameShadow(QFrame.Raised)
        self.verticalLayout_25 = QVBoxLayout(self.p8_top)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.back_button_11 = QPushButton(self.p8_top)
        self.back_button_11.setObjectName(u"back_button_11")
        self.back_button_11.setMinimumSize(QSize(125, 50))
        self.back_button_11.setStyleSheet(u"border-image: url(:/Horus Main Page/backButton.png);")
        self.back_button_11.clicked.connect(partial(self.on_click_goto_result, "back_button_11"))

        self.verticalLayout_25.addWidget(self.back_button_11, 0, Qt.AlignLeft|Qt.AlignTop)

        self.label_4 = QLabel(self.p8_top)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(300, 50))
        self.label_4.setFont(font7)
        self.label_4.setStyleSheet(u"")

        self.verticalLayout_25.addWidget(self.label_4)
        self.verticalLayoutp8.addWidget(self.p8_top)

        self.p8_chart_frame = QFrame(self.p8mainframe)
        self.p8_chart_frame.setObjectName(u"p8_chart_frame")
        self.p8_chart_frame.setGeometry(QRect(0, 136, 1025, 499))
        sizePolicy1.setHeightForWidth(self.p8_chart_frame.sizePolicy().hasHeightForWidth())
        self.p8_chart_frame.setSizePolicy(sizePolicy1)
        self.p8_chart_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p8_chart_frame.setFrameShape(QFrame.StyledPanel)
        self.p8_chart_frame.setFrameShadow(QFrame.Raised)
        self.p8_donutlayout = QVBoxLayout(self.p8_chart_frame)
        self.p8_donutlayout.setObjectName(u"p8_donutlayout")

        self.verticalLayoutp8.addWidget(self.p8_chart_frame)

        self.verticalLayout_21.addWidget(self.p8mainframe)


        self.verticalLayout_30.addLayout(self.verticalLayout_21)

        self.stackedWidget.addWidget(self.page_8)

        self.page_9 = QWidget()
        self.page_9.setObjectName(u"page_9")
        self.verticalLayout_23 = QVBoxLayout(self.page_9)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.verticalLayout_24 = QVBoxLayout()
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.p9MainFrame = QFrame(self.page_9)
        self.p9MainFrame.setObjectName(u"p9MainFrame")
        self.p9MainFrame.setFrameShape(QFrame.StyledPanel)
        self.p9MainFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayoutp9 = QVBoxLayout(self.p9MainFrame)
        self.verticalLayoutp9.setObjectName(u"verticalLayoutp9")
        self.p9Top = QFrame(self.p9MainFrame)
        self.p9Top.setObjectName(u"p9Top")
        self.p9Top.setGeometry(QRect(0, 0, 1025, 129))
        sizePolicy4.setHeightForWidth(self.p9Top.sizePolicy().hasHeightForWidth())
        self.p9Top.setSizePolicy(sizePolicy4)
        self.p9Top.setMinimumSize(QSize(0, 0))
        self.p9Top.setMaximumSize(QSize(16777215, 200))
        self.p9Top.setSizeIncrement(QSize(0, 0))
        self.p9Top.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p9Top.setFrameShape(QFrame.StyledPanel)
        self.p9Top.setFrameShadow(QFrame.Raised)
        self.verticalLayout_26 = QVBoxLayout(self.p9Top)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.back_button_12 = QPushButton(self.p9Top)
        self.back_button_12.setObjectName(u"back_button_12")
        self.back_button_12.setMinimumSize(QSize(125, 50))
        self.back_button_12.setStyleSheet(u"border-image: url(:/Horus Main Page/backButton.png);")
        self.back_button_12.clicked.connect(partial(self.on_click_goto_result, "back_button_12"))

        self.verticalLayout_26.addWidget(self.back_button_12, 0, Qt.AlignLeft|Qt.AlignTop)

        self.label_5 = QLabel(self.p9Top)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(300, 50))
        self.label_5.setFont(font7)
        self.label_5.setStyleSheet(u"")

        self.verticalLayout_26.addWidget(self.label_5)
        self.label_8 = QLabel(self.p9Top)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_26.addWidget(self.label_8)
        self.verticalLayoutp9.addWidget(self.p9Top)

        self.p9_chart_frame = QFrame(self.p9MainFrame)
        self.p9_chart_frame.setObjectName(u"p9_chart_frame")
        self.p9_chart_frame.setGeometry(QRect(0, 136, 1025, 499))
        sizePolicy1.setHeightForWidth(self.p9_chart_frame.sizePolicy().hasHeightForWidth())
        self.p9_chart_frame.setSizePolicy(sizePolicy1)
        self.p9_chart_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p9_chart_frame.setFrameShape(QFrame.StyledPanel)
        self.p9_chart_frame.setFrameShadow(QFrame.Raised)
        self.p9_linelayout = QVBoxLayout(self.p9_chart_frame)
        self.p9_linelayout.setObjectName(u"p9_linelayout")

        self.verticalLayoutp9.addWidget(self.p9_chart_frame)

        self.verticalLayout_24.addWidget(self.p9MainFrame)

        self.verticalLayout_23.addLayout(self.verticalLayout_24)

        self.stackedWidget.addWidget(self.page_9)
        self.page_10 = QWidget()
        self.page_10.setObjectName(u"page_10")
        self.verticalLayout_22 = QVBoxLayout(self.page_10)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_27 = QVBoxLayout()
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.p1mainframe = QFrame(self.page_10)
        self.p1mainframe.setObjectName(u"p1mainframe")
        self.p1mainframe.setFrameShape(QFrame.StyledPanel)
        self.p1mainframe.setFrameShadow(QFrame.Raised)
        self.verticalLayoutp10 = QVBoxLayout(self.p1mainframe)
        self.verticalLayoutp10.setObjectName(u"verticalLayoutp10")
        self.p10top = QFrame(self.p1mainframe)
        self.p10top.setObjectName(u"p10top")
        self.p10top.setGeometry(QRect(0, 0, 1025, 129))
        sizePolicy4.setHeightForWidth(self.p10top.sizePolicy().hasHeightForWidth())
        self.p10top.setSizePolicy(sizePolicy4)
        self.p10top.setMinimumSize(QSize(0, 0))
        self.p10top.setMaximumSize(QSize(16777215, 200))
        self.p10top.setSizeIncrement(QSize(0, 0))
        self.p10top.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p10top.setFrameShape(QFrame.StyledPanel)
        self.p10top.setFrameShadow(QFrame.Raised)
        self.verticalLayout_29 = QVBoxLayout(self.p10top)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.back_button_14 = QPushButton(self.p10top)
        self.back_button_14.setObjectName(u"back_button_14")
        self.back_button_14.setMinimumSize(QSize(125, 50))
        self.back_button_14.setStyleSheet(u"border-image: url(:/Horus Main Page/backButton.png);")
        self.back_button_14.clicked.connect(partial(self.on_click_goto_result, "back_button_14"))

        self.verticalLayout_29.addWidget(self.back_button_14, 0, Qt.AlignLeft|Qt.AlignTop)

        self.label_7 = QLabel(self.p10top)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(300, 50))
        self.label_7.setFont(font7)
        self.label_7.setStyleSheet(u"")

        self.verticalLayout_29.addWidget(self.label_7)
        self.verticalLayoutp10.addWidget(self.p10top)

        self.p10_chart_frame = QFrame(self.p1mainframe)
        self.p10_chart_frame.setObjectName(u"p10_chart_frame")
        self.p10_chart_frame.setGeometry(QRect(0, 136, 1025, 499))
        sizePolicy1.setHeightForWidth(self.p10_chart_frame.sizePolicy().hasHeightForWidth())
        self.p10_chart_frame.setSizePolicy(sizePolicy1)
        self.p10_chart_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p10_chart_frame.setFrameShape(QFrame.StyledPanel)
        self.p10_chart_frame.setFrameShadow(QFrame.Raised)

        self.verticalLayoutp10.addWidget(self.p10_chart_frame)

        self.verticalLayout_27.addWidget(self.p1mainframe)

        self.verticalLayout_22.addLayout(self.verticalLayout_27)

        self.stackedWidget.addWidget(self.page_10)
        
        self.page_11 = QWidget()
        self.page_11.setObjectName(u"page_11")
        self.verticalLayout_31 = QVBoxLayout(self.page_11)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.verticalLayout_28 = QVBoxLayout()
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.frame_3 = QFrame(self.page_11)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_33 = QVBoxLayout(self.frame_3)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.pie_top_4 = QFrame(self.frame_3)
        self.pie_top_4.setObjectName(u"pie_top_4")
        sizePolicy4.setHeightForWidth(self.pie_top_4.sizePolicy().hasHeightForWidth())
        self.pie_top_4.setSizePolicy(sizePolicy4)
        self.pie_top_4.setMinimumSize(QSize(0, 0))
        self.pie_top_4.setMaximumSize(QSize(16777215, 200))
        self.pie_top_4.setSizeIncrement(QSize(0, 0))
        self.pie_top_4.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.pie_top_4.setFrameShape(QFrame.StyledPanel)
        self.pie_top_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_32 = QVBoxLayout(self.pie_top_4)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.back_button_13 = QPushButton(self.pie_top_4)
        self.back_button_13.setObjectName(u"back_button_13")
        self.back_button_13.setMinimumSize(QSize(125, 50))
        self.back_button_13.setStyleSheet(u"border-image: url(:/Horus Main Page/backButton.png);")
        self.back_button_13.clicked.connect(partial(self.on_click_goto_result, "back_button_13"))

        self.verticalLayout_32.addWidget(self.back_button_13, 0, Qt.AlignLeft|Qt.AlignTop)

        self.label_6 = QLabel(self.pie_top_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(300, 50))
        self.label_6.setFont(font7)
        self.label_6.setStyleSheet(u"")

        self.verticalLayout_32.addWidget(self.label_6)


        self.verticalLayout_33.addWidget(self.pie_top_4)

        self.p6_chart_frame_4 = QFrame(self.frame_3)
        self.p6_chart_frame_4.setObjectName(u"p6_chart_frame_4")
        sizePolicy1.setHeightForWidth(self.p6_chart_frame_4.sizePolicy().hasHeightForWidth())
        self.p6_chart_frame_4.setSizePolicy(sizePolicy1)
        self.p6_chart_frame_4.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p6_chart_frame_4.setFrameShape(QFrame.StyledPanel)
        self.p6_chart_frame_4.setFrameShadow(QFrame.Raised)
        
        self.verticalLayout_34 = QVBoxLayout(self.p6_chart_frame_4)
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.label_9 = QLabel(self.p6_chart_frame_4)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")

        self.verticalLayout_34.addWidget(self.label_9, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.verticalLayout_33.addWidget(self.p6_chart_frame_4)


        self.verticalLayout_28.addWidget(self.frame_3)


        self.verticalLayout_31.addLayout(self.verticalLayout_28)

        self.stackedWidget.addWidget(self.page_11)

        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.horus_image_label_2.setText("")
        self.horus_name_label.setText("")
        self.start_button.setText("")
        self.crowd_control_button.setText("")
        self.single_user_button.setText("")
        self.deception_detection_button.setText("")
        self.screen_capture_button.setText("")
        self.list_analysis_button.setText("")
        self.horus_image_label.setText("")
        self.choose_mode_label.setText("")
        self.scanLabelp3.setText(QCoreApplication.translate("Horus", u"SCANNING...", None))
        self.replay_button_3.setText("")
        self.pause_button_3.setText("")
        self.play_button_3.setText("")
        self.pushButton_3.setText("")
        self.back_button_6.setText("")
        self.upload_button_3.setText("")
        self.p3_screen_label.setText("")
        self.scanLabelp4.setText(QCoreApplication.translate("Horus", u"SCANNING...", None))
        #self.replay_button_2.setText("")
        self.pause_button_2.setText("")
        self.play_button_2.setText("")
        self.changeCamButton.setText(QCoreApplication.translate("Horus", u"Change Camera", None))
        self.pushButton_2.setText("")
        self.back_button_5.setText("")
        #self.upload_button_2.setText("")
        self.p4_screen_label.setText("")
        self.detectionLabel.setText(QCoreApplication.translate("Horus", u"Click Start Button to Continue", None))
        self.back_button_4.setText("")
        self.detectionStartButton.setText(QCoreApplication.translate("Horus", u"Start Detection", None))
        self.leftCounterLabel.setText("")
        self.p5_screen_label.setText("")
        self.rightCounterLabel.setText("")
        self.screenCapScanLabel.setText(QCoreApplication.translate("Horus", u"SCANNING...", None))
        #self.replay_button.setText("")
        self.pause_button.setText("")
        self.play_button.setText("")
        self.pushButton.setText("")
        self.back_button_3.setText("")
        #self.upload_button.setText("")
        self.p21_screen_label.setText("")
        self.back_button_2.setText("")
        self.chooseo_output_type.setText("")
        self.viewCodeButton.setText("")
        self.linechart_button.setText("")
        self.pie_button.setText("")
        self.histogram_button.setText("")
        # self.table_button.setText("")
        self.donut_button.setText("")
        self.edit_button.setText("")
        self.download_button.setText("")
        self.back_button.setText("")
        self.analysis_text.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">SCAN2 ANALYSIS</span></p></body></html>", None))
        self.back_button_8.setText("")
        self.capture_label.setText("")
        self.runbutton.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:18pt;\">RUN</span></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.runbutton.setText(QCoreApplication.translate("MainWindow", u"RUN", None))
        self.back_button_7.setText("")
        self.label.setText("")
        self.pushButton_5.setText(QCoreApplication.translate("Horus", u"DELETE", None))
        self.pushButton_4.setText(QCoreApplication.translate("Horus", u"Continue", None))
        self.back_button_9.setText("")
        self.label_2.setText(QCoreApplication.translate("Horus", u"<html><head/><body><p align=\"center\"><span style=\" color:#646464;\">PIE CHART</span></p></body></html>", None))
        self.back_button_10.setText("")
        self.label_3.setText(QCoreApplication.translate("Horus", u"<html><head/><body><p align=\"center\"><span style=\" color:#646464;\">HISTOGRAM</span></p></body></html>", None))
        self.back_button_11.setText("")
        self.label_4.setText(QCoreApplication.translate("Horus", u"<html><head/><body><p align=\"center\"><span style=\" color:#646464;\">Donut Chart</span></p></body></html>", None))
        self.back_button_12.setText("")
        self.label_5.setText(QCoreApplication.translate("Horus", u"<html><head/><body><p align=\"center\"><span style=\" color:#646464;\">Line Chart</span></p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("Horus", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Happy &gt; Sad &gt; Disgust &gt; Angry &gt; Neutral &gt; Suprised &gt; Fear </span></p></body></html>", None))
        self.back_button_14.setText("")
        self.label_7.setText(QCoreApplication.translate("Horus", u"<html><head/><body><p align=\"center\"><span style=\" color:#646464;\">Table</span></p></body></html>", None))
        self.back_button_13.setText("")
        self.label_6.setText(QCoreApplication.translate("Horus", u"<html><head/><body><p align=\"center\"><span style=\" color:#646464;\">View Recorded Data</span></p></body></html>", None))
        self.label_9.setText("")
    # retranslateUi