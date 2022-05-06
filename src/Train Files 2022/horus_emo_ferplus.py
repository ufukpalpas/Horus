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

test_size =  3573 #12055 #

model = model_from_json(open("model.json", "r").read())
model.load_weights('model.h5')
"""face_haar_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt.xml')

cap=cv2.VideoCapture(0)"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#image_dir = os.path.join(BASE_DIR,"test") #fer2013
image_dir = os.path.join(BASE_DIR,"test(ferplus)") #ferplus

datapath2 = "fer2013new.csv"  
dfplus = pd.read_csv(datapath2)
dfplus.head()

"""datapath = "fer2013.csv"  
df = pd.read_csv(datapath)
df.head()"""

"""
for root,dirs, files in os.walk(image_dir):
    for file in files:
        path = os.path.join(root,file)
        label = os.path.basename(os.path.dirname(path)).replace(" ", "-").lower()
        pil_image = Image.open(path)
        final_image = np.array(pil_image, "uint8")
        image_pixels = img_to_array(final_image)
        image_pixels = np.expand_dims(image_pixels, axis = 0)
        image_pixels /= 255
        
        x_test = np.append(x_test, image_pixels)
       #y_test = np.append(y_test, label)
"""

#ferplus
x_test = []
y_test = []

image_direct ="ExpwCleaned" #Expw
fileAt = 1
""" 
for root,dirs, files in os.walk(image_direct):
    for file in files:
        path = os.path.join(root,file)
        if fileAt >= 76342:
            pil_image = Image.open(path).convert('L')
            final_image = np.array(pil_image, "uint8")
            image_pixels = img_to_array(final_image)
            image_pixels = np.expand_dims(image_pixels, axis = 0)
            image_pixels /= 255   
            x_test.append(image_pixels)
        print(fileAt)
        fileAt += 1
    
fileAt = 1
test_lines = []
with open("expwlabels.txt") as file:
    for line in file:
        if fileAt >= 76342:
            test_lines.append(int(line.rstrip()))
        fileAt += 1
y_test = y_test + test_lines
"""
flag = False
for index, row in dfplus.iterrows():      
    #if row['Usage'] == 'PublicTest' or row['Usage'] == 'PrivateTest':
    if row['Usage'] == 'PrivateTest':
        #if str(row[1]) == "fer0028711.png":
        #    flag = True
        if row["NF"] != 10: #and flag:
            max_row = np.argmax([row["neutral"],row["happiness"], row["surprise"], row["sadness"],row["anger"],row["disgust"],row["fear"]])   
            label = -1
            if max_row == 0:
                label = 6
            if max_row == 1:
                label = 3
            if max_row == 2:
                label = 5
            if max_row == 3:
                label = 4
            if max_row == 4:
                label = 0
            if max_row == 5:
                label = 1
            if max_row == 6:
                label = 2
            y_test.append(label)

for root,dirs, files in os.walk(image_dir):
    for file in files:
        path = os.path.join(root,file)
        label = os.path.basename(os.path.dirname(path)).replace(" ", "-").lower()
        pil_image = Image.open(path)
        final_image = np.array(pil_image, "uint8")
        image_pixels = img_to_array(final_image)
        image_pixels = np.expand_dims(image_pixels, axis = 0)
        image_pixels /= 255   
        x_test.append(image_pixels)

x_test = np.array(x_test)
y_test = np.array(y_test)

print(x_test.shape)
print(y_test.shape)

x_test = np.reshape(x_test, (test_size, 48, 48))

with tf.device('/gpu:1'):
    lbl = model.predict(x_test)
labels = [0,1,2,3,4,5,6]
trueCount = 0
#print("label: ", lbl)

for i in range(test_size):
    mx = max(lbl[i][0], lbl[i][1], lbl[i][2], lbl[i][3], lbl[i][4], lbl[i][5], lbl[i][6]) 

    if mx == lbl[i][0]:
        label = labels[0]
    elif mx == lbl[i][1]:
        label = labels[1]
    elif mx == lbl[i][2]:
        label = labels[2]
    elif mx == lbl[i][3]:
        label = labels[3]
    elif mx == lbl[i][4]:
        label = labels[4]
    elif mx == lbl[i][5]:
        label = labels[5]
    else:
        label = labels[6]

    if label == y_test[i]:
        trueCount += 1    
print(test_size, " images tested")
print("True guesses: ", trueCount)
print ("Percentage: ", trueCount*100/test_size)

""" while cap.isOpened():
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