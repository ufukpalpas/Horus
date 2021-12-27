import os
import numpy as np
import cv2
from PIL import Image
import pickle
import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop,SGD,Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR,"images")

x_test = []
y_test = []
x_test = np.array(x_test)
y_test = np.array(y_test)

for root,dirs, files in os.walk(image_dir):
    for file in files:
        path = os.path.join(root,file)
        label = os.path.basename(os.path.dirname(path)).replace(" ", "-").lower()
        pil_image = Image.open(path)
        final_image = np.array(pil_image, "uint8")
        x_test = np.append(x_test, final_image)
        y_test = np.append(y_test, label)
        print(label)


x_test = np.reshape(x_test, (95+95+95, 250, 250, 3))

recog = tf.keras.models.load_model("model")
lbl = recog.predict(x_test)
labels = ["positive", "neutral", "negative"]
trueCount = 0

for i in range(285):
    mx = max(lbl[i][0], lbl[i][1], lbl[i][2])
    if mx == lbl[i][0]:
        label = labels[0]
    elif mx == lbl[i][1]:
        label = labels[1]
    else:
        label = labels[2]

    if label == y_test[i]:
        trueCount += 1    
print("285 images tested")
print("True guesses: ", trueCount)
print ("Percentage: ", trueCount*100/285)
