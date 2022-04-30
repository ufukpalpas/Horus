from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import cv2

class VideoSingleThread(QThread): # iu hard coded mp4 adlarını düzenle
    ImageUpdate = pyqtSignal(QImage)
    
    def run(self):
        self.ThreadActive = True
        cap = cv2.VideoCapture("iyi.mp4") # 0 for camera
        self.pauseVid = False
        self.replayVid = False
        self.openVid = False
        self.videoPath = "iyi.mp4"
        
        while self.ThreadActive:
            if self.replayVid and self.videoPath != None:
                cap = cv2.VideoCapture("iyi.mp4")
                self.replayVid = False
            if self.openVid:
                cap = cv2.VideoCapture(self.videoPath)
                self.openVid = False
            if not self.pauseVid:
                ret, frame = cap.read()
            if ret:
                Image = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
                #FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(1920,1080,Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
            cv2.waitKey(1) #kaldır kamera gelince
        cap.release()
     
    def pause(self):
        self.pauseVid = True
    
    def play(self):
        self.pauseVid = False
        
    def replay(self):
        self.replayVid = True
        if self.pauseVid:
            self.pauseVid = False
    
    def open(self, path):
        self.videoPath = path
        self.openVid = True
        self.play()
        
    def stop(self):
        self.ThreadActive = False
        self.quit()

class VideoMultiThread(QThread):
    pass

class ScreenCaptureThread(QThread):
    pass

class LieDetectionThread(QThread): #ilk baştaki yeterse yapma bunu ilerleyen zamanda bak
    pass 

#Kamera + video modalrı yapılacak