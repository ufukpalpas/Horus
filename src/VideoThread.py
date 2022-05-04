from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import cv2
from grpc import ChannelConnectivity
import numpy as np
from PIL import Image
import time
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.image import img_to_array
from mss import mss

class VideoSingleThread(QThread):
    ImageUpdate = pyqtSignal(QImage) #thread signal forward attachment
    ValChanged = pyqtSignal(int) #camera check forward
    Analysis = pyqtSignal(list) #List of analysis of emotions
    
    def __init__(self):
        super().__init__()
        self.model = model_from_json(open("model.json", "r").read())
        self.model.load_weights('model.h5')
        #self.face_haar_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt.xml') 
        self.modelFile = "res10_300x300_ssd_iter_140000.caffemodel"
        self.configFile = "deploy.prototxt.txt" 
        self.labelColor = (10, 10, 255)
        self.average_emotions = np.zeros(7, dtype=int)
#        self.average_emotions[0] = 0 #Angry
#        self.average_emotions[1] = 0 #Disgust
#        self.average_emotions[2] = 0 #Fear
#        self.average_emotions[3] = 0 #Happy
#        self.average_emotions[4] = 0 #Sad
#        self.average_emotions[5] = 0 #Surprised
#        self.average_emotions[6] = 0 #Neutral
        self.captured_emotions = self.average_emotions.copy()
    
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
        maxed_emotion = 'Neutral'
        
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
                self.captured_emotions = np.zeros(7, dtype=int)
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
                            if emotion_prediction == 'Angry':
                                self.captured_emotions[0] +=1
                            elif emotion_prediction == 'Disgust':
                                self.captured_emotions[1] +=1
                            elif emotion_prediction == 'Fear':
                                self.captured_emotions[2] +=1
                            elif emotion_prediction == 'Happy':
                                self.captured_emotions[3] +=1
                            elif emotion_prediction == 'Sad':
                                self.captured_emotions[4] +=1
                            elif emotion_prediction == 'Surprised':
                                self.captured_emotions[5] +=1
                            elif emotion_prediction == 'Neutral':
                                self.captured_emotions[6] +=1
                            cv2.putText(frame, "{}".format(emotion_prediction), (x2 - int((x2-x)/2) -30,y2+20), cv2.FONT_HERSHEY_SIMPLEX,0.7, self.labelColor,2)
                except:
                    pass
                max_ind = np.argmax(self.captured_emotions)
                average_emotion = 0
                if self.captured_emotions[max_ind] != 0:
                    if max_ind == 0:
                        self.average_emotions[0] +=1
                        maxed_emotion = 'Angry'
                    elif max_ind == 1:
                        self.average_emotions[1] +=1
                        maxed_emotion = 'Disgust'
                    elif max_ind == 2:
                        self.average_emotions[2] +=1
                        maxed_emotion = 'Fear'
                    elif max_ind == 3:
                        self.average_emotions[3] +=1
                        maxed_emotion = 'Happy'
                    elif max_ind == 4:
                        self.average_emotions[4] +=1
                        maxed_emotion = 'Sad'
                    elif max_ind == 5:
                        self.average_emotions[5] +=1
                        maxed_emotion = 'Surprised'
                    elif max_ind == 6:
                        self.average_emotions[6] +=1
                        maxed_emotion = 'Neutral'
                    average_emotion = self.captured_emotions[max_ind]/ np.sum(self.captured_emotions)
                    #print("av: ", self.average_emotions)
                #print("cap: ", maxed_emotion, " with ac: ", average_emotion)
                Image_ = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
                #Image = cv2.resize(Image,(1920,1080))
                #FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(Image_.data, Image_.shape[1], Image_.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(1920,1080,Qt.KeepAspectRatio)
                if not self.pauseVid:
                    self.ImageUpdate.emit(Pic)
            else:
                if self.changePixmap:
                    self.ValChanged.emit(1)
                    self.changePixmap = False
            cv2.waitKey(1)
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
        analysis = list(self.average_emotions/ np.sum(self.average_emotions))
        self.Analysis.emit(analysis)
        self.quit()

