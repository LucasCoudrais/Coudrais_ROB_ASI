#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import curses
import cv2
import numpy as np

def make_request(stdscr):
    urlSensors = "http://127.0.0.1:5000/traitement_infos"

    # Configuration de la fenêtre curses
    curses.curs_set(0)  # Masquer le curseur
    stdscr.nodelay(1)  # Mode non bloquant pour la lecture de l'entrée

    # Boucle principale
    while True:
        stdscr.clear()  # Effacer l'écran

        # Effectuer la requête HTTP
        responseSensors = requests.get(urlSensors)
        dataSensors = responseSensors.json()
        
        
        # Afficher les résultats dans l'interface curses
        height, width = stdscr.getmaxyx()
        y = 1

        for item in dataSensors:
            name = item['name']
            time = item['time']
            output = str(name) + " : "+ str(time)
            stdscr.addstr(y, 0, output)
            y += 1
            

        stdscr.refresh()  # Rafraîchir l'écran

        # Lire l'entrée utilisateur
        key = stdscr.getch()
        if key == ord('q'):
            break

# Appel de la fonction principale avec curses
curses.wrapper(make_request)