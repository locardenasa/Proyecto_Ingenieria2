from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Conexión a MongoDB con la base de datos inventario_db
client = MongoClient(os.getenv('MONGO_URI'))
db = client.inventario_db
products_collection = db['products']
counters_collection = db['counters']

# Inicializar contador si no existe
if counters_collection.find_one({'_id': 'product_id'}) is None:
    counters_collection.insert_one({'_id': 'product_id', 'seq': 100})

# Función para obtener el siguiente ID numérico
def get_next_product_id():
    counter = counters_collection.find_one_and_update(
        {'_id': 'product_id'},
        {'$inc': {'seq': 1}},
        return_document=True
    )
    return counter['seq']

# Función para imprimir mensajes con timestamp
def log_message(action, details):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {action}: {details}")

# Rutas CRUD para productos
@app.route('/products', methods=['GET'])
def get_products():
    log_message("CONSULTA", "Obteniendo lista de todos los productos")
    products = list(products_collection.find())
    response_data = {
        'message': 'Productos obtenidos exitosamente',
        'count': len(products),
        'data': products
    }
    log_message("CONSULTA_EXITOSA", f"Se encontraron {len(products)} productos")
    return jsonify(response_data)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    log_message("CONSULTA_INDIVIDUAL", f"Buscando producto con ID: {product_id}")
    product = products_collection.find_one({'id': product_id})
    if product:
        log_message("ENCONTRADO", f"Producto '{product.get('name', 'Sin nombre')}' encontrado")
        return jsonify({
            'message': 'Producto encontrado exitosamente',
            'data': product
        })
    else:
        log_message("NO_ENCONTRADO", f"Producto con ID {product_id} no existe")
        return jsonify({'message': 'Producto no encontrado'}), 404

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    log_message("CREACIÓN", f"Intentando crear nuevo producto: {data}")
    
    # Validar datos requeridos
    if not data.get('name'):
        log_message("ERROR_VALIDACIÓN", "Falta el nombre del producto")
        return jsonify({'message': 'El campo "name" es requerido'}), 400
    
    # Generar ID numérico corto
    product_id = get_next_product_id()
    data['id'] = product_id
    
    result = products_collection.insert_one(data)
    
    log_message("CREACIÓN_EXITOSA", f"Producto creado con ID: {product_id}")
    return jsonify({
        'message': 'Producto creado exitosamente',
        'data': {'id': product_id}
    }), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    log_message("ACTUALIZACIÓN", f"Actualizando producto {product_id} con datos: {data}")
    
    result = products_collection.update_one({'id': product_id}, {'$set': data})
    if result.modified_count > 0:
        log_message("ACTUALIZACIÓN_EXITOSA", f"Producto {product_id} actualizado correctamente")
        return jsonify({
            'message': 'Producto actualizado exitosamente',
            'modified_count': result.modified_count
        })
    else:
        log_message("ACTUALIZACIÓN_FALLIDA", f"Producto {product_id} no encontrado para actualizar")
        return jsonify({'message': 'Producto no encontrado'}), 404

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    log_message("ELIMINACIÓN", f"Intentando eliminar producto {product_id}")
    
    # Primero obtener el producto para mostrar info en el log
    product = products_collection.find_one({'id': product_id})
    
    result = products_collection.delete_one({'id': product_id})
    if result.deleted_count > 0:
        product_name = product.get('name', 'Sin nombre') if product else 'Desconocido'
        log_message("ELIMINACIÓN_EXITOSA", f"Producto '{product_name}' (ID: {product_id}) eliminado permanentemente")
        return jsonify({
            'message': f'Producto "{product_name}" eliminado exitosamente',
            'deleted_count': result.deleted_count
        })
    else:
        log_message("ELIMINACIÓN_FALLIDA", f"Producto {product_id} no encontrado para eliminar")
        return jsonify({'message': 'Producto no encontrado'}), 404

@app.route('/health', methods=['GET'])
def health_check():
    log_message("HEALTH_CHECK", "Verificación de estado del servidor")
    return jsonify({
        'status': 'healthy',
        'message': 'Servidor Flask funcionando correctamente',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    log_message("INICIO", "Servidor Flask iniciado en http://localhost:5000")
    log_message("INICIO", "Base de datos: MongoDB - inventario_db")
    log_message("INICIO", "IDs numéricos: 100-999 (3 dígitos)")
    log_message("INICIO", "Servidor listo para recibir peticiones")
    app.run(debug=True, port=5000)