class VideoThread(QThread):
    ImageUpdate = pyqtSignal(QImage) #thread signal forward attachment
    ValChanged = pyqtSignal(int) #camera check forward
    Analysis_Thread = pyqtSignal(list) #list of analysis of emotions
    
    def __init__(self, threadID, name):
        super().__init__()
        self.threadID = threadID
        self.name = name
        self.model = model_from_json(open("model.json", "r").read())
        self.model.load_weights('model.h5')
        #self.face_haar_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt.xml') 
        self.modelFile = "res10_300x300_ssd_iter_140000.caffemodel"
        self.configFile = "deploy.prototxt.txt" 
        self.labelColor = (10, 10, 255)
        self.chosen = 0
        self.average_emotions = np.zeros(7, dtype=int)
#        self.average_emotions[0] = 0 #Angry
#        self.average_emotions[1] = 0 #Disgust
#        self.average_emotions[2] = 0 #Fear
#        self.average_emotions[3] = 0 #Happy
#        self.average_emotions[4] = 0 #Sad
#        self.average_emotions[5] = 0 #Surprised
#        self.average_emotions[6] = 0 #Neutral
        self.captured_emotions = self.average_emotions.copy()

        
    def run(self):
        self.ThreadActive = True
        cap = cv2.VideoCapture(self.threadID)
        # if not cap.isOpened():
        #     print("^No camera detected!")
        self.changePixmap = True
        self.pauseVid = False
        self.replayVid = False
        self.openVid = False
        self.videoPath = None
        maxed_emotion = 'Neutral'
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
                blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0)) #177
                net.setInput(blob)
                faces = net.forward()
                #faces = self.face_haar_cascade.detectMultiScale(gray_image)
                self.captured_emotions = np.zeros(7, dtype=int)
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
                            if emotion_prediction == 'Angry':
                                self.captured_emotions[0] +=1
                            elif emotion_prediction == 'Disgust':
                                self.captured_emotions[1] +=1
                            elif emotion_prediction == 'Fear':
                                self.captured_emotions[2] +=1
                            elif emotion_prediction == 'Happy':
                                self.captured_emotions[3] +=1
                            elif emotion_prediction == 'Sad':
                                self.captured_emotions[4] +=1
                            elif emotion_prediction == 'Surprised':
                                self.captured_emotions[5] +=1
                            elif emotion_prediction == 'Neutral':
                                self.captured_emotions[6] +=1
                            cv2.putText(frame, "{}".format(emotion_prediction), (x2 - int((x2-x)/2) -30,y2+20), cv2.FONT_HERSHEY_SIMPLEX,0.7, self.labelColor,2)
                except:
                    pass
                max_ind = np.argmax(self.captured_emotions)
                average_emotion = 0
                if self.captured_emotions[max_ind] != 0:
                    if max_ind == 0:
                        self.average_emotions[0] +=1
                        maxed_emotion = 'Angry'
                    elif max_ind == 1:
                        self.average_emotions[1] +=1
                        maxed_emotion = 'Disgust'
                    elif max_ind == 2:
                        self.average_emotions[2] +=1
                        maxed_emotion = 'Fear'
                    elif max_ind == 3:
                        self.average_emotions[3] +=1
                        maxed_emotion = 'Happy'
                    elif max_ind == 4:
                        self.average_emotions[4] +=1
                        maxed_emotion = 'Sad'
                    elif max_ind == 5:
                        self.average_emotions[5] +=1
                        maxed_emotion = 'Surprised'
                    elif max_ind == 6:
                        self.average_emotions[6] +=1
                        maxed_emotion = 'Neutral'
                    average_emotion = self.captured_emotions[max_ind]/ np.sum(self.captured_emotions)
                    #print("av: ", self.average_emotions)
                #print("cap: ", maxed_emotion, " with ac: ", average_emotion)
                if self.chosen == 1:
                    self.frame_sender(frame)
                    #print("Thread ", self.name, " sending")
                #else:
                    #print("Thread ", self.name, " not sending")
            else:
                if self.changePixmap:
                    self.ValChanged.emit(1)
                    self.changePixmap = False
            cv2.waitKey(1) #kaldır kamera gelince
        cap.release
        
    def frame_sender(self, frame):
        Image_ = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
                #Image = cv2.resize(Image,(1920,1080))
                #FlippedImage = cv2.flip(Image, 1)
        ConvertToQtFormat = QImage(Image_.data, Image_.shape[1], Image_.shape[0], QImage.Format_RGB888)
        Pic = ConvertToQtFormat.scaled(1600,900,Qt.KeepAspectRatio)
        if not self.pauseVid:
                    self.ImageUpdate.emit(Pic)
    
    def set_chosen(self, choice):
        self.chosen = choice
        print("Thread ", self.threadID, " chosen ", self.chosen)
    
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
        print("Stopped thread ", self.name)
        #analys = list(self.captured_emotions)
        analys = list(self.average_emotions/ np.sum(self.average_emotions))
        self.Analysis_Thread.emit(analys)
        self.quit()
        
