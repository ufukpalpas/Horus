# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled2IeHOPT.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import startscreen_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(889, 695)
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
        self.logo0 = QLabel(self.page)
        self.logo0.setObjectName(u"logo0")
        self.logo0.setMinimumSize(QSize(300, 150))
        self.logo0.setStyleSheet(u"border-image: url(:/Horus Main Page/Horus.png);")

        self.verticalLayout.addWidget(self.logo0, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.name0 = QLabel(self.page)
        self.name0.setObjectName(u"name0")
        self.name0.setMinimumSize(QSize(300, 75))
        self.name0.setStyleSheet(u"border-image: url(:/Horus Main Page/HorusName.png);")

        self.verticalLayout.addWidget(self.name0, 0, Qt.AlignHCenter|Qt.AlignTop)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.start_btn = QPushButton(self.page)
        self.start_btn.setObjectName(u"start_btn")
        self.start_btn.setMinimumSize(QSize(200, 50))
        self.start_btn.setStyleSheet(u"border-image: url(:/Horus Main Page/start.png);")
        self.start_btn.setCheckable(False)
        self.start_btn.setChecked(False)
        self.start_btn.setAutoDefault(False)

        self.verticalLayout_2.addWidget(self.start_btn, 0, Qt.AlignHCenter|Qt.AlignBottom)


        self.gridLayout_2.addLayout(self.verticalLayout_2, 1, 0, 1, 1)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout_3 = QGridLayout(self.page_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.crowd_control_btn = QPushButton(self.page_2)
        self.crowd_control_btn.setObjectName(u"crowd_control_btn")
        self.crowd_control_btn.setMinimumSize(QSize(300, 40))
        self.crowd_control_btn.setStyleSheet(u"border-image: url(:/Horus Main Page/crowdcontrol.png);")

        self.verticalLayout_7.addWidget(self.crowd_control_btn, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_3.addLayout(self.verticalLayout_7, 3, 0, 1, 1)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.single_user_btn = QPushButton(self.page_2)
        self.single_user_btn.setObjectName(u"single_user_btn")
        self.single_user_btn.setMinimumSize(QSize(300, 50))
        self.single_user_btn.setStyleSheet(u"border-image: url(:/Horus Main Page/singleuser.png);")

        self.verticalLayout_6.addWidget(self.single_user_btn, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_3.addLayout(self.verticalLayout_6, 2, 0, 1, 1)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.deception_det_btn = QPushButton(self.page_2)
        self.deception_det_btn.setObjectName(u"deception_det_btn")
        self.deception_det_btn.setMinimumSize(QSize(400, 50))
        self.deception_det_btn.setStyleSheet(u"border-image: url(:/Horus Main Page/deceptiondetection.png);")

        self.verticalLayout_8.addWidget(self.deception_det_btn, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_3.addLayout(self.verticalLayout_8, 4, 0, 1, 1)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.screen_cap_btn = QPushButton(self.page_2)
        self.screen_cap_btn.setObjectName(u"screen_cap_btn")
        self.screen_cap_btn.setMinimumSize(QSize(350, 35))
        self.screen_cap_btn.setStyleSheet(u"border-image: url(:/Horus Main Page/screencapt\u0131ure.png);")

        self.verticalLayout_11.addWidget(self.screen_cap_btn, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_3.addLayout(self.verticalLayout_11, 6, 0, 1, 1)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.pushButton_3 = QPushButton(self.page_2)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(400, 40))
        self.pushButton_3.setStyleSheet(u"border-image: url(:/Horus Main Page/lastanalyses.png);")

        self.verticalLayout_10.addWidget(self.pushButton_3, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_3.addLayout(self.verticalLayout_10, 5, 0, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.logo1 = QLabel(self.page_2)
        self.logo1.setObjectName(u"logo1")
        self.logo1.setMinimumSize(QSize(200, 100))
        self.logo1.setStyleSheet(u"border-image: url(:/Horus Main Page/Horus.png);")

        self.verticalLayout_3.addWidget(self.logo1, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_3.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.name1 = QLabel(self.page_2)
        self.name1.setObjectName(u"name1")
        self.name1.setMinimumSize(QSize(400, 50))
        self.name1.setStyleSheet(u"border-image: url(:/Horus Main Page/choosemode.png);")

        self.verticalLayout_4.addWidget(self.name1, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_3.addLayout(self.verticalLayout_4, 1, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.stackedWidget.addWidget(self.page_3)

        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.logo0.setText("")
        self.name0.setText("")
        self.start_btn.setText("")
        self.crowd_control_btn.setText("")
        self.single_user_btn.setText("")
        self.deception_det_btn.setText("")
        self.screen_cap_btn.setText("")
        self.pushButton_3.setText("")
        self.logo1.setText("")
        self.name1.setText("")
    # retranslateUi

