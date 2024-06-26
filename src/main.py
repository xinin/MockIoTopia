import sys
import traceback
import time
import ssl
import json
import random
import os

import pkg_resources

installed_packages = pkg_resources.working_set
installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
for package in installed_packages_list:
    print(package)


import boto3
import paho.mqtt.client as mqtt
import yaml
from yaml.loader import SafeLoader

from message_generator import generate_message
 
def download_from_s3 (path):
    s3 = boto3.client('s3')
    
    parts = path.split('/')
    local_file_path='./'+parts[-1]
    bucket_name = parts[2]
    s3_key = '/'.join(parts[3:])
    s3.download_file(bucket_name, s3_key, local_file_path)
    
    return local_file_path


config = None
connected = False

try:
    config_path = os.getenv('CONFIG_FILE')
    if config_path is None:
        raise ValueError('CONFIG_FILE undefined, trying to load local config from ./config.yml')
    config=download_from_s3(config_path)
    with open(config) as f:
        config = yaml.load(f, Loader=SafeLoader)
except Exception as e:
    print(f"\n{str(e)}")
    traceback.print_exc()
    config_path='./config.yml'
    try:
        with open(config_path, 'r') as f:
            config = yaml.load(f, Loader=SafeLoader)
    except Exception as local_e:
        print(f"Failed to load local config: {str(local_e)}")
        traceback.print_exc()
        sys.exit("Error: Unable to load any configuration file")

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
        mqtt_ca_cert = download_from_s3(mqtt_ca_cert)
        mqtt_client_cert = download_from_s3(mqtt_client_cert)
        mqtt_client_key = download_from_s3(mqtt_client_key)


    # Callback function on connection establishment
    def on_connect(client, userdata, flags, rc):
        global connected
        if not connected:
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
            message = generate_message(config["Message"], message)
            if random.random() < loss_probability:
                print("## MESSAGE LOST ##", message, "\n-------------------------")
            else:
                client.publish(mqtt_topic, json.dumps(message))
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