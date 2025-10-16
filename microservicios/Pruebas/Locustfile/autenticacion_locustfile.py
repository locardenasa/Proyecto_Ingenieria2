from locust import HttpUser, task, between
import random
import string

# Genera correos y contraseñas aleatorios para crear usuarios de prueba
def random_email():
    return "user_" + "".join(random.choices(string.ascii_lowercase, k=6)) + "@test.com"

def random_password():
    return "".join(random.choices(string.ascii_letters + string.digits, k=8))


class LaravelAuthUser(HttpUser):
    wait_time = between(1, 3)  # segundos entre tareas

    def on_start(self):
        """Se ejecuta cuando inicia el test: crea y loguea un usuario"""
        self.email = random_email()
        self.password = random_password()

        # Crear usuario
        create_payload = {
            "name": "Usuario Test",
            "email": self.email,
            "password": self.password
        }
        with self.client.post("/api/create_user", json=create_payload, catch_response=True) as response:
            if response.status_code != 201:
                response.failure(f"Error al crear usuario: {response.text}")

        # Login para obtener token
        login_payload = {
            "email": self.email,
            "password": self.password
        }
        with self.client.post("/api/login", json=login_payload, catch_response=True) as response:
            if response.status_code == 200:
                self.token = response.json().get("access_token")
            else:
                response.failure("Error al iniciar sesión")

    @task(3)
    def change_password(self):
        """Cambia la contraseña del usuario logueado"""
        headers = {"Authorization": f"Bearer {self.token}"}
        payload = {
            "current_password": self.password,
            "new_password": random_password()
        }
        with self.client.post("/api/change_password", headers=headers, json=payload, catch_response=True) as response:
            if response.status_code != 200:
                response.failure("Error al cambiar contraseña")

    @task(1)
    def logout(self):
        """Cerrar sesión"""
        headers = {"Authorization": f"Bearer {self.token}"}
        with self.client.post("/api/logout", headers=headers, catch_response=True) as response:
            if response.status_code != 200:
                response.failure("Error al cerrar sesión")