import argparse
import sys
import traceback
import time
import ssl
import json
import random
import tempfile

import boto3
import paho.mqtt.client as mqtt
import yaml
from yaml.loader import SafeLoader

from message_generator import generate_message
 
parser = argparse.ArgumentParser(description="MockIoTopia")
parser.add_argument("-v", "--verbose", help="Show debugging information", action="store_true")
parser.add_argument("-c", "--config", help="Path configuration file", type=str)

args = parser.parse_args()

config = None
connected = False

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
    interval =  config["Miscellanea"]["IntervalMilis"]
    loss_probability =  config["Miscellanea"]["MessageLossProbability"]

    print("\nEstablishing the connection ... ")

    MQTT_config = config["MQTT"]
    mqtt_client_id = MQTT_config["ClientID"]
    mqtt_host = MQTT_config["Host"]
    mqtt_port = MQTT_config["Port"]
    mqtt_topic = MQTT_config["Topic"]
    mqtt_ca_cert = MQTT_config["Certificates"]["ca_cert"]
    mqtt_client_cert = MQTT_config["Certificates"]["client_cert"]
    mqtt_client_key = MQTT_config["Certificates"]["client_key"]

    mqtt_in_s3 = MQTT_config.get("Certificates").get("stored_in_s3")
    if mqtt_in_s3 is not None:

        def download_cert_from_s3 (path):
            s3 = boto3.client('s3')
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                parts = path.split('/')
                bucket_name = parts[2]
                file_name = '/'.join(parts[3:])

                s3.download_fileobj(bucket_name, file_name, temp_file)
                return temp_file.name

        mqtt_ca_cert = download_cert_from_s3(mqtt_ca_cert)
        mqtt_client_cert = download_cert_from_s3(mqtt_client_cert)
        mqtt_client_key = download_cert_from_s3(mqtt_client_key)

    # Callback function on connection establishment
    def on_connect(client, userdata, flags, rc):
        global connected
        print("Connected with the code:", rc)
        connected = True

    # Create MQTT client instance with TLS/SSL
    client = mqtt.Client(client_id=mqtt_client_id)
    client.tls_set(ca_certs=mqtt_ca_cert, certfile=mqtt_client_cert, keyfile=mqtt_client_key, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)

    # Configure callbacks
    client.on_connect = on_connect

    # Connection to the host
    client.connect(mqtt_host, mqtt_port)

    # Start loop to manage communication
    client.loop_start()
  
    message = None

    try:
        while not connected:
            time.sleep(1)

        while True:
            message = generate_message(config["Messages"], message)
            if random.random() < loss_probability:
                print("## MESSAGE LOST ##", message, "\n-------------------------")
            else:
                client.publish(mqtt_topic, json.dumps(message))
                if args.verbose:
                    print(message, "\n-------------------------")
            time.sleep(interval/1000)
    
    except KeyboardInterrupt:
        # Finish loop and close connection
        print("Disconnection requested by the user.")
        client.disconnect()
        client.loop_stop()

except(KeyError):
    print("\nERROR parsing configuration")
    traceback.print_exc()
    sys.exit()

print("See you soon!")