
from flask import jsonify

def get_all_products(mysql):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM productos")
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)

def get_product(mysql, id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
    data = cursor.fetchone()
    cursor.close()
    return jsonify(data)

def add_product(mysql, data):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, descripcion, cantidad, precio) VALUES (%s, %s, %s, %s)",
        (data['nombre'], data['descripcion'], data['cantidad'], data['precio'])
    )
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Producto agregado con éxito'})

def update_product(mysql, id, data):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "UPDATE productos SET nombre=%s, descripcion=%s, cantidad=%s, precio=%s WHERE id=%s",
        (data['nombre'], data['descripcion'], data['cantidad'], data['precio'], id)
    )
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Producto actualizado correctamente'})

def delete_product(mysql, id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Producto eliminado'})