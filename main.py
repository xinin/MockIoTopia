import paho.mqtt.client as mqtt
import ssl

# Configuración de los certificados
ca_cert = "ruta/al/ca_cert.pem"
client_cert = "ruta/al/client_cert.pem"
client_key = "ruta/al/client_key.pem"

# Configuración de la conexión MQTT
mqtt_broker = "direccion_del_broker"
mqtt_port = 8883
mqtt_topic = "tu/topic"

def on_connect(client, userdata, flags, rc):
    print("Conectado con código de resultado:", rc)
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print(f"Mensaje recibido en el topic '{msg.topic}': {msg.payload.decode()}")

client = mqtt.Client()
client.tls_set(ca_certs=ca_cert, certfile=client_cert, keyfile=client_key, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker, mqtt_port, keepalive=60)

client.loop_forever()
