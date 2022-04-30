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

model = model_from_json(open("model.json", "r").read())
model.load_weights('model.h5')
face_haar_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt.xml')

cap=cv2.VideoCapture(0)

#This part is to test with realtime camera to run it please close the code above and uncommand bellow


while cap.isOpened():
    res,frame=cap.read()

    height, width , channel = frame.shape
    # sub_img = frame[0:int(height/6),0:int(width)]

    # black_rect = np.ones(sub_img.shape, dtype=np.uint8)*0
    # res = cv2.addWeighted(sub_img, 1, black_rect,0, 0)
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 0.8
    FONT_THICKNESS = 2
    labelColor = (10, 10, 255)
    #lable = "Emotion Detection made by Abhishek"
    #lable_dimension = cv2.getTextSize(lable,FONT ,FONT_SCALE,FONT_THICKNESS)[0]
    #textX = int((frame.shape[1] - lable_dimension[0]) / 2)
    #textY = int((frame.shape[0] + lable_dimension[1]) / 2)
    #cv2.putText(frame, lable, (textX,textY), FONT, FONT_SCALE, (0,0,0), FONT_THICKNESS)
    gray_image= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_haar_cascade.detectMultiScale(gray_image )
    try:
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, pt1 = (x,y),pt2 = (x+w, y+h), color = (10,10,255),thickness =  2)
            roi_gray = gray_image[y-5:y+h+5,x-5:x+w+5]
            print(roi_gray.shape)
            roi_gray=cv2.resize(roi_gray,(48,48))
            image_pixels = img_to_array(roi_gray)
            image_pixels = np.expand_dims(image_pixels, axis = 0)
            image_pixels /= 255
            predictions = model.predict(image_pixels)
            max_index = np.argmax(predictions[0])
            emotion_detection = ('Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprised', 'Neutral')
            emotion_prediction = emotion_detection[max_index]
            cv2.putText(frame, "{}".format(emotion_prediction), (x+int(w/2)-30,y+h+20), FONT,0.7, labelColor,2)
            #lable_violation = 'Confidence: {}'.format(str(np.round(np.max(predictions[0])*100,1))+ "%")
            #violation_text_dimension = cv2.getTextSize(lable_violation,FONT,FONT_SCALE,FONT_THICKNESS )[0]
            #violation_x_axis = int(frame.shape[1]- violation_text_dimension[0])
            #cv2.putText(frame, lable_violation, (violation_x_axis,250+5), FONT,0.7, labelColor,2)
            #print("label: ", predictions)
    except :
        pass
    frame[0:int(height/6),0:int(width)] =res
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows 