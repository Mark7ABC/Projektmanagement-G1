from flask import Flask, render_template, url_for, request, flash
import picamera, os, json

def picture():
    os.remove("/home/pi/Desktop/webapp/static/image.jpg")

    with picamera.PiCamera() as camera:
            camera.resolution = (640, 640)
            camera.capture("/home/pi/Desktop/webapp/static/image.jpg")
            
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('refresh') == 'Refresh':
            picture()
            
        elif request.form.get('fangmodus') == 'Fangmodus':
            odMode = '0'
            
            text_file = open("odMode.txt", "a")
            n = text_file.write(odMode)
            text_file.close()
                    
        elif request.form.get('fluchtmodus') == 'Fluchtmodus':
            odMode = '1'
            
            text_file = open("odMode.txt", "w")
            n = text_file.write(odMode)
            text_file.close()
            
        else:  
            rgbColorDict = request.get_json()
            rgbColor = json.dumps(rgbColorDict['pixelColor'])
            rgbColor = rgbColor.replace('"', '')
            
            text_file = open("farbcode.txt", "w")
            n = text_file.write(rgbColor)
            text_file.close()
            
    elif request.method == 'GET':
        pass
    
    return render_template('index.html')   

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
