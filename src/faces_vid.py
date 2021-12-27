import os
import numpy as np
import cv2
from PIL import Image
import pickle
import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop,SGD,Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt.xml')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
video_dir = os.path.join(BASE_DIR,"video4.mp4")

videoObj = cv2.VideoCapture(video_dir)

images_array = []
images_array = np.array(images_array)

success = 1
count = 0
im_x = 0
im_y = 0
im_z = 0

while success:
    success, image = videoObj.read()
    if success:
        images_array = np.append(images_array, image)
        count+=1
        print(image.shape)
        im_x = image.shape[0]
        im_y = image.shape[1]
        im_z = image.shape[2]
    print(count)
images_array = np.reshape(images_array, (count, im_x, im_y, im_z))
print(images_array.shape)    

recog = tf.keras.models.load_model("model")
labels = ["positive", "neutral", "negative"]
for i in range(images_array.shape[0]):
    im = np.array(images_array[i], "uint8")
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
     
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

    for(x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = im[y:y+h, x:x+w]
        size = (250, 250)
        image_array = np.array(roi_color, "uint8")
        pil_image = Image.fromarray(image_array)  
        final_image = pil_image.resize(size)
        final_image = np.array(final_image, "uint8")
        final_image = np.reshape(final_image, (1, final_image.shape[0], final_image.shape[1], final_image.shape[2]))
        lbl = recog.predict(final_image)
        print(lbl)

        font = cv2.FONT_HERSHEY_SIMPLEX
        mx = max(lbl[0][0], lbl[0][1], lbl[0][2])
        if mx == lbl[0][0]:
            label = labels[0]
        elif mx == lbl[0][1]:
            label = labels[1]
        else:
            label = labels[2]
            
        color = (255,255,255)
        stroke = 2
        cv2.putText(im,label, (x,y), font, 1, color, stroke, cv2.LINE_AA)

        color = (255,0,0) #BGR 0-255
        stroke = 2
        en_coord_x= x + w
        en_coord_y= y + h
        cv2.rectangle(im, (x, y), (en_coord_x, en_coord_y), color, stroke)
    cv2.imshow('im', im)    
    if cv2.waitKey(180) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()


