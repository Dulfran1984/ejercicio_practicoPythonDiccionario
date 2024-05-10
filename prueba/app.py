from flask import Flask, render_template, request

app = Flask(__name__)
datos = []

@app.route('/', methods=['GET', 'POST'])
def formulario():
    mensaje = ""
    if request.method == 'POST':
        # Aquí procesas los datos del formulario
        nombre = request.form['nombre']
        contacto = request.form['contacto']
        correo = request.form['correo']
        direccion = request.form['direccion']
        datos.append({'Nombre': nombre, 'Contacto': contacto, 'Correo': correo, 'Direccion': direccion})
        # Validar si se proporcionó algún dato
        mensaje = "Formulario enviado correctamente"
    
    return render_template('formulario.html', mensaje=mensaje)
@app.route('/mostrar')
def fnt_mostrar():
    return render_template('mostrar.html', datos = datos)

if __name__ == '__main__':
    app.run(debug=True)
