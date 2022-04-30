import sys
import os
from ui_interface import *
from PyQt5 import QtGui
from qt_material import *
import ctypes

myappid = 'Horus.main.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        appIcon = PyQt5.QtGui.QIcon()
        appIcon.addFile("logos/Horus-16x16.png", PyQt5.QtCore.QSize(16,16))
        appIcon.addFile("logos/Horus-24x24.png", PyQt5.QtCore.QSize(24,24))
        appIcon.addFile("logos/Horus-32x32.png", PyQt5.QtCore.QSize(32,32))
        appIcon.addFile("logos/Horus-48x48.png", PyQt5.QtCore.QSize(48,48))
        appIcon.addFile("logos/Horus-256x256.png", PyQt5.QtCore.QSize(256,256))
        self.setWindowIcon(appIcon)
        self.setWindowTitle('Horus')
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
