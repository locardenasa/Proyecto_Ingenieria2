from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'      # tu usuario Laragon
app.config['MYSQL_PASSWORD'] = ''      # tu contraseña Laragon
app.config['MYSQL_DB'] = 'notificaciones_db'

mysql = MySQL(app)

# Crear tabla automáticamente
def crear_tabla():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS notificaciones (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario VARCHAR(100),
            mensaje TEXT,
            tipo VARCHAR(50),
            fecha DATETIME
        )
        """)
        mysql.connection.commit()
        cur.close()

crear_tabla()

# Endpoints
@app.route('/notificaciones', methods=['GET'])
def listar_notificaciones():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, usuario, mensaje, tipo, fecha FROM notificaciones")
    resultados = cur.fetchall()
    cur.close()
    notis = []
    for n in resultados:
        notis.append({
            'id': n[0],
            'usuario': n[1],
            'mensaje': n[2],
            'tipo': n[3],
            'fecha': n[4].strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(notis)

@app.route('/notificaciones', methods=['POST'])
def crear_notificacion():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO notificaciones (usuario, mensaje, tipo, fecha) VALUES (%s, %s, %s, NOW())",
        (data['usuario'], data['mensaje'], data['tipo'])
    )
    mysql.connection.commit()
    cur.close()
    return jsonify({'mensaje': 'Notificación creada'}), 201

if __name__ == "__main__":
    app.run(debug=True, port=5003)

