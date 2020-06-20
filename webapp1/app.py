#!/bin/sh
from flask import Flask, render_template, url_for, request, flash, redirect, session
import picamera, os, json, sys, signal, multiprocessing

def process():
    os.system("python3 /home/pi/Desktop/python_script.py")
    
    
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('pursure-mode') == 'Pursure-Mode':
            odMode = '0'
            
            text_file = open("odMode.txt", "w")
            n = text_file.write(odMode)
            text_file.close()
                    
        elif request.form.get('escape-mode') == 'Escape-Mode':
            odMode = '1'
            
            text_file = open("odMode.txt", "w")
            n = text_file.write(odMode)
            text_file.close()
            
        elif request.form.get('start') == 'Start':
            newProcess = multiprocessing.Process(target=process)
            newProcess.start()
            
        elif request.form.get('stop') == 'Stop':
            pid = open("pid.txt", "r").read()
            os.system("kill -9 {}".format(pid))
            
        elif request.form.get('pick color') == 'Pick Color':
            return redirect(url_for('pick_color'))
        
        else:
            pass
            
    elif request.method == 'GET':
        pass
        
    mode = open("odMode.txt", "r").read()
    if mode == '0':
        session['mode'] = 'Pursure-Mode'
    elif mode == '1':
        session['mode'] = 'Escape-Mode'
    else:
        session['mode'] = ''
        
    session['rgbColor'] = open("farbcode.txt", "r").read()
    
    return render_template('index.html', rgbColor = session['rgbColor'], mode = session['mode'])


@app.route('/pick_color', methods=['GET', 'POST'])
def pick_color():
    if request.method == 'POST':
        if request.form.get('refresh') == 'Refresh':
            os.remove("/home/pi/Desktop/webapp/static/image.jpg")

            with picamera.PiCamera() as camera:
                camera.resolution = (640, 480)
                camera.capture("/home/pi/Desktop/webapp/static/image.jpg")
                
        elif request.form.get('homepage') == 'Homepage':
            return redirect(url_for('index'))
        
        else:  
            rgbColorDict = request.get_json()
            rgbColor = json.dumps(rgbColorDict['pixelColor'])
            rgbColor = rgbColor.replace('"', '')
            
            text_file = open("farbcode.txt", "w")
            n = text_file.write(rgbColor)
            text_file.close()
    else:
        pass
    
    return render_template('pick_color.html')


if __name__ == '__main__':
    app.secret_key = ".."
    app.run(debug=True, host='0.0.0.0')
