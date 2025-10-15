# 🧾 Microservicio de Inventario

Microservicio en **Flask** que gestiona productos de inventario, conectado a **MongoDB Nombre: inventario_db**.  
Permite crear, consultar, actualizar y eliminar productos mediante una API REST.

---

##  Comandos básicos

# Crear entorno e instalar dependencias
pip install flask pymongo python-dotenv

# Ejecutar el microservicio
python app.py


# Variables principales
Variable	Descripción
id	ID numérico autogenerado del producto
name	Nombre del producto
description	Descripción del producto
price	Precio del producto
quantity	Cantidad disponible

# Endpoints principales
Método	Ruta	Descripción
GET	/products	Obtener todos los productos
GET	/products/<id>	Obtener un producto por ID
POST	/products	Crear un nuevo producto
PUT	/products/<id>	Actualizar un producto existente
DELETE	/products/<id>	Eliminar un producto

# Pruebas con Locust

# Instalar locust
pip install locust

# Ejecutar pruebas con 2 o 15 usuarios
locust -f inventario_locustfile.py