from locust import HttpUser, task, between

class NotificationUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_health(self):
        self.client.get("/health")

    @task
    def send_email(self):
        payload = {
            "to": "sebastianworks21@gmail.com",
            "subject": "Prueba de Carga",
            "body": "Este es un correo de prueba enviado por Locust"
        }
        self.client.post("/notify", json=payload)