class VideoMultiThread(QThread):
    Analysis = pyqtSignal(list)
    def __init__(self, cameraInds):
        super().__init__()
        self.camerInds = cameraInds
        self.threadCount = len(cameraInds)
        self.currentThread = 0
    def startThreads(self):
        self.threads = []
        for i in range(self.threadCount):
            temp = VideoThread(self.camerInds[i], "thread-" + str(self.camerInds[i]))
            print("Added " , temp.name)
            self.threads.append(temp)
        for i in range(self.threadCount):
            self.frame = None
            self.threads[i].start()
            self.threads[i].Analysis_Thread.connect(self.get_analysis)
        self.threads[self.currentThread].set_chosen(1)
        print("sending")
        
        #for i in range(self.threadCount):
            #threads[i].frame_sender(self.frame)
            #self.threads[i].stop()"""
    
    def choose_thread(self, index):
        for i in range(self.threadCount):
            if i == index:
                self.threads[i].set_chosen(1)
            else:
                self.threads[i].set_chosen(0)
    
    def stop_threads(self):
        for i in range(self.threadCount):
            self.threads[i].stop()
    
    def get_analysis(self, anal):
        print("Analysis received from ", self.sender().name, " : ", anal)
    
    def getCurrentImageUpdate(self):
        print("THREADASDAS ", self.currentThread)
        return self.threads[self.currentThread].ImageUpdate
    
    def getCurrentValChanged(self):
        return self.threads[self.currentThread].ValChanged
        
    def pause(self):
        return self.threads[self.currentThread].pause()
    
    def play(self):
        return self.threads[self.currentThread].play()

class ScreenCaptureThread(QThread):
    ImageUpdate = pyqtSignal(QImage) #thread signal forward attachment
    ValChanged = pyqtSignal(int) #camera check forward
    Analysis = pyqtSignal(list) #list of analysis of emotions
    
    def __init__(self):
        super().__init__()
        self.model = model_from_json(open("model.json", "r").read())
        self.model.load_weights('model.h5')
        #self.face_haar_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt.xml') 
        self.modelFile = "res10_300x300_ssd_iter_140000.caffemodel"
        self.configFile = "deploy.prototxt.txt" 
        self.labelColor = (10, 10, 255)
        self.average_emotions = np.zeros(7, dtype=int)
