# Microservicio de Notificaciones
Microservicio desarrollado en **Flask** que permite enviar correos electrónicos individuales y masivos usando **Gmail (SMTP)**.

## Tecnologías
- **Framework:** Flask (Python)
- **Base de datos:** No aplica (noSQL no requerida)
- **Servidor de correo:** Gmail SMTP
- **Pruebas de carga:** Locust

## Instalar dependencias
pip install flask flask-mail flask-cors locust

# Ejecutar el microservicio
python app.py

## Endpoints principales
Método	Ruta	Descripción
GET	/	Información del servicio
GET	/health	Verifica el estado del microservicio y conexión SMTP
POST	/notify	Envía un correo individual
POST	/notify/bulk	Envía correos masivos a varios destinatarios

## Ejecutar Locust
locust -f notificaciones_locustfile.py

## Variables importantes
Variable	Descripción
MAIL_SERVER	Servidor SMTP (por defecto smtp.gmail.com)
MAIL_PORT	Puerto SMTP (587)
MAIL_USERNAME	Correo remitente
MAIL_PASSWORD	Contraseña de aplicación de Gmail
MAIL_DEFAULT_SENDER	Dirección por defecto del remitente