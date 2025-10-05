from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)

# --- Crear tabla automáticamente dentro del contexto de la app ---
with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            descripcion TEXT,
            cantidad INT NOT NULL,
            precio DECIMAL(10,2),
            fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)
    mysql.connection.commit()
    cur.close()

# --- Endpoints ---
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"mensaje": "Microservicio Flask activo y tabla creada automáticamente"}), 200

@app.route('/productos', methods=['GET'])
def obtener_productos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos")
    datos = cur.fetchall()
    cur.close()

    productos = []
    for fila in datos:
        productos.append({
            "id": fila[0],
            "nombre": fila[1],
            "descripcion": fila[2],
            "cantidad": fila[3],
            "precio": float(fila[4]),
            "fecha_actualizacion": str(fila[5])
        })
    return jsonify(productos)

@app.route('/productos', methods=['POST'])
def agregar_producto():
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO productos (nombre, descripcion, cantidad, precio) VALUES (%s, %s, %s, %s)",
        (data['nombre'], data.get('descripcion', ''), data['cantidad'], data['precio'])
    )
    mysql.connection.commit()
    cur.close()
    return jsonify({"mensaje": "Producto agregado exitosamente"}), 201

@app.route('/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE productos
        SET nombre=%s, descripcion=%s, cantidad=%s, precio=%s
        WHERE id=%s
    """, (data['nombre'], data.get('descripcion', ''), data['cantidad'], data['precio'], id))
    mysql.connection.commit()
    cur.close()
    return jsonify({"mensaje": "Producto actualizado correctamente"}), 200

@app.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM productos WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({"mensaje": "Producto eliminado correctamente"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)
