from cmath import nan
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
import collections
import random
import string
import glob

def randomStr(self):
    letters = string.ascii_letters
    st = ''.join(random.choice(letters) for i in range(10))
    return st

class VideoSingleThread(QThread):
    ImageUpdate = pyqtSignal(QImage) #thread signal forward attachment
    ValChanged = pyqtSignal(int) #camera check forward
    EmotionUpdate = pyqtSignal(list) #emotions to charts
    Analysis = pyqtSignal(list) #List of analysis of emotions
    RandomSender = pyqtSignal(str)
    
    
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
        self.emitEmoSpeed = 4
    
    def run(self):
        self.ThreadActive = True
        cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc('X','V','I','D') #(*'MP42')
        rand_string = randomStr(self)
        name_of = "saved_videos\\single_video_" + str(rand_string) +".avi"
        self.RandomSender.emit(rand_string)
        videoWriter = cv2.VideoWriter(str(name_of), fourcc, 10.0, (640, 480))
        # if not cap.isOpened():
        #     print("^No camera detected!")
        self.changePixmap = True
        self.pauseVid = False
        self.replayVid = False
        self.openVid = False
        self.videoPath = None
        emotions = []
        emotionsPast = [[]]
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
                            #lable_violation = 'Confidence: {}'.format(str(np.round(np.max(predictions[0])*100,1))+ "%")
                            emotions = list(np.round(predictions*100))
                            ##print(str(np.round(predictions*100)))
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
                    #average_emotion = self.captured_emotions/ np.sum(self.captured_emotions)
                    #print("av: ", self.average_emotions)
                #print("cap: ", maxed_emotion, " with ac: ", average_emotion)
                frame_to_write = cv2.resize(frame, (640, 480))
                videoWriter.write(frame_to_write)
                Image_ = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
                #Image = cv2.resize(Image,(1920,1080))
                #FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(Image_.data, Image_.shape[1], Image_.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(1920,1080,Qt.KeepAspectRatio)
                if not self.pauseVid:
                    self.ImageUpdate.emit(Pic)
                    if len(emotions) != 0 and collections.Counter(emotionsPast[0]) != collections.Counter(emotions[0]):
                        #print(emotions)
                        self.emitEmoSpeed -= 1
                        if self.emitEmoSpeed == 0:
                            self.EmotionUpdate.emit(emotions)
                            emotionsPast = emotions
                            self.emitEmoSpeed = 8
            else:
                if self.changePixmap:
                    self.ValChanged.emit(1)
                    self.changePixmap = False
            cv2.waitKey(1)
        cap.release()
        videoWriter.release()
        
     
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
    FrameSender = pyqtSignal(np.ndarray)
    
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
                    average_emotion = self.captured_emotions/ np.sum(self.captured_emotions)
                    if self.chosen == 1:
                        analys = list(average_emotion/ np.sum(average_emotion))
                        self.Analysis_Thread.emit(analys)
                    #print("av: ", self.average_emotions)
                #print(" ", self.name, " Emotion with highest acc: ", maxed_emotion)# " with array ac: ", average_emotion)
                if self.chosen == 1:
                    #print("av: ", self.average_emotions)
                    self.frame_sender(frame)
                    #print("Thread ", self.name, " sending")
                #else:
                    #print("Thread ", self.name, " not sending")
            else:
                if self.changePixmap:
                    self.ValChanged.emit(1)
                    self.changePixmap = False
            cv2.waitKey(1) #kald??r kamera gelince
        cap.release
        
    def frame_sender(self, frame):
        self.FrameSender.emit(frame)
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
        #analys = list(self.average_emotions/ np.sum(self.average_emotions))
        #self.Analysis_Thread.emit(analys)
        self.quit()
        
