from flask import Flask, render_template, request, jsonify, url_for, redirect, flash, Response, send_file
from camera import VideoCamera
import os 
from flask import send_from_directory 
import cv2    


app = Flask(__name__)


@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')



@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame) + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
           mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host=os.getenv('HOST', '127.0.0.1'), port=os.getenv('PORT', 5000), debug=app.config.get('FLASK_DEBUG'))
   
    
    