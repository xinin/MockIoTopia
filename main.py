import argparse
import sys
import traceback
import time
import ssl
import json

import paho.mqtt.client as mqtt
import yaml
from yaml.loader import SafeLoader

from message_generator import generate_message
from exceptions import FieldSintaxError
 
parser = argparse.ArgumentParser(description="MockIoTopia")
#TODO HACER UN HELP y cambiar los parametros para que tengo sentido en el futuro, todo en ingles
parser.add_argument("-v", "--verbose", help="Mostrar información de depuración", action="store_true")
parser.add_argument("-c", "--config", help="Ruta fichero configuración", type=str)

args = parser.parse_args()

config = None

if not args.config:
    print("ERROR: The path to the IoT message configuration file is required to continue.")
    sys.exit("Please set the -c or --config parameter")
else:
    with open(args.config) as f:
        config = yaml.load(f, Loader=SafeLoader)

art = r"""
 __  __               _     _____     _______             _        
 |  \/  |             | |   |_   _|   |__   __|           (_)       
 | \  / |  ___    ___ | | __  | |   ___  | |  ___   _ __   _   __ _ 
 | |\/| | / _ \  / __|| |/ /  | |  / _ \ | | / _ \ | '_ \ | | / _` |
 | |  | || (_) || (__ |   <  _| |_| (_) || || (_) || |_) || || (_| |
 |_|  |_| \___/  \___||_|\_\|_____|\___/ |_| \___/ | .__/ |_| \__,_|
                                                   | |              
                                                   |_|              
"""

print(art)

print("Configuration: \n")
print(yaml.safe_dump(config))

try:
    interval =  config["Miscellanea"]["interval_ms"]

    print("\nEstablishing the connection ... ")

    MQTT_config = config["MQTT"]
    mqtt_client_id = MQTT_config["ClientID"]
    mqtt_host = MQTT_config["Host"]
    mqtt_port = MQTT_config["Port"]
    mqtt_topic = MQTT_config["Topic"]
    mqtt_ca_cert = MQTT_config["Certificates"]["ca_cert"]
    mqtt_client_cert = MQTT_config["Certificates"]["client_cert"]
    mqtt_client_key = MQTT_config["Certificates"]["client_key"]

    # Callback function on connection establishment
    def on_connect(client, userdata, flags, rc):
        print("Connected with the code:", rc)

    # Create MQTT client instance with TLS/SSL
    client = mqtt.Client(client_id=mqtt_client_id)
    client.tls_set(ca_certs=mqtt_ca_cert, certfile=mqtt_client_cert, keyfile=mqtt_client_key, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)

    # Configurar callbacks
    client.on_connect = on_connect

    # Conectar al broker
    client.connect(mqtt_host, mqtt_port)

    # Iniciar loop para manejar comunicación
    client.loop_start()
  
    message = None

    try:
        while True:
            message = generate_message(config["Messages"], message)
            print("current message", message)
            client.publish(mqtt_topic, json.dumps(message))
            time.sleep(interval/1000)
    except KeyboardInterrupt:
        print("Disconnection requested by the user.")
        client.disconnect()
        client.loop_stop()

except(KeyError):
    print("\nERROR parsing configuration")
    traceback.print_exc()
    sys.exit()

print("See you soon!")