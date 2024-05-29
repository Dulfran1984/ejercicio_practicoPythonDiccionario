import cv2.data
from flask import Flask, render_template, request,send_from_directory
from datetime import datetime
from rembg import remove
from PIL import Image
import sqlite3
import cv2
import os
from flask import Response

app = Flask(__name__)
camera = cv2.VideoCapture(0)
def gen_frames():
    while True:
        success, frame = camera.read()  # Leer la cámara
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#registro = 0
@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/', methods=['GET', 'POST'])
def formulario():
    global registro
    mensaje = ""
    if request.method == 'POST':
        # Aquí procesas los datos del formulario
        nombre = request.form['nombre']
        contacto = request.form['contacto']
        correo = request.form['correo']
        direccion = request.form['direccion']
        _archivo = request.files['txtImagen']
        
        # Validar si se proporcionó algún dato
        mensaje = f"La persona {nombre} ha sido registrada con éxito"
        tiempo = datetime.now()
        hora_Actual = tiempo.strftime('%Y%M%H%M%S')
        if _archivo.filename!="":
            nombre_Archivo = hora_Actual + "_" +_archivo.filename
            _archivo.save('static/img/'+nombre_Archivo)
            filepath = 'static/img/'+nombre_Archivo
            image = Image.open(filepath)
            image = image.resize((100, 100))  # Redimensionar a 500x500 píxeles
            image.save(filepath)
            guardarDB(nombre, contacto,correo,direccion,nombre_Archivo)
            
        #datos.append({'Registro': (registro + 1),'Nombre': nombre, 'Contacto': contacto, 'Correo': correo, 'Direccion': direccion,'Imagen':nombre_Archivo})
        #registro+=1
        
    return render_template('formulario.html', mensaje=mensaje)
@app.route("/conferencia")
def index():
    return render_template("conferencia.html")
@app.route('/guardar')
def guardarDB(nombre, contacto, correo, direccion,archivo):
    conn = sqlite3.connect('static/datos.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS datos (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, contacto TEXT, correo TEXT, direccion TEXT, imagen TEXT)")
    cursor.execute("INSERT INTO datos (nombre, contacto, correo, direccion, imagen) VALUES (?,?,?,?,?)", (nombre, contacto, correo, direccion, archivo))
    conn.commit()
    conn.close()
    return render_template('formulario.html', mensaje="Los datos han sido guardados en la base de datos con éxito")

@app.route('/video/<path:filename>')
def video(filename):
    return send_from_directory('videos', filename)
@app.route('/mostrar')
def fnt_mostrar():
    conexion = sqlite3.connect('static/datos.db ')
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM datos")
    datos = cursor.fetchall()
    conexion.close()
    return render_template('mostrar.html', datos = datos)
    print(datos)
@app.route('/reproducir')
def reproducir():
    return render_template('videos.html')
@app.route('/reportes')
def reporte():
    return render_template('reportes.html')
if __name__ == '__main__':
    app.run(debug=True,host='172.22.50.17', port=5000)
    #app.run(debug=True,host='172.22.50.17', port=5000)