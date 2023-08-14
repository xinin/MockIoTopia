# MockIoTopia
## MQTT Adventures in Simulated IoT

The objective of this tool is the simulation of an IoT device which sends customised messages to an MQTT broker, such as AWS IoT Core.

## 1. Configuration
To modify the operation of the tool, a YAML configuration file is used.

The file is divided into several sections

````
MQTT:
    # Host configuration
Miscellanea:
    # Extra tool configurations
Messages:
    # Configuration of the different attributes that the message will have and its characteristics.
````

### 1.1. MQTT

To establish a connection to the MQTT broker, only the option using SSL and with certificates is available.

Below is an example of a configuration

`````
MQTT:
  ClientID: MockIoTopia
  Host: "xxxxxxx-ats.iot.eu-west-1.amazonaws.com"
  Port: 8883
  Topic: "my-topic"
  Certificates:
    ca_cert: "certificates/AmazonRootCA1.pem"
    client_cert: "certificates/certificate.pem.crt"
    client_key: "certificates/private.pem.key"
`````

### 1.2. Miscellanea

This section details general behaviours of the tool.

````
Miscellanea:
  IntervalMilis: 2000 #Interval in miliseconds between messages
  MessageLossProbability: 0.5 #Probability of the message not being sent
````

### 1.3. Messages
TODO

## 2. Usage
Once the YAML configuration file is set up, the tool is ready to use.

It can be used directly from local by installing the libraries or from the provided container.

### 2.1 Local

Installation of dependencies

```
pip install -r requirements.txt
```
To run it, you need to specify the YAML configuration file with the **--config** or **-c** parameter. Additionally you can include the **--verbose** or **-v** parameter to display more information on the screen.

```
python main.py -c my-config.yml -v
```

### 2.2 Container
TODO



## 3. Connecting to an AWS IoTCore

To connect to an IoTCore you need to follow these steps

1. From **IoTCore** in the **Security > Certificates** section create a new certificate. 

> It is important to download the key and the cert, as well as the pem of the CA at that moment, as it will not be able to be downloaded again later.

2. Then **assign a policy to this certificate** that allows you to connect to IoT and publish messages.

3. To obtain the IoT Core connection endopint, go to the **Settings > Device data endpoint** section.