class VideoMultiThread(QThread):
    Analysis = pyqtSignal(list)
    Thread_specific_anal = pyqtSignal(str ,list)
    RandomSender = pyqtSignal(str)
    
    def __init__(self, cameraInds):
        super().__init__()
        self.camerInds = cameraInds
        self.threadCount = len(cameraInds)
        self.currentThread = 0
        self.analysis_array = []
        self.analysis_result = []
        
    def startThreads(self):
        self.threads = []
        fourcc = cv2.VideoWriter_fourcc('X','V','I','D') #(*'MP42')
        rand_string = randomStr(self)
        name_of = "saved_videos\\multi_video_" + str(rand_string) +".avi"
        self.RandomSender.emit(rand_string)
        self.videoWriter = cv2.VideoWriter(str(name_of), fourcc, 10.0, (640, 480))
        for i in range(self.threadCount):
            temp = VideoThread(self.camerInds[i], "thread-" + str(self.camerInds[i]))
            print("Added " , temp.name)
            self.threads.append(temp)
        for i in range(self.threadCount):
            self.frame = None
            self.threads[i].start()
            self.threads[i].Analysis_Thread.connect(self.get_analysis)
            self.threads[i].FrameSender.connect(self.get_frames)
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
        self.analysis_result = np.sum(self.analysis_array, axis=0) / len(self.analysis_array)
        if not np.isnan(self.analysis_result).any():
            self.Analysis.emit(list(self.analysis_result))
    
    def get_analysis(self, anal):
        print("Analysis received from ", self.sender().name, " : ", anal)
        self.analysis_array.append(anal)
        self.analysis_result = np.sum(self.analysis_array, axis=0) / len(self.analysis_array)
        #self.Analysis.emit(list(self.analysis_result))
        self.Thread_specific_anal.emit(self.sender().name, list(anal))
    
    def get_frames(self, frame):
        frame_to_write = cv2.resize(frame, (640, 480))
        self.videoWriter.write(frame_to_write)    
    
    
    def getCurrentImageUpdate(self):
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
    Real_time_analysis = pyqtSignal(list) #real-time analysis of emotions
    RandomSender = pyqtSignal(str)
    
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
        fourcc = cv2.VideoWriter_fourcc('X','V','I','D') #(*'MP42')
        rand_string = randomStr(self)
        name_of = "saved_videos\\screen_video_" + str(rand_string) +".avi"
        self.RandomSender.emit(rand_string)
        self.videoWriter = cv2.VideoWriter(str(name_of), fourcc, 10.0, (640, 480))
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
                    average_emotion = []
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
                        average_emotion = self.captured_emotions/ np.sum(self.captured_emotions)
                        #print("av: ", self.average_emotions)
                    #print("Emotion with highest acc: ", maxed_emotion, " with array ac: ", average_emotion)
                        if len(average_emotion) != 0:
                            self.Real_time_analysis.emit(list(average_emotion))
                    frame_to_write = cv2.resize(frame, (640, 480))
                    self.videoWriter.write(frame_to_write)
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
        if not np.isnan(analysis).any():
            self.Analysis.emit(analysis)
        self.quit()

