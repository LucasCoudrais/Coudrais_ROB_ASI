#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)

def generate_frames():
    video_path = "../tiny_darknet/voitures.mp4"  # Spécifiez le chemin vers votre vidéo

    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)