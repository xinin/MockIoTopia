# MockIoTopia

>TODO
hacer el contenedor
probar a poner ruta desde s3 en local tanto para el config como las certs y usar un asume role en local

## MQTT Adventures in Simulated IoT

The objective of this tool is the simulation of an IoT device which sends customised messages to an MQTT broker, such as AWS IoT Core.

<p align="center">
  <img src="image.png" alt="Texto alternativo" width="300" height="300">
</p>

## 1. Configuration
To customize the tool's operation, a YAML configuration file is employed. You can refer to the **example_config.yml** file for instances demonstrating all potential functionalities.

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
There are different types of fields available to include in messages

> **All fields indicated in each of the types are mandatory.**

#### 1.3.1. Integer

Simulating fields with integer type involves adjusting their operation through the **primary settings, specifically the Max and Min values**.

These fields can exhibit either a randomized pattern or adhere to a predefined probability and extent of alteration.

This configuration is established within the "Behaviour" section, where the choice between **Random** or **Permanent** is indicated.
In the case of the latter, parameters like **VariationProbability** and **VariationMagnitude**, representing probabilities ranging from 0 to 1, should be included.

``````
    -
      Name: Int_Random
      Description: "Example of a Int_Random"
      Type: int
      Max: 10
      Min: 0
      Behaviour:
        Type: Random
    - 
      Name: Int_Permanent
      Description: "Example of a Int_Permanent"
      Type: int
      Max: 10
      Min: 0
      Behaviour:
        Type: Permanent
        VariationProbability: 0.5
        VariationMagnitude: 0.5
``````

#### 1.3.2. Float

Similar to the integer case, the behavior remains consistent; however, an additional parameter called **Decimals** is introduced to indicate the number of decimal places.

```
    -
      Name: Float_Random
      Description: "Example of a Float_Random"
      Type: float
      Max: 10
      Min: 0
      Decimals: 4
      Behaviour:
        Type: Random
    - 
      Name: Float_Permanent
      Description: "Example of a Float_Permanent"
      Type: float
      Max: 10
      Min: 0
      Decimals: 3
      Behaviour:
        Type: Permanent
        VariationProbability: 0.5
        VariationMagnitude: 0.5
```
#### 1.3.3. Boolean

These parameter types are employed to simulate the behavior of boolean values, which can either be random or adhere to a probability of variation defined by the **VariationProbability** parameter and the specification of the default value using the **Default** parameter. 
The resulting values are 0 or 1.

```
    - 
      Name: Boolean_Random
      Description: "Example of a Boolean_Random"
      Type: boolean
      Behaviour:
        Type: Random
    - 
      Name: Boolean_Permanent
      Description: "Example of a Boolean_Permanent"
      Type: boolean
      Behaviour:
        Type: Permanent
        VariationProbability: 0.5
        Default: 0
```

#### 1.3.4. String
TODO

#### 1.3.5. Date
TODO

#### 1.3.6. Array
TODO

#### 1.3.7. Object
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

