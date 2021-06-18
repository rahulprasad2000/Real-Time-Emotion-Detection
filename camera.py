import cv2
from model import MyFaceExpressionModel
import numpy as np
from keras.preprocessing.image import img_to_array

face = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
model = MyFaceExpressionModel("model.json", "model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    # returns camera frames along with bounding boxes and predictions
    def get_frame(self):
        _, frame = self.video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi_gray=gray[y:y+h,x:x+w]
            roi=cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)
            pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])
             

            cv2.putText(frame,pred,(x,y),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()