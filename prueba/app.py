from flask import Flask, render_template, request
from datetime import datetime
from rembg import remove
from PIL import Image
import os
app = Flask(__name__)
datos = []
registro = 0
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
            
        datos.append({'Registro': (registro + 1),'Nombre': nombre, 'Contacto': contacto, 'Correo': correo, 'Direccion': direccion,'Imagen':nombre_Archivo})
        registro+=1
        
    return render_template('formulario.html', mensaje=mensaje)
@app.route('/mostrar')
def fnt_mostrar():
    return render_template('mostrar.html', datos = datos)

if __name__ == '__main__':
    #app.run(debug=True,host='127.0.0.1', port=5000)
    app.run(debug=True,host='172.22.50.17', port=5000)