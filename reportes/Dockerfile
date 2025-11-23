# Imagen base
FROM python:3.10-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del microservicio
COPY . .

# Exponer puerto
EXPOSE 5002

# Comando de ejecución
CMD ["python", "app.py"]
