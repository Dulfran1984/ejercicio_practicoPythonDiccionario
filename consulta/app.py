from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Función para conectarse a la base de datos SQLite
def conectar_db():
    conn = sqlite3.connect('datos.s3db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def formulario():
    return render_template('formulario.html')

@app.route('/obtener_usuario', methods=['POST'])
def obtener_usuario():
    documento = request.json['documento']

    # Conexión a la base de datos
    conn = conectar_db()
    cursor = conn.cursor()

    # Buscar información en la base de datos
    cursor.execute("SELECT * FROM usuarios WHERE documento = ?", (documento,))
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        usuario_dict = {key: usuario[key] for key in usuario.keys()}
        return jsonify(usuario_dict)
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404
@app.route('/material')
def material():
    return render_template('material.html')
if __name__ == '__main__':
    app.run(debug=True)
