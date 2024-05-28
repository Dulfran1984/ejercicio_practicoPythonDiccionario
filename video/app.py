from flask import Flask, render_template,request,flash,redirect,url_for
from datetime import datetime
from PIL import Image
import sqlite3
app = Flask(__name__)
app.secret_key = 'clave_secreta'  # Clave secreta requerida para usar la función flash
'''@app.route('/')
def index():
    return render_template('video.html')'''
def get_db_connection():
    conn = sqlite3.connect('static/dbs_control.s3db')
    conn.row_factory = sqlite3.Row  # Permite el acceso a las columnas por nombre
    return conn
@app.route('/')
def index():
    return render_template('formulario.html')
@app.route('/submit', methods=['GET', 'POST'])
def formulario():
    mensaje = ""
    if request.method == 'POST':
        # Aquí procesas los datos del formulario
        nombre = request.form['nombres']
        identificacion = request.form['identificacion']
        tarjeta = request.form['tarjeta']
        contacto = request.form['contacto']
        _archivo = request.files['imagen']
        perfil = request.form['perfil']
        
        # Validar si se proporcionó algún dato
        mensaje = f"La persona {nombre} ha sido registrada con éxito"
        tiempo = datetime.now()
        hora_Actual = tiempo.strftime('%Y%M%H%M%S')
        if _archivo.filename!="":
            nombre_Archivo = hora_Actual + "_" +_archivo.filename
            _archivo.save('static/img/'+nombre_Archivo)
            filepath = 'static/img/'+nombre_Archivo
            image = Image.open(filepath)
            image = image.resize((400, 400))  # Redimensionar a 500x500 píxeles
            image.save(filepath)
            conn = get_db_connection()
            conn.execute('INSERT INTO tbl_personas (id, nombres, contacto, perfil, imagen,tarjeta) VALUES (?, ?, ?, ?, ?,?)', (identificacion, nombre.upper(), contacto, perfil.upper(), nombre_Archivo,tarjeta))
            conn.commit()
            conn.close()
            #flash('¡El usuario se ha registrado correctamente!', 'success')  # Mensaje de éxito
            return redirect(url_for('index'))
@app.route('/control')
def control():
    render_template('control.html')
'''@app.route('/editar/<int:user_id>', methods=['GET', 'POST'])
def editar(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tbl_personas WHERE id = ?', (user_id))
    user = cursor.fetchone()
    conn.close()

    if request.method == 'POST':
        # Procesar el formulario de edición aquí
        return redirect(url_for('index'))

    return render_template('control.html', user=user)'''
if __name__ == '__main__':
    app.run(debug=True)