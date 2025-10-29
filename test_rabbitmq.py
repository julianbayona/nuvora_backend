"""Script de prueba para enviar un evento de vehículo a RabbitMQ"""
import pika
import json
from datetime import datetime

# Conectar a RabbitMQ
credentials = pika.PlainCredentials('admin', 'admin')
parameters = pika.ConnectionParameters(
    host='localhost',
    port=5672,
    credentials=credentials
)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='vehicle_events', durable=True)

# Evento de prueba
test_event = {
    'vehicle_type': 'car',
    'confidence': 0.95,
    'timestamp': datetime.now().isoformat(),
    'coordinates': {
        'x1': 100,
        'y1': 200,
        'x2': 400,
        'y2': 500
    },
    'plate_number': 'ABC123'
}

# Publicar evento
channel.basic_publish(
    exchange='',
    routing_key='vehicle_events',
    body=json.dumps(test_event),
    properties=pika.BasicProperties(delivery_mode=2)
)

print(f"✅ Evento de prueba enviado: {test_event}")
connection.close()
