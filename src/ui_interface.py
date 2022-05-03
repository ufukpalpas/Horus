# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'HorusNewjrlSeY.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from msilib.schema import ListView
from VideoThread import ScreenCaptureThread, VideoMultiThread, VideoSingleThread
import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog
from functools import partial
import cv2
import startscreen_rc

class Ui_MainWindow(object):
        
    def on_click_to_menu(self, sender):
        self.stackedWidget.setCurrentIndex(1)
        if sender == "back_button_6":
            self.videoSingleThread.stop()
        elif sender == "back_button_5":
            self.multiThread.stop_threads()
        
    def on_click_single_user(self):
        self.stackedWidget.setCurrentIndex(2)
        self.videoSingleThread = VideoSingleThread()
        self.videoSingleThread.start()
        self.videoSingleThread.ImageUpdate.connect(self.ImageUpdateSlot)
        self.videoSingleThread.ValChanged.connect(self.CameraCheckSlot)
        self.p3_screen_label.setPixmap(QPixmap(u":/Horus Main Page/loading.png")) #bunu asağıdan aldık buraya koyduk herbirininkini al kendi butonuna koy
    
    def pauseVidBtn(self, sender):
        if sender == "pause_button_2":
            self.multiThread.pause()
            self.scanLabelp4.setText(QCoreApplication.translate("Horus", u"PAUSED...", None))
        elif sender == "pause_button_3":
            self.videoSingleThread.pause()
            self.scanLabelp3.setText(QCoreApplication.translate("Horus", u"PAUSED...", None))
        
    def playVidBtn(self, sender):
        if sender == "play_button_2":
            self.multiThread.play()
            self.scanLabelp4.setText(QCoreApplication.translate("Horus", u"SCANNING...", None))
        elif sender == "play_button_3":
            self.videoSingleThread.play()
            self.scanLabelp3.setText(QCoreApplication.translate("Horus", u"SCANNING...", None))

    
    def replayVidBtn(self):
        self.videoSingleThread.replay()
    
    def on_click_list_analyses(self):
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
            self.multiThread.startThreads()
            self.multiThread.getCurrentImageUpdate().connect(self.ImageUpdateSlot_2)#   ImageUpdate.connect(self.ImageUpdateSlot)
            self.multiThread.getCurrentValChanged().connect(self.CameraCheckSlot)#   ValChanged.connect(self.CameraCheckSlot)
            self.stackedWidget.setCurrentIndex(3)
            self.p4_screen_label.setPixmap(QPixmap(u":/Horus Main Page/loading.png"))
        else:
            print("No camera Selected")
    def on_click_deception_detection(self):
        self.p5_screen_label.setPixmap(QPixmap(u":/Horus Main Page/loading.png"))
        self.stackedWidget.setCurrentIndex(4)
    def on_click_screen_capture(self):
        self.screenCapture = ScreenCaptureThread()
        self.screenCapture.start()
        self.screenCapture.ImageUpdate.connect(self.ImageUpdateSlot_3)
        self.screenCapture.ValChanged.connect(self.CameraCheckSlot)
        self.p21_screen_label.setPixmap(QPixmap(u":/Horus Main Page/loading.png"))
        self.stackedWidget.setCurrentIndex(5)   
    def on_click_goto_result(self):
        self.stackedWidget.setCurrentIndex(6)
        
    def ImageUpdateSlot(self, Image):
        self.p3_screen_label.setPixmap(PyQt5.QtGui.QPixmap.fromImage(Image))

    def ImageUpdateSlot_2(self, Image):
        self.p4_screen_label.setPixmap(PyQt5.QtGui.QPixmap.fromImage(Image))
        
    def ImageUpdateSlot_3(self, Image):
        self.p21_screen_label.setPixmap(PyQt5.QtGui.QPixmap.fromImage(Image))
    
    def CameraCheckSlot(self, val):
        if val == 1:
            stt = u":/Horus Main Page/nocam.png"
        self.p3_screen_label.setPixmap(QPixmap(stt))
        self.p4_screen_label.setPixmap(QPixmap(stt))
        self.p5_screen_label.setPixmap(QPixmap(stt))
        self.p21_screen_label.setPixmap(QPixmap(stt))
        
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

        self.horizontalLayout.addWidget(self.scanLabelp3, 0, Qt.AlignHCenter)

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
        self.pushButton_3.clicked.connect(self.on_click_goto_result)

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

        self.p3_middle_frame = QFrame(self.page_3)
        self.p3_middle_frame.setObjectName(u"p3_middle_frame")
        self.p3_middle_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p3_middle_frame.setLineWidth(0)
        self.screenlayout = QVBoxLayout(self.p3_middle_frame)
        self.screenlayout.setSpacing(0)
        self.screenlayout.setObjectName(u"screenlayout")
        self.screenlayout.setContentsMargins(0, 0, 0, 0)
        self.p3_screen_label = QLabel(self.p3_middle_frame)
        self.p3_screen_label.setObjectName(u"p3_screen_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.p3_screen_label.sizePolicy().hasHeightForWidth())
        self.p3_screen_label.setSizePolicy(sizePolicy1)

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

        self.horizontalLayout_6.addWidget(self.scanLabelp4, 0, Qt.AlignHCenter)

        self.replay_button_2 = QPushButton(self.p4_bottom_frame)
        self.replay_button_2.setObjectName(u"replay_button_2")
        self.replay_button_2.setMinimumSize(QSize(50, 50))
        self.replay_button_2.setStyleSheet(u"border-image: url(:/Horus Main Page/repeat.png);")

        self.horizontalLayout_6.addWidget(self.replay_button_2, 0, Qt.AlignHCenter|Qt.AlignBottom)

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
        self.pushButton_2.clicked.connect(self.on_click_goto_result)

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

        self.upload_button_2 = QPushButton(self.p4_top_frame)
        self.upload_button_2.setObjectName(u"upload_button_2")
        self.upload_button_2.setMinimumSize(QSize(80, 50))
        self.upload_button_2.setStyleSheet(u"border-image: url(:/Horus Main Page/upload.png);")

        self.horizontalLayout_3.addWidget(self.upload_button_2, 0, Qt.AlignRight|Qt.AlignTop)


        self.gridLayout_14.addWidget(self.p4_top_frame, 0, 0, 1, 1)

        self.p4_middle_frame = QFrame(self.page_4)
        self.p4_middle_frame.setObjectName(u"p4_middle_frame")
        self.p4_middle_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p4_middle_frame.setLineWidth(0)
        self.screenlayout2 = QVBoxLayout(self.p4_middle_frame)
        self.screenlayout2.setSpacing(0)
        self.screenlayout2.setObjectName(u"screenlayout2")
        self.screenlayout2.setContentsMargins(0, 0, 0, 0)
        self.p4_screen_label = QLabel(self.p4_middle_frame)
        self.p4_screen_label.setObjectName(u"p4_screen_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.p4_screen_label.sizePolicy().hasHeightForWidth())
        self.p4_screen_label.setSizePolicy(sizePolicy2)

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
        self.stand_still_label = QTextBrowser(self.p5_bottom_frame)
        self.stand_still_label.setObjectName(u"stand_still_label")
        self.stand_still_label.setMaximumSize(QSize(200, 50))
        self.stand_still_label.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")

        self.verticalLayout_61.addWidget(self.stand_still_label, 0, Qt.AlignHCenter|Qt.AlignBottom)


        self.gridLayout_15.addWidget(self.p5_bottom_frame, 2, 0, 1, 1)

        self.p5_top_frame = QFrame(self.page_5)
        self.p5_top_frame.setObjectName(u"p5_top_frame")
        sizePolicy.setHeightForWidth(self.p5_top_frame.sizePolicy().hasHeightForWidth())
        self.p5_top_frame.setSizePolicy(sizePolicy)
        self.p5_top_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p5_top_frame.setLineWidth(0)
        self.verticalLayout_59 = QVBoxLayout(self.p5_top_frame)
        self.verticalLayout_59.setSpacing(0)
        self.verticalLayout_59.setObjectName(u"verticalLayout_59")
        self.verticalLayout_59.setContentsMargins(0, 0, 0, 0)
        self.back_button_4 = QPushButton(self.p5_top_frame)
        self.back_button_4.setObjectName(u"back_button_4")
        self.back_button_4.setMinimumSize(QSize(125, 50))
        self.back_button_4.setStyleSheet(u"border-image: url(:/Horus Main Page/backButton.png);")
        self.back_button_4.clicked.connect(partial(self.on_click_to_menu, "back_button_4"))

        self.verticalLayout_59.addWidget(self.back_button_4, 0, Qt.AlignLeft|Qt.AlignTop)


        self.gridLayout_15.addWidget(self.p5_top_frame, 0, 0, 1, 1)

        self.p5_middle_frame = QFrame(self.page_5)
        self.p5_middle_frame.setObjectName(u"p5_middle_frame")
        self.p5_middle_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p5_middle_frame.setLineWidth(0)
        self.screenlayout3 = QVBoxLayout(self.p5_middle_frame)
        self.screenlayout3.setSpacing(0)
        self.screenlayout3.setObjectName(u"screenlayout3")
        self.screenlayout3.setContentsMargins(0, 0, 0, 0)
        self.p5_screen_label = QLabel(self.p5_middle_frame)
        self.p5_screen_label.setObjectName(u"p5_screen_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.p5_screen_label.sizePolicy().hasHeightForWidth())
        self.p5_screen_label.setSizePolicy(sizePolicy3)

        self.screenlayout3.addWidget(self.p5_screen_label, 0, Qt.AlignHCenter|Qt.AlignVCenter)

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
        self.scanning_label = QTextBrowser(self.p21_bottom_frame)
        self.scanning_label.setObjectName(u"scanning_label")
        self.scanning_label.setMaximumSize(QSize(200, 50))
        self.scanning_label.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")

        self.horizontalLayout_8.addWidget(self.scanning_label, 0, Qt.AlignHCenter|Qt.AlignBottom)

        self.replay_button = QPushButton(self.p21_bottom_frame)
        self.replay_button.setObjectName(u"replay_button")
        self.replay_button.setMinimumSize(QSize(50, 50))
        self.replay_button.setStyleSheet(u"border-image: url(:/Horus Main Page/repeat.png);")

        self.horizontalLayout_8.addWidget(self.replay_button, 0, Qt.AlignHCenter|Qt.AlignBottom)

        self.pause_button = QPushButton(self.p21_bottom_frame)
        self.pause_button.setObjectName(u"pause_button")
        self.pause_button.setMinimumSize(QSize(50, 50))
        self.pause_button.setStyleSheet(u"border-image: url(:/Horus Main Page/stop.png);")

        self.horizontalLayout_8.addWidget(self.pause_button, 0, Qt.AlignHCenter|Qt.AlignBottom)

        self.play_button = QPushButton(self.p21_bottom_frame)
        self.play_button.setObjectName(u"play_button")
        self.play_button.setMinimumSize(QSize(50, 50))
        self.play_button.setStyleSheet(u"border-image: url(:/Horus Main Page/play.png);")

        self.horizontalLayout_8.addWidget(self.play_button, 0, Qt.AlignHCenter|Qt.AlignBottom)

        self.pushButton = QPushButton(self.p21_bottom_frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(100, 50))
        self.pushButton.setStyleSheet(u"border-image: url(:/Horus Main Page/gotoresults.png);")
        self.pushButton.clicked.connect(self.on_click_goto_result)

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

        self.upload_button = QPushButton(self.p21_top_frame)
        self.upload_button.setObjectName(u"upload_button")
        self.upload_button.setMinimumSize(QSize(80, 50))
        self.upload_button.setStyleSheet(u"border-image: url(:/Horus Main Page/upload.png);")

        self.horizontalLayout_7.addWidget(self.upload_button, 0, Qt.AlignRight|Qt.AlignTop)


        self.gridLayout_16.addWidget(self.p21_top_frame, 0, 0, 1, 1)

        self.p21_middle_frame = QFrame(self.page_21)
        self.p21_middle_frame.setObjectName(u"p21_middle_frame")
        self.p21_middle_frame.setStyleSheet(u"border-image: url(:/Horus Main Page/empty.png);")
        self.p21_middle_frame.setLineWidth(0)
        self.screenlayout4 = QVBoxLayout(self.p21_middle_frame)
        self.screenlayout4.setSpacing(0)
        self.screenlayout4.setObjectName(u"screenlayout4")
        self.screenlayout4.setContentsMargins(0, 0, 0, 0)
        self.p21_screen_label = QLabel(self.p21_middle_frame)
        self.p21_screen_label.setObjectName(u"p21_screen_label")
        sizePolicy2.setHeightForWidth(self.p21_screen_label.sizePolicy().hasHeightForWidth())
        self.p21_screen_label.setSizePolicy(sizePolicy2)
        
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
        #self.back_button_2.clicked.connect(self.on_click_to_menu) #2 yerden erişim sağlanabiliyo hallet

        self.verticalLayout_13.addWidget(self.back_button_2, 0, Qt.AlignLeft|Qt.AlignTop)

        self.chooseo_output_type = QLabel(self.page_22)
        self.chooseo_output_type.setObjectName(u"chooseo_output_type")
        self.chooseo_output_type.setMinimumSize(QSize(400, 50))
        self.chooseo_output_type.setStyleSheet(u"border-image: url(:/Horus Main Page/chooseoutputtype.png);")

        self.verticalLayout_13.addWidget(self.chooseo_output_type, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_17.addLayout(self.verticalLayout_13, 0, 0, 1, 1)

        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")

        self.gridLayout_17.addLayout(self.verticalLayout_15, 3, 0, 1, 1)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.linechart_button = QPushButton(self.page_22)
        self.linechart_button.setObjectName(u"linechart_button")
        self.linechart_button.setMinimumSize(QSize(150, 40))
        self.linechart_button.setStyleSheet(u"border-image: url(:/Horus Main Page/linechart.png);")

        self.horizontalLayout_9.addWidget(self.linechart_button, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.pie_button = QPushButton(self.page_22)
        self.pie_button.setObjectName(u"pie_button")
        self.pie_button.setMinimumSize(QSize(150, 40))
        self.pie_button.setStyleSheet(u"border-image: url(:/Horus Main Page/pie.png);")

        self.horizontalLayout_9.addWidget(self.pie_button, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.histogram_button = QPushButton(self.page_22)
        self.histogram_button.setObjectName(u"histogram_button")
        self.histogram_button.setMinimumSize(QSize(150, 40))
        self.histogram_button.setStyleSheet(u"border-image: url(:/Horus Main Page/histogram.png);")

        self.horizontalLayout_9.addWidget(self.histogram_button, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.table_button = QPushButton(self.page_22)
        self.table_button.setObjectName(u"table_button")
        self.table_button.setMinimumSize(QSize(150, 40))
        self.table_button.setStyleSheet(u"border-image: url(:/Horus Main Page/table.png);")

        self.horizontalLayout_9.addWidget(self.table_button, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.donut_button = QPushButton(self.page_22)
        self.donut_button.setObjectName(u"donut_button")
        self.donut_button.setMinimumSize(QSize(150, 40))
        self.donut_button.setStyleSheet(u"border-image: url(:/Horus Main Page/donut.png);")

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

        self.label = QLabel(self.p25_top_frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(300, 50))
        self.label.setStyleSheet(u"border-image: url(:/Horus Main Page/listanalysis.png);")

        self.verticalLayout_62.addWidget(self.label, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_20.addWidget(self.p25_top_frame, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_25)

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
        self.replay_button_2.setText("")
        self.pause_button_2.setText("")
        self.play_button_2.setText("")
        self.changeCamButton.setText(QCoreApplication.translate("Horus", u"Change Camera", None))
        self.pushButton_2.setText("")
        self.back_button_5.setText("")
        self.upload_button_2.setText("")
        self.p4_screen_label.setText("")
        self.stand_still_label.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">STAND STILL...</span></p></body></html>", None))
        self.back_button_4.setText("")
        self.p5_screen_label.setText("")
        self.scanning_label.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">SCANNING...</span></p></body></html>", None))
        self.replay_button.setText("")
        self.pause_button.setText("")
        self.play_button.setText("")
        self.pushButton.setText("")
        self.back_button_3.setText("")
        self.upload_button.setText("")
        self.p21_screen_label.setText("")
        self.back_button_2.setText("")
        self.chooseo_output_type.setText("")
        self.linechart_button.setText("")
        self.pie_button.setText("")
        self.histogram_button.setText("")
        self.table_button.setText("")
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
    # retranslateUi

