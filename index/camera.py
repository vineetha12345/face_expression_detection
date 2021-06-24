import cv2,os,urllib.request
from django.conf import settings
from index.model import FacialExpressionModel
import numpy as np
facec = cv2.CascadeClassifier("./index/haarcascade_frontalface_default.xml")
model = FacialExpressionModel("./index/model.json", "./index/model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()
    def get_frame(self):
        ret,frame = self.video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facec.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            fc = gray[y:y+h, x:x+w]
            font=2
            roi = cv2.resize(fc, (48, 48))
            pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])
            cv2.putText(frame, pred, (x, y), font, 1, (255, 255, 0), 2)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.imshow('Video',frame)
            if cv2.waitKey(1) & 0xFF==ord('q'):
                break
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
def gen(camera):
    while True:
        frame=camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n\r\n')