#        self.average_emotions[0] = 0 #Angry
#        self.average_emotions[1] = 0 #Disgust
#        self.average_emotions[2] = 0 #Fear
#        self.average_emotions[3] = 0 #Happy
#        self.average_emotions[4] = 0 #Sad
#        self.average_emotions[5] = 0 #Surprised
#        self.average_emotions[6] = 0 #Neutral
        self.captured_emotions = self.average_emotions.copy()
    
    def run(self):
        self.ThreadActive = True
        cap = cv2.VideoCapture(0)
        # if not cap.isOpened():
        #     print("^No camera detected!")
        self.changePixmap = True
        self.pauseVid = False
        # self.replayVid = False
        # self.openVid = False
        self.videoPath = None
        maxed_emotion = 'Neutral'
        while self.ThreadActive:
            # if self.replayVid and self.videoPath != None:
            #     cap = cv2.VideoCapture(self.videoPath)
            #     self.replayVid = False
            # if self.openVid:
            #     cap = cv2.VideoCapture(self.videoPath)
            #     self.openVid = False
            sct = mss()
            monitor = sct.monitors[1]
                #print(sct.monitors[1])
                #ret, frame = cap.read()
            
            if monitor: 
                if not self.pauseVid:
                    sct_img = sct.grab(monitor)
                    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "RGBX")
                    frame = np.array(img)
                    #print("t: ", frame.shape)
                    h,w,_ = frame.shape #monitor['height'], monitor['width'] 
                    gray_image= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    
                    net = cv2.dnn.readNetFromCaffe(self.configFile, self.modelFile)
                    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0))
                    net.setInput(blob)
                    faces = net.forward()
                    self.captured_emotions = np.zeros(7, dtype=int)
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
                                if emotion_prediction == 'Angry':
                                    self.captured_emotions[0] +=1
                                elif emotion_prediction == 'Disgust':
                                    self.captured_emotions[1] +=1
                                elif emotion_prediction == 'Fear':
                                    self.captured_emotions[2] +=1
                                elif emotion_prediction == 'Happy':
                                    self.captured_emotions[3] +=1
                                elif emotion_prediction == 'Sad':
                                    self.captured_emotions[4] +=1
                                elif emotion_prediction == 'Surprised':
                                    self.captured_emotions[5] +=1
                                elif emotion_prediction == 'Neutral':
                                    self.captured_emotions[6] +=1
                                cv2.putText(frame, "{}".format(emotion_prediction), (x2 - int((x2-x)/2) -30,y2+20), cv2.FONT_HERSHEY_SIMPLEX,0.7, self.labelColor,2)
                    except:
                        pass
                    max_ind = np.argmax(self.captured_emotions)
                    average_emotion = 0
                    if self.captured_emotions[max_ind] != 0:
                        if max_ind == 0:
                            self.average_emotions[0] +=1
                            maxed_emotion = 'Angry'
                        elif max_ind == 1:
                            self.average_emotions[1] +=1
                            maxed_emotion = 'Disgust'
                        elif max_ind == 2:
                            self.average_emotions[2] +=1
                            maxed_emotion = 'Fear'
                        elif max_ind == 3:
                            self.average_emotions[3] +=1
                            maxed_emotion = 'Happy'
                        elif max_ind == 4:
                            self.average_emotions[4] +=1
                            maxed_emotion = 'Sad'
                        elif max_ind == 5:
                            self.average_emotions[5] +=1
                            maxed_emotion = 'Surprised'
                        elif max_ind == 6:
                            self.average_emotions[6] +=1
                            maxed_emotion = 'Neutral'
                        average_emotion = self.captured_emotions[max_ind]/ np.sum(self.captured_emotions)
                        #print("av: ", self.average_emotions)
                    #print("cap: ", maxed_emotion, " with ac: ", average_emotion)
                    Image_ = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
                    #Image = cv2.resize(Image,(1920,1080))
                    #FlippedImage = cv2.flip(Image, 1)
                    ConvertToQtFormat = QImage(Image_.data, Image_.shape[1], Image_.shape[0], QImage.Format_RGB888)
                    Pic = ConvertToQtFormat.scaled(1280,720,Qt.KeepAspectRatio)
                    if not self.pauseVid:
                        self.ImageUpdate.emit(Pic)
            else:
                if self.changePixmap:
                    self.ValChanged.emit(1)
                    self.changePixmap = False
            cv2.waitKey(1)
        #cap.release()
     
    def pause(self):
        self.pauseVid = True
    
    def play(self):
        self.pauseVid = False
        
    def stop(self):
        self.ThreadActive = False
        analysis = list(self.average_emotions/ np.sum(self.average_emotions))
        self.Analysis.emit(analysis)
        self.quit()

class LieDetectionThread(QThread): #ilk baştaki yeterse yapma bunu ilerleyen zamanda bak
    pass 

#Kamera + video modalrı yapılacak