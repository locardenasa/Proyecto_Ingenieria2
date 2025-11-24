from locust import HttpUser, task, between
import random

class TransactionUser(HttpUser):
    wait_time = between(1, 3)  # tiempo de espera entre peticiones (segundos)
    base_url = "/api/transacciones"

    @task(2)
    def listar_transacciones(self):
        self.client.get(self.base_url)

    @task(3)
    def crear_transaccion(self):
        payload = {
            "descripcion": f"Compra número {random.randint(100, 999)}",
            "monto": random.uniform(10.0, 500.0),
            "tipo": random.choice(["ingreso", "egreso"])
        }
        response = self.client.post(self.base_url, json=payload)
        if response.status_code != 201:
            print(f"Error al crear transacción: {response.status_code} -> {response.text}")
        else:
            transaction_id = response.json().get("id")
            if transaction_id:
                self.last_id = transaction_id

    @task(2)
    def ver_transaccion(self):
        if hasattr(self, "last_id"):
            self.client.get(f"{self.base_url}/{self.last_id}")

    @task(1)
    def actualizar_transaccion(self):
        if hasattr(self, "last_id"):
            payload = {
                "descripcion": "Actualización desde Locust",
                "monto": random.uniform(100.0, 600.0)
            }
            self.client.put(f"{self.base_url}/{self.last_id}", json=payload)

    @task(1)
    def eliminar_transaccion(self):
        if hasattr(self, "last_id"):
            self.client.delete(f"{self.base_url}/{self.last_id}")
            del self.last_id  # eliminar el id después de borrar
