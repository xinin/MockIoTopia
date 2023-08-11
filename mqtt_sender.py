import paho.mqtt.client as mqtt
import ssl

# Configuración de conexión
mqtt_broker = "a2f8qpo41xhi6t-ats.iot.eu-west-1.amazonaws.com"

mqtt_port = 8883
mqtt_ca_cert = "AmazonRootCA1.pem"
mqtt_client_cert = "certificate.pem.crt"
mqtt_client_key = "private.pem.key"

# Función de callback cuando se establece la conexión
def on_connect(client, userdata, flags, rc):
    print("Conectado con el código:", rc)

# Función de callback cuando se recibe un mensaje
def on_message(client, userdata, msg):
    print("Mensaje recibido:", msg.payload.decode())

# Crear instancia del cliente MQTT con TLS/SSL
client = mqtt.Client(client_id="your_client_id")
client.tls_set(ca_certs=mqtt_ca_cert, certfile=mqtt_client_cert, keyfile=mqtt_client_key, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)

# Configurar callbacks
client.on_connect = on_connect
client.on_message = on_message

# Conectar al broker
client.connect(mqtt_broker, mqtt_port)

# Iniciar loop para manejar comunicación
client.loop_start()

# Publicar un mensaje en un tópico
topic = "123"
message = "Hola, mundo!"

client.publish(topic, message)

# Mantener el programa en ejecución
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Desconexión solicitada por el usuario.")
    client.disconnect()
    client.loop_stop()
