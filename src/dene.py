import numpy as np
import cv2
import glob
from mss import mss
from PIL import Image
import time

color = (0, 255, 0) # bounding box color.

# This defines the area on the screen.
sct = mss()
mon = sct.monitors[0]

previous_time = 0
while True :
    sct_img = sct.grab(mon)
    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
    img = np.array(img)
    print("s: ", img.shape)
    cv2.imshow('screen', img)
    if cv2.waitKey ( 1 ) & 0xff == ord( 'q' ) :
        cv2.destroyAllWindows()
    txt1 = 'fps: %.1f' % ( 1./( time.time() - previous_time ))
    previous_time = time.time()
    print(txt1)