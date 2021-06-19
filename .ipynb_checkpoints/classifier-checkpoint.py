{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "3e9701c2",
   "metadata": {},
   "outputs": [],
   "source": [
    "from keras.preprocessing import image as im\n",
    "\n",
    "import cv2\n",
    "import json\n",
    "import numpy as np\n",
    "\n",
    "def classify(frame, face_detector, model):\n",
    "\n",
    "    # Emotions\n",
    "    emotions = ('Angry', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral')\n",
    "\n",
    "    gray = frame\n",
    "\n",
    "    # Detect faces\n",
    "    detected_faces = face_detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)\n",
    "\n",
    "    # Face properties\n",
    "    face_prop = []\n",
    "\n",
    "    # Faces are detected more than 0 i.e not 0\n",
    "    if len(detected_faces) > 0:\n",
    "        # x,y = x,y coordinates\n",
    "        # w,h = width, height\n",
    "        for (x, y, w, h) in detected_faces:\n",
    "            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)\n",
    "            img = cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)\n",
    "\n",
    "            adjust_img = img[y:y+h, x:x+w]  # Crop img to the face\n",
    "            adjust_img = cv2.resize(adjust_img, (48, 48))  # Resize img to fit the ML model\n",
    "\n",
    "            img_tensor = im.img_to_array(adjust_img)\n",
    "            img_tensor = np.expand_dims(img_tensor, axis=0)\n",
    "\n",
    "            img_tensor /= 255  # pixels are in scale of [0, 255]. normalize all pixels in scale of [0, 1]\n",
    "\n",
    "            predictions = model.predict(img_tensor)  # store probabilities of 2 facial expressions\n",
    "            label = emotions[np.argmax(predictions)]  # Get label with most probability\n",
    "\n",
    "            confidence = np.max(predictions)  # Get the confidence of that label\n",
    "\n",
    "            confidence *= 100 # Multiple probability by 100\n",
    "\n",
    "            detect = dict()\n",
    "            detect['label'] = label\n",
    "            detect['score'] = str(confidence).split(\".\")[0]\n",
    "            detect['x'] = str(x)\n",
    "            detect['y'] = str(y)\n",
    "            detect['width'] = str(w)\n",
    "            detect['height'] = str(h)\n",
    "\n",
    "            face_prop.append(detect)\n",
    "            print(face_prop)\n",
    "            \n",
    "            cv2.putText(frame, label + \" : \" + str(confidence), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)\n",
    "        \n",
    "    cv2.imwrite(\"somefile.jpeg\", frame)\n",
    "\n",
    "    # output_json = json.dumps([face.__dict__ for face in face_prop])\n",
    "    return face_prop"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ea6c2243",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}