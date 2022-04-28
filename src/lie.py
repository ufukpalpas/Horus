import numpy as np
import cv2
import pickle
import tensorflow as tf
from PIL import Image
#import screeninfo
import os
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.image import load_img,img_to_array
from tensorflow.keras.preprocessing import image
import pandas as pd
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import librosa.display
import librosa

#Video labelları save edilecek ses analiz edilecek
#video sonucu belli bir filtreden geçecek sonra micro emotion bakılacak sonuç alınacak
#sonra weightlere göre çarpılacak çıkan ekrana verilecek


def mp3tomfcc(file_path, max_pad):
  audio, sample_rate = librosa.core.load(file_path)
  mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=20)
  pad_width = max_pad - mfcc.shape[1]
  if (pad_width > 0):
    mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
  else:
    mfcc = mfcc[:,0:max_pad]
  return mfcc

# Sampling frequency
freq = 44100
  
# Recording duration
duration = 5 #change or handle seconds 

with open('LR_model.pkl', 'rb') as f:
    lr = pickle.load(f)
  
# Start recorder with the given values 
# of duration and sample frequency
recording = sd.rec(int(duration * freq), 
                   samplerate=freq, channels=2)
  
# Record audio for the given number of seconds
sd.wait()
  
# This will convert the NumPy array to an audio
# file with the given sampling frequency
sound = write("recording0.wav", freq, recording)
  
# Convert the NumPy array to audio file
audioFile = wv.write("recording1.wav", recording, freq, sampwidth=2)

mfccs = []
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
mfccs.append(mp3tomfcc(BASE_DIR + '/recording1.wav', 1000)) 
mfccs = np.asarray(mfccs)

nsamples, nx, ny = mfccs.shape
X_final = mfccs.reshape((nsamples,nx*ny))

pred = lr.predict_proba(X_final) # predict_proba bu probları veriyomuş [truth, lie]
prede = lr.predict(X_final)
print(pred)
print(prede)

"""
if pred == 0: # 0 truth 1 lie
    print("Doğru söyleyeni 9 köyde sikerler")
else:
    print("Yalancı OÇ")
"""
"""
model = model_from_json(open("model.json", "r").read())
model.load_weights('model.h5')
face_haar_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt.xml')

cap=cv2.VideoCapture(0)

while cap.isOpened():
    res,frame=cap.read()

    height, width , channel = frame.shape
    sub_img = frame[0:int(height/6),0:int(width)]

    black_rect = np.ones(sub_img.shape, dtype=np.uint8)*0
    res = cv2.addWeighted(sub_img, 0.77, black_rect,0.23, 0)
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 0.8
    FONT_THICKNESS = 2
    lable_color = (10, 10, 255)
    lable = "Emotion Detection made by Abhishek"
    lable_dimension = cv2.getTextSize(lable,FONT ,FONT_SCALE,FONT_THICKNESS)[0]
    textX = int((res.shape[1] - lable_dimension[0]) / 2)
    textY = int((res.shape[0] + lable_dimension[1]) / 2)
    cv2.putText(res, lable, (textX,textY), FONT, FONT_SCALE, (0,0,0), FONT_THICKNESS)
    gray_image= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_haar_cascade.detectMultiScale(gray_image )
    try:
        for (x,y, w, h) in faces:
            cv2.rectangle(frame, pt1 = (x,y),pt2 = (x+w, y+h), color = (255,0,0),thickness =  2)
            roi_gray = gray_image[y-5:y+h+5,x-5:x+w+5]
            roi_gray=cv2.resize(roi_gray,(48,48))
            image_pixels = img_to_array(roi_gray)
            image_pixels = np.expand_dims(image_pixels, axis = 0)
            image_pixels /= 255
            predictions = model.predict(image_pixels)
            max_index = np.argmax(predictions[0])
            emotion_detection = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
            emotion_prediction = emotion_detection[max_index]
            cv2.putText(res, "Sentiment: {}".format(emotion_prediction), (0,textY+22+5), FONT,0.7, lable_color,2)
            lable_violation = 'Confidence: {}'.format(str(np.round(np.max(predictions[0])*100,1))+ "%")
            violation_text_dimension = cv2.getTextSize(lable_violation,FONT,FONT_SCALE,FONT_THICKNESS )[0]
            violation_x_axis = int(res.shape[1]- violation_text_dimension[0])
            cv2.putText(res, lable_violation, (violation_x_axis,textY+22+5), FONT,0.7, lable_color,2)
            print("label: ", predictions)
    except :
        pass
    frame[0:int(height/6),0:int(width)] =res
    cv2.imshow('frame', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows """