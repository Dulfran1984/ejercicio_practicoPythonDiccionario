from flask import Flask, render_template, request
from datetime import datetime
import os
app = Flask(__name__)
datos = []
registro = 0
@app.route('/', methods=['GET', 'POST'])
def formulario():
    mensaje = ""
    if request.method == 'POST':
        # Aquí procesas los datos del formulario
        nombre = request.form['nombre']
        contacto = request.form['contacto']
        correo = request.form['correo']
        direccion = request.form['direccion']
        _archivo = request.files['txtImagen']
        # Validar si se proporcionó algún dato
        mensaje = "Formulario enviado correctamente"
        tiempo = datetime.now()
        hora_Actual = tiempo.strftime('%Y%M%H%M%S')
        if _archivo.filename!="":
            nombre_Archivo = hora_Actual + "_" +_archivo.filename
            _archivo.save('templates/img/'+nombre_Archivo)
        datos.append({'Registro': (registro + 1),'Nombre': nombre, 'Contacto': contacto, 'Correo': correo, 'Direccion': direccion,'Imagen':nombre_Archivo})
    return render_template('formulario.html', mensaje=mensaje)
@app.route('/mostrar')
def fnt_mostrar():
    return render_template('mostrar.html', datos = datos)

if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1', port=5000)
