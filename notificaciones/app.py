from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import logging
import os
from datetime import datetime

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# Configuración de Flask-Mail para Gmail - CON NUEVO CORREO
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_DEBUG'] = False
app.config['MAIL_SUPPRESS_SEND'] = False

# Configuración adicional para mejor compatibilidad
app.config['MAIL_ASCII_ATTACHMENTS'] = False
mail = Mail(app)

@app.route('/')
def home():
    """Endpoint principal para verificar que el servicio está funcionando"""
    return jsonify({
        'service': 'Microservicio de Notificaciones',
        'status': 'Activo',
        'version': '1.0',
        'email_from': 'lorenacardenasaguirre@gmail.com',
        'endpoints': {
            'GET /': 'Información del servicio',
            'GET /health': 'Estado de salud del servicio',
            'POST /notify': 'Enviar notificación por email',
            'POST /notify/bulk': 'Envío masivo de notificaciones'
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar el estado de salud del servicio"""
    try:
        # Verificar conexión con el servidor de correo
        with mail.connect() as conn:
            pass
        return jsonify({
            'status': 'healthy',
            'service': 'notification-service',
            'mail_server': 'connected',
            'email_account': 'lorenacardenasaguirre@gmail.com',
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error en health check: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'service': 'notification-service',
            'mail_server': 'disconnected',
            'email_account': 'lorenacardenasaguirre@gmail.com',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/notify', methods=['POST'])
def send_notification():
    """
    Endpoint para enviar notificaciones por correo electrónico
    Body JSON esperado:
    {
        "to": "sebastianworks21@gmail.com",
        "subject": "Asunto del correo",
        "body": "Contenido del mensaje",
        "html": "<p>Contenido HTML opcional</p>"
    }
    """
    try:
        # Verificar que se recibió JSON
        if not request.is_json:
            return jsonify({'error': 'Content-Type debe ser application/json'}), 400
        
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['to', 'subject', 'body']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo requerido faltante: {field}'}), 400

        # Validar formato de email
        to_email = data['to']
        if '@' not in to_email or '.' not in to_email:
            return jsonify({'error': 'Formato de email inválido'}), 400

        # Crear mensaje
        msg = Message(
            subject=data['subject'],
            recipients=[to_email]
        )

        # Usar HTML si está disponible, sino usar texto plano
        if 'html' in data:
            msg.html = data['html']
            msg.body = data['body']  # Fallback en texto plano
        else:
            msg.body = data['body']

        # Enviar correo
        mail.send(msg)
        
        logger.info(f"Notificación enviada exitosamente a: {to_email}")
        
        return jsonify({
            'message': 'Notificación enviada exitosamente',
            'from': 'lorenacardenasaguirre@gmail.com',
            'to': to_email,
            'subject': data['subject'],
            'timestamp': datetime.now().isoformat()
        }), 200

    except Exception as e:
        error_msg = f'Error al enviar notificación: {str(e)}'
        logger.error(error_msg)
        
        # Manejar errores específicos de SMTP
        if "535" in str(e) or "BadCredentials" in str(e):
            return jsonify({
                'error': 'Error de autenticación con el servidor de correo. Verifica las credenciales.',
                'solution': 'Usa una contraseña de aplicación de Gmail en lugar de la contraseña normal.',
                'email_account': 'lorenacardenasaguirre@gmail.com'
            }), 500
        elif "Connection refused" in str(e):
            return jsonify({
                'error': 'No se puede conectar al servidor de correo.',
                'solution': 'Verifica la configuración SMTP y la conexión a internet.'
            }), 500
        else:
            return jsonify({'error': error_msg}), 500

@app.route('/notify/bulk', methods=['POST'])
def send_bulk_notifications():
    """
    Endpoint para enviar notificaciones a múltiples destinatarios
    Body JSON esperado:
    {
        "recipients": ["locardenasa@unal.edu.co"],
        "subject": "Asunto del correo",
        "body": "Contenido del mensaje"
    }
    """
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['recipients', 'subject', 'body']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo requerido faltante: {field}'}), 400

        recipients = data['recipients']
        if not isinstance(recipients, list) or len(recipients) == 0:
            return jsonify({'error': 'recipients debe ser una lista no vacía'}), 400

        results = []
        for recipient in recipients:
            try:
                msg = Message(
                    subject=data['subject'],
                    recipients=[recipient],
                    body=data['body']
                )
                mail.send(msg)
                results.append({'to': recipient, 'status': 'success'})
                logger.info(f"Notificación enviada a: {recipient}")
            except Exception as e:
                results.append({'to': recipient, 'status': 'error', 'error': str(e)})
                logger.error(f"Error enviando a {recipient}: {str(e)}")

        return jsonify({
            'message': 'Proceso de envío masivo completado',
            'from': 'lorenacardenasaguirre@gmail.com',
            'results': results,
            'total_sent': len([r for r in results if r['status'] == 'success']),
            'total_failed': len([r for r in results if r['status'] == 'error']),
            'timestamp': datetime.now().isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Error en envío masivo: {str(e)}")
        return jsonify({'error': f'Error en envío masivo: {str(e)}'}), 500

# Manejo de errores global
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Método no permitido'}), 405

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    # Configuración para desarrollo
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5003))
    
    print(f" Iniciando Microservicio de Notificaciones...")
    print(f" URL: http://{host}:{port}")
    print(f" Debug: {debug_mode}")
    print(f" Cuenta de correo: lorenacardenasaguirre@gmail.com")
    print(f" Servidor de correo: {app.config['MAIL_SERVER']}:{app.config['MAIL_PORT']}")
    print(f"  IMPORTANTE: Configura la contraseña de aplicación en MAIL_PASSWORD")
    
    app.run(debug=debug_mode, host=host, port=port)