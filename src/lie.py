import numpy as np
import cv2
import pickle
import tensorflow as tf
from PIL import Image
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
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

class DeceptionDetectionVoice(QThread):
  LieVoiceResult = pyqtSignal(list)
  def mp3tomfcc(self, 
                file_path, max_pad):
    audio, sample_rate = librosa.core.load(file_path)
    mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=20)
    pad_width = max_pad - mfcc.shape[1]
    if (pad_width > 0):
      mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
    else:
      mfcc = mfcc[:,0:max_pad]
    return mfcc

  def run(self):
    self.ThreadActive = True
    if self.ThreadActive:
      freq = 44100  # Sampling frequency
      duration = 28 #change or handle seconds 

      with open('LR_model.pkl', 'rb') as f:
          lr = pickle.load(f)
        
      # Start recorder with the given values 
      # of duration and sample frequency
      recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
        
      # Record audio for the given number of seconds
      sd.wait()
        
      # This will convert the NumPy array to an audio
      # file with the given sampling frequency
      sound = write("recording0.wav", freq, recording)
        
      # Convert the NumPy array to audio file
      audioFile = wv.write("recording1.wav", recording, freq, sampwidth=2)

      mfccs = []
      BASE_DIR = os.path.dirname(os.path.abspath(__file__))
      mfccs.append(self.mp3tomfcc(BASE_DIR + '/recording1.wav', 1000)) 
      mfccs = np.asarray(mfccs)

      nsamples, nx, ny = mfccs.shape
      X_final = mfccs.reshape((nsamples,nx*ny))

      pred = lr.predict_proba(X_final) # predict_proba bu probları veriyomuş [truth, lie]
      prede = lr.predict(X_final)
      print(pred)
      print(prede)
      predAndPerc = [pred, prede]
      self.LieVoiceResult.emit(predAndPerc)
      """
      if pred == 0: # 0 truth 1 lie
          print("Not LIE")
      else:
          print("LIE")
      """
    def stop(self):
      self.ThreadActive = False
      self.quit()              