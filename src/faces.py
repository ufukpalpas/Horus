import numpy as np
import cv2
import pickle
import tensorflow as tf
from PIL import Image
import screeninfo

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt.xml')
face_cascade2 = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
face_cascade_tree = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt_tree.xml')
profile_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_profileface.xml')
isRect = False

recog = tf.keras.models.load_model("model")

'''recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner.yml")

labels={"person_name": 1}
with open("labels.pickle", 'rb') as f:
   og_labels = pickle.load(f)
   labels = {v:k for k,v in og_labels.items()}'''

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    profile = profile_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    faces2 = face_cascade2.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    facestr = face_cascade_tree.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

    for(x,y,w,h) in faces:
        #print(x,y,w,h)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        size = (250, 250)
        image_array = np.array(roi_color, "uint8")
        pil_image = Image.fromarray(image_array)  
        #final_image = pil_image.resize(size, Image.ANTIALIAS)
        final_image = pil_image.resize(size)
        final_image = np.array(final_image, "uint8")
        final_image = np.reshape(final_image, (1, final_image.shape[0], final_image.shape[1], final_image.shape[2]))
        #print(final_image.shape)
        lbl = recog.predict(final_image)
        print(lbl)

        labels = ["positive", "neutral", "negative"]
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
        cv2.putText(frame,label, (x,y), font, 1, color, stroke, cv2.LINE_AA)
        #img_item = "7.png"
        #cv2.imwrite(img_item, roi_gray)

        color = (255,0,0) #BGR 0-255
        stroke = 2
        en_coord_x= x + w
        en_coord_y= y + h
        cv2.rectangle(frame, (x, y), (en_coord_x, en_coord_y), color, stroke)
    
    '''for(x,y,w,h) in profile:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        img_item = "7.png"
        cv2.imwrite(img_item, roi_gray)
        color = (255,0,0) #BGR 0-255
        stroke = 2
        en_coord_x= x + w
        en_coord_y= y + h
        cv2.rectangle(frame, (x, y), (en_coord_x, en_coord_y), color, stroke)
        
    for(x,y,w,h) in faces2:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        img_item = "7.png"
        cv2.imwrite(img_item, roi_gray)
        color = (255,0,0) #BGR 0-255
        stroke = 2
        en_coord_x= x + w
        en_coord_y= y + h
        cv2.rectangle(frame, (x, y), (en_coord_x, en_coord_y), color, stroke)

    facestr = face_cascade_tree.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    for(x,y,w,h) in facestr:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        img_item = "7.png"
        cv2.imwrite(img_item, roi_gray)
        color = (255,0,0) #BGR 0-255
        stroke = 2
        en_coord_x= x + w
        en_coord_y= y + h
        cv2.rectangle(frame, (x, y), (en_coord_x, en_coord_y), color, stroke)'''
    
    screen = screeninfo.get_monitors()[0]
    width, height = screen.width, screen.height
    cv2.namedWindow('frame', cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow('frame', screen.x - 1, screen.y - 1)
    cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()