import paho.mqtt.client as mqtt
import firebase_admin
from firebase_admin import credentials, firestore
import json
from datetime import datetime, timezone

# Configuración de Firebase
cred = credentials.Certificate('credenciales.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Configuración MQTT
BROKER = '127.0.0.1'
PORT = 1883
TOPIC_CPU = 'examen/cpu'
TOPIC_RAM = 'examen/ram'

# ID del documento en Firestore
DOC_ID = 'base_de_datos_laptop'

# Asegurarse de que el documento exista y tenga una estructura inicial
def ensure_document_exists():
    doc_ref = db.collection('datos').document(DOC_ID)
    doc = doc_ref.get()
    if not doc.exists:
        doc_ref.set({
            'cpu_logs': [],
            'ram_logs': []
        })

# Callback cuando el cliente recibe un mensaje
def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    data = json.loads(payload)
    
    timestamp = datetime.now(timezone.utc).isoformat()  # Obtiene la fecha y hora actual en UTC

    # Asegurarse de que el documento exista antes de actualizar
    ensure_document_exists()

    # Preparar los datos con la marca de tiempo
    record = {
        'value': data.get('cpu_usage') or data.get('ram_usage'),
        'timestamp': timestamp
    }

    # Actualizar el documento con datos nuevos
    if message.topic == TOPIC_CPU:
        db.collection('datos').document(DOC_ID).update({
            'cpu_logs': firestore.ArrayUnion([record])
        })
    elif message.topic == TOPIC_RAM:
        db.collection('datos').document(DOC_ID).update({
            'ram_logs': firestore.ArrayUnion([record])
        })

def main():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    
    client.subscribe(TOPIC_CPU)
    client.subscribe(TOPIC_RAM)
    
    client.loop_forever()

if __name__ == "__main__":
    main()
