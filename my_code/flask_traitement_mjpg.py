#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, Response, render_template, jsonify
import cv2
from PIL import Image
import numpy as np
import time
import json


app = Flask(__name__)
        
def generate_frames_filtered():
    video_path = "http://127.0.0.1:5000/video_feed"  # Spécifiez le lien vers votre flux MJPEG
    # video_path = "../tiny_darknet/voitures.mp4"  # Spécifiez le lien vers votre flux MJPEG

    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        updated_sensor = {"id": 1, "name": "Traitement image", "time": str(time.time())}
        sensors = read_sensors()

        for sensor in sensors:
            if sensor['id'] == 1:
                sensor.update(updated_sensor)
                write_sensors(sensors)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertir le format d'image BGR en RGB
        
        frame = cv2.Canny(frame, 30, 150)

        img_pil = Image.fromarray(frame)
        img_pil.thumbnail((640, 480))  # Redimensionner l'image si nécessaire

        frame = np.array(img_pil)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        

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
    return render_template('index_traitement.html')

@app.route('/video_feed_filtered')
def video_feed_filtered():
    return Response(generate_frames_filtered(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/traitement_infos', methods=['GET'])
def get_traitement_infos():
    sensors = read_sensors()
    return jsonify(sensors)


def read_sensors():
    with open('data/traitement.json', 'r') as file:
        sensors = json.load(file)
    return sensors

def write_sensors(sensors):
    with open('data/traitement.json', 'w') as file:
        json.dump(sensors, file)

if __name__ == '__main__':
    app.run(host="localhost", port=5001, debug=True)