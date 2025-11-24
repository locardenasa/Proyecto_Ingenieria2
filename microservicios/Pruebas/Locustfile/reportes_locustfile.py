from locust import HttpUser, task, between

class ReportesUser(HttpUser):
    wait_time = between(1, 3)  # tiempo aleatorio entre peticiones

    @task(2)
    def reporte_json(self):
        """Probar el reporte en formato JSON"""
        self.client.get("/reporte/productos?formato=json", name="/reporte/json")

    @task(2)
    def reporte_excel(self):
        """Probar el reporte en formato Excel"""
        self.client.get("/reporte/productos?formato=excel", name="/reporte/excel")

    @task(2)
    def reporte_pdf(self):
        """Probar el reporte en formato PDF"""
        self.client.get("/reporte/productos?formato=pdf", name="/reporte/pdf")

    @task(1)
    def reporte_con_filtro(self):
        """Probar con filtro por nombre"""
        self.client.get("/reporte/productos?formato=json&nombre=camisa", name="/reporte/json?nombre")

