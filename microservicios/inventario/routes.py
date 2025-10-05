# routes.py
from flask import Blueprint, request
from models import get_all_products, get_product, add_product, update_product, delete_product

routes = Blueprint('routes', __name__)

def init_routes(app, mysql):
    @routes.route('/productos', methods=['GET'])
    def listar_productos():
        return get_all_products(mysql)

    @routes.route('/productos/<int:id>', methods=['GET'])
    def obtener_producto(id):
        return get_product(mysql, id)

    @routes.route('/productos', methods=['POST'])
    def crear_producto():
        data = request.get_json()
        return add_product(mysql, data)

    @routes.route('/productos/<int:id>', methods=['PUT'])
    def editar_producto(id):
        data = request.get_json()
        return update_product(mysql, id, data)

    @routes.route('/productos/<int:id>', methods=['DELETE'])
    def eliminar_producto(id):
        return delete_product(mysql, id)

    app.register_blueprint(routes)