class LieDetectionThread(QThread):
    ImageUpdate = pyqtSignal(QImage) #thread signal forward attachment
    ValChanged = pyqtSignal(int) #camera check forward
    EmotionUpdate = pyqtSignal(bool) #emotions to charts
    
    def __init__(self):
        super().__init__()
        self.model = model_from_json(open("model.json", "r").read())
        self.model.load_weights('model.h5')
        self.modelFile = "res10_300x300_ssd_iter_140000.caffemodel"
        self.configFile = "deploy.prototxt.txt" 
        self.labelColor = (10, 10, 255)
        self.frameResults = []
        self.filteredResults = []
        
    def run(self):
        cap = cv2.VideoCapture(0)
        self.ThreadActive = True
        self.changePixmap = True
        # Define the codec and create VideoWriter object
        #fourcc = cv2.VideoWriter_fourcc('X','V','I','D') #(*'MP42')
        #videoWriter = cv2.VideoWriter('video.avi', fourcc, 30.0, (640, 480))
        a = 0
        while self.ThreadActive:
            ret, frame = cap.read()
            if ret:
                #frame = cv2.resize(frame, (640, 480))
                #videoWriter.write(frame)
                h,w,_ = frame.shape
                gray_image= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                net = cv2.dnn.readNetFromCaffe(self.configFile, self.modelFile)
                blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0))
                net.setInput(blob)
                faces = net.forward()
                try:
                    for i in range(0, faces.shape[2]):
                        confidence = faces[0, 0, i, 2]
                        if confidence > 0.5:
                            box = faces[0, 0, i, 3:7] * np.array([w, h, w, h])
                            (x, y, x2, y2) = box.astype("int")
                            cv2.rectangle(frame, pt1 = (x,y),pt2 = (x2, y2), color = (10,10,255),thickness =  2)
                            roi_gray = gray_image[y-5:y2+5,x-5:x2+5]
                            roi_gray=cv2.resize(roi_gray,(48,48))
                            image_pixels = img_to_array(roi_gray)
                            image_pixels = np.expand_dims(image_pixels, axis = 0)
                            image_pixels /= 255
                            predictions = self.model.predict(image_pixels)
                            max_index = np.argmax(predictions[0])
                            emotion_detection = ('Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprised', 'Neutral')
                            emotion_prediction = emotion_detection[max_index]
                            cv2.putText(frame, "{}".format(emotion_prediction), (x2 - int((x2-x)/2) -30,y2+20), cv2.FONT_HERSHEY_SIMPLEX,0.7, self.labelColor,2)
                            #lable_violation = 'Confidence: {}'.format(str(np.round(np.max(predictions[0])*100,1))+ "%")
                            percent = int(np.round(np.max(predictions[0])*100))
                            self.frameResults.append([emotion_prediction, percent])
                            ##print(str(np.round(predictions*100)))
                except:
                    pass
                Image_ = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
                #Image = cv2.resize(Image,(1920,1080))
                #FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(Image_.data, Image_.shape[1], Image_.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(1920,1080,Qt.KeepAspectRatio)

                self.ImageUpdate.emit(Pic)
                a += 1
                #print(a)
                if a >= 10*25:
                    break
            else:
                if self.changePixmap:
                    self.ValChanged.emit(1)
                    self.changePixmap = False
        
        cap.release()
        if self.ThreadActive:
            for x in range(len(self.frameResults)):
                if x == 0:
                    self.filteredResults.append(self.frameResults[0])
                    continue
                if x == 1:
                    self.filteredResults.append(self.frameResults[1])
                    continue
                if x == len(self.frameResults) - 1:
                    self.filteredResults.append(self.frameResults[len(self.frameResults) - 1])
                    continue
                if x == len(self.frameResults) - 2:
                    self.filteredResults.append(self.frameResults[len(self.frameResults) - 2])
                    continue
                count = [0,0,0,0,0,0,0]
                average = [0,0,0,0,0,0,0]
                #print("x", x)
                for y in range(5):
                    w = x - 2
                    if self.frameResults[y + w][0] == "Angry":
                        average[0] += int(self.frameResults[y + w][1])
                        count[0] += 1
                    elif self.frameResults[y + w][0] == "Disgust":
                        average[1] += int(self.frameResults[y + w][1])
                        count[1] += 1
                    elif self.frameResults[y + w][0] == "Fear":
                        average[2] += int(self.frameResults[y + w][1])
                        count[2] += 1
                    elif self.frameResults[y + w][0] == "Happy":
                        average[3] += int(self.frameResults[y + w][1])
                        count[3] += 1
                    elif self.frameResults[y + w][0] == "Sad":
                        average[4] += int(self.frameResults[y + w][1])
                        count[4] += 1
                    elif self.frameResults[y + w][0] == "Surprised":
                        average[5] += int(self.frameResults[y + w][1])
                        count[5] += 1
                    elif self.frameResults[y + w][0] == "Neutral":
                        average[6] += int(self.frameResults[y + w][1])
                        count[6] += 1
                maxx = max(count)
                maxVal = count.index(maxx)
                emos = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprised', 'Neutral']
                self.filteredResults.append([emos[maxVal], average[maxVal]/count[maxVal]])
                
            result = False
            countAgain = []
            countAgainTrimed =[]
            counterEmo = 0
            currentEmo = None
            for k in range(len(self.filteredResults)):
                if currentEmo == None:
                    currentEmo = self.frameResults[k][0]
                    counterEmo += 1
                elif currentEmo != self.frameResults[k][0]:
                    countAgain.append(counterEmo)
                    currentEmo = self.frameResults[k][0]
                    counterEmo = 1
                else:
                    counterEmo += 1   
                #print(counterEmo)  
            countAgain.append(counterEmo)       
            #print(countAgain)
            for x in countAgain:
                if x > 8:
                    countAgainTrimed.append(x)
            if len(countAgain) > 10:
                result = True
            print(result)
            self.EmotionUpdate.emit(result)
            """
            countAgain = [0,0,0,0,0,0,0]
            for k in range(len(self.filteredResults)):
                if self.frameResults[k][0] == "Angry":
                    countAgain[0] += 1
                elif self.frameResults[k][0] == "Disgust":
                    countAgain[1] += 1
                elif self.frameResults[k][0] == "Fear":
                    countAgain[2] += 1
                elif self.frameResults[k][0] == "Happy":
                    countAgain[3] += 1
                elif self.frameResults[k][0] == "Sad":
                    countAgain[4] += 1
                elif self.frameResults[k][0] == "Surprised":
                    countAgain[5] += 1
                elif self.frameResults[k][0] == "Neutral":
                    countAgain[6] += 1
            maxemo = max(countAgain)
            maxemoVal = countAgain.index(maxemo)
            result = False
            for j in range(len(self.filteredResults)):
                counter = 0
                if self.filteredResults[k][0] != emos[maxVal]:
                    for m in range(10):
                        if self.filteredResults[k+m][0] == emos[maxVal]:
                            counter += 1
                    if counter > 8:
                        result = True
                        break
        self.EmotionUpdate.emit(result)     
        """           
            #videoWriter.release()
            #cv2.destroyAllWindows() 
    
    def stop(self):
        self.ThreadActive = False
        self.quit()             
        
class View_Analysis(QThread):
    ImageUpdate = pyqtSignal(QImage) #thread signal forward attachment
    def __init__(self, fileName=None):
        super().__init__()
        self.fileName = fileName
    
    def run(self):
        self.ThreadActive = True
        searching = str('saved_videos\\*' + self.fileName + ".avi")
        fileNameList = glob.glob(searching)
        cap = cv2.VideoCapture(fileNameList[0])
        while cap.isOpened() and self.ThreadActive:
            ret, frame = cap.read()
            if ret:
                Image_ = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
                    #Image = cv2.resize(Image,(1920,1080))
                    #FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(Image_.data, Image_.shape[1], Image_.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(1920,1080,Qt.KeepAspectRatio)
                
                self.ImageUpdate.emit(Pic)
                    
    def stop(self):
        self.ThreadActive = False
        self.quit()    
        
        