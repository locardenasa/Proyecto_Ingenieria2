FROM python:3.11-slim
WORKDIR /app

# dependencias del SO necesarias
RUN apt-get update && apt-get install -y build-essential netcat && rm -rf /var/lib/apt/lists/*

# copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copiar código
COPY . .

# crear carpeta de logs y darle permisos
RUN mkdir -p /var/log/auditoria && chown -R www-data:www-data /var/log/auditoria

EXPOSE 5000

# usar gunicorn en producción (puedes dejar python app.py en desarrollo)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "2"]