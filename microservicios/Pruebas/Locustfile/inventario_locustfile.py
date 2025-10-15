from locust import HttpUser, task, between

class InventarioUser(HttpUser):
    wait_time = between(1, 3)  # Tiempo de espera entre peticiones (segundos)

    @task(1)
    def listar_productos(self):
        self.client.get("/products")

    @task(2)
    def crear_producto(self):
        producto = {
            "name": "Producto Test Locust",
            "price": 25.5,
            "quantity": 10
        }
        self.client.post("/products", json=producto)

    @task(1)
    def obtener_producto_individual(self):
        self.client.get("/products/101")  # ajusta según un ID real que exista

    @task(1)
    def verificar_salud(self):
        self.client.get("/health")
