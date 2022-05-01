from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import cv2
import numpy as np
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.image import img_to_array
from mss import mss

class VideoSingleThread(QThread):
    ImageUpdate = pyqtSignal(QImage)
    ValChanged = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.model = model_from_json(open("model.json", "r").read())
        self.model.load_weights('model.h5')
        self.face_haar_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt.xml') 
        self.modelFile = "res10_300x300_ssd_iter_140000.caffemodel"
        self.configFile = "deploy.prototxt.txt" 
        self.labelColor = (10, 10, 255)
    
    def run(self):
        self.ThreadActive = True
        cap = cv2.VideoCapture(0)
        # if not cap.isOpened():
        #     print("^No camera detected!")
        self.changePixmap = True
        self.pauseVid = False
        self.replayVid = False
        self.openVid = False
        self.videoPath = None
        
        while self.ThreadActive:
            if self.replayVid and self.videoPath != None:
                cap = cv2.VideoCapture(self.videoPath)
                self.replayVid = False
            if self.openVid:
                cap = cv2.VideoCapture(self.videoPath)
                self.openVid = False
            if not self.pauseVid:
                ret, frame = cap.read()
            
            if ret:
                h,w,_ = frame.shape
                gray_image= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                net = cv2.dnn.readNetFromCaffe(self.configFile, self.modelFile)
                blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0))
                net.setInput(blob)
                faces = net.forward()
                #faces = self.face_haar_cascade.detectMultiScale(gray_image)
                try:
                    for i in range(0, faces.shape[2]):
                        if self.pauseVid:
                            break
                        confidence = faces[0, 0, i, 2]
                        if confidence > 0.5:
                            box = faces[0, 0, i, 3:7] * np.array([w, h, w, h])
                            (x, y, x2, y2) = box.astype("int")
                            cv2.rectangle(frame, pt1 = (x,y),pt2 = (x2, y2), color = (10,10,255),thickness =  2)
                            roi_gray = gray_image[y-5:y2+5,x-5:x2+5]
                            # if roi_gray.shape[1] == 0 or roi_gray.shape[0] == 0:
                            #     continue
                            roi_gray=cv2.resize(roi_gray,(48,48))
                            image_pixels = img_to_array(roi_gray)
                            image_pixels = np.expand_dims(image_pixels, axis = 0)
                            image_pixels /= 255
                            predictions = self.model.predict(image_pixels)
                            max_index = np.argmax(predictions[0])
                            emotion_detection = ('Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprised', 'Neutral')
                            emotion_prediction = emotion_detection[max_index]
                            cv2.putText(frame, "{}".format(emotion_prediction), (x2 - int((x2-x)/2) -30,y2+20), cv2.FONT_HERSHEY_SIMPLEX,0.7, self.labelColor,2)
                except:
                    pass
                Image = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
                #Image = cv2.resize(Image,(1920,1080))
                #FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(1920,1080,Qt.KeepAspectRatio)
                if not self.pauseVid:
                    self.ImageUpdate.emit(Pic)
            else:
                if self.changePixmap:
                    self.ValChanged.emit(1)
                    self.changePixmap = False
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