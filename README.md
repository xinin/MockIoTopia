# MockIoTopia

## MQTT Adventures in Simulated IoT

The objective of this tool is the simulation of an IoT device which sends customised messages to an MQTT broker, such as AWS IoT Core.

<p align="center">
  <img src="image.png" alt="Texto alternativo" width="300" height="300">
</p>

## 1. Configuration
To customize the tool's operation, a YAML configuration file is employed. You can refer to the `example_config.yml` file for instances demonstrating all potential functionalities.

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

Below is an example of a configuration:

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

#### 1.1.1. Certificates stored in S3
It is also possible to store the certificates in an S3 bucket. To do this it would be enough to indicate the S3 file path, activate the flag `stored_in_s3: True` and provide the necessary credentials.

```
MQTT:
  ClientID: MockIoTopia
  Host: "a2f8qpo41xhi6t-ats.iot.eu-west-1.amazonaws.com"
  Port: 8883
  Topic: "123"
  Certificates:
    stored_in_s3: True
    ca_cert: "s3://my-bucket/certificates/AmazonRootCA1.pem"
    client_cert: "s3://my-bucket/certificates/certificate.pem.crt"
    client_key: "s3://my-bucket/certificates/private.pem.key"
```

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

Simulating fields with integer type involves adjusting their operation through the **primary settings, specifically the** `Max` **and **`Min`** values**.

These fields can exhibit either a randomized pattern or adhere to a predefined probability and extent of alteration.

This configuration is established within the `Behaviour` section, where the **choice** between `Random` or `Permanent` is indicated.
In the case of the latter, parameters like `VariationProbability` and `VariationMagnitude`, representing probabilities ranging from 0 to 1, should be included.

``````
    -
      Name: My_Parameter_Int_Random
      Description: "Example of a Int_Random"
      Type: int
      Max: 10
      Min: 0
      Behaviour:
        Type: Random
    - 
      Name: My_Parameter_Int_Permanent
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

Similar to the integer case, the behavior remains consistent; however, an additional parameter called `Decimals` is introduced to indicate the number of decimal places.

```
    -
      Name: My_Parameter_Float_Random
      Description: "Example of a Float_Random"
      Type: float
      Max: 10
      Min: 0
      Decimals: 4
      Behaviour:
        Type: Random
    - 
      Name: My_Parameter_Float_Permanent
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

These parameter types are employed to simulate the behavior of boolean values, which can either be random or adhere to a probability of variation defined by the `VariationProbability` parameter and the specification of the default value using the `Default` parameter (0 or 1). 

The resulting values are 0 or 1.

> Unlike the other parameters, the `Boolean_Permanent` type reverts to the `Default` state after a change triggered by its `VariationProbability`, with the aim of simulating flags in a real environment. 
If this behavior is not desired, it is advisable to use the `Int_Permanent` type.

```
    - 
      Name: My_Parameter_Boolean_Random
      Description: "Example of a Boolean_Random"
      Type: boolean
      Behaviour:
        Type: Random
    - 
      Name: My_Parameter_Boolean_Permanent
      Description: "Example of a Boolean_Permanent"
      Type: boolean
      Behaviour:
        Type: Permanent
        VariationProbability: 0.5
        Default: 0
```

#### 1.3.4. String
Parameter type that simulates text strings, similarly to the other cases, we have the `Random` mode, which we modify the output dimension through the `Length` parameter. 
On the other hand, there is the `Permanent` option where a `Default` value must be provided.

```
- 
      Name: My_Parameter_String_Random
      Description: "Example of a String_Random"
      Type: string
      Behaviour:
        Type: Random
        Length: 50
    - 
      Name: My_Parameter_String_Permanent
      Description: "Example of a String_Permanent"
      Type: string
      Behaviour:
        Type: Permanent
        Default: "This is an string example"
```

#### 1.3.5. Date
The last type of parameter is the date field, which has different formats, which is controlled by the `Type` field in the `Behaviour` section.

- **Date_UnixEpoch:** The Unix epoch (or Unix time or POSIX time or Unix timestamp) is the number of seconds that have elapsed since January 1, 1970 (midnight UTC/GMT). 
>For example: 1692170608

- **Date_UnixEpochMilis:** The Unix epoch in miliseconds.
>For example: 1692170608177

- **Date_ISO8601:** Date in ISO 8601 format in UTC
>For example: "2023-08-16T07:23:28.177668"

```
    - 
      Name: My_Parameter_Date_UnixEpoch
      Description: "Example of a Date_UnixEpoch"
      Type: date
      Behaviour:
        Type: UnixEpoch
    - 
      Name: My_Parameter_Date_UnixEpochMilis
      Description: "Example of a Date_UnixEpochMilis"
      Type: date
      Behaviour:
        Type: UnixEpochMilis
    - 
      Name: My_Parameter_Date_ISO8601
      Description: "Example of a Date_ISO8601"
      Type: date
      Behaviour:
        Type: ISO8601
```

#### 1.3.6. Array
The `Array` format makes use of the other data types mentioned above.
> It is important **not to include the** `Name` **field** in the array components and to indicate them in the order in which you want to have the output order.
```
    -
      Name: My_Parameter_Array
      Description: "Example of an Array"
      Type: array
      Fields:
        - 
          Description: "Example of a Int_Permanent"
          Type: int
          Max: 10
          Min: 0
          Behaviour:
            Type: Permanent
            VariationProbability: 0.1
            VariationMagnitude: 0.5
        -
          Description: "Example of a Date_ISO8601"
          Type: date
          Behaviour:
            Type: ISO8601
```

#### 1.3.7. Object
Similar to the `Array` type, the `Object` type can contain the other objects mentioned above.
> In this case, **the** `Name` **attribute must be included**, unlike in `Array`.

```
 - Name: My_Parameter_Object
      Description: "Example of an Object field"
      Type: object
      Fields:
        - 
          Name: My_Parameter_Int_field
          Description: "Example of a Int_Permanent"
          Type: int
          Max: 10
          Min: 0
          Behaviour:
            Type: Permanent
            VariationProbability: 0.1
            VariationMagnitude: 0.5
        -
          Name: My_Parameter_Date_ISO8601
          Description: "Example of a Date_ISO8601"
          Type: date
          Behaviour:
            Type: ISO8601
```

#### 1.3.8. Recursivity in Arrays and Objects
The `Array` and `Object` data type can be included inside another field of type `Array` or `Object` and vice versa.

```
    -
        Name: My_Parameter_Array
        Description: "Example of an Array"
        Type: array
        Fields:
            -
                Description: "Example of an Object In an Array"
                Type: object
                Fields:
                    - 
                        Description: "Example of an Array in Object"
                        Type: array
                        Fields:
                            - 
                                Name: My_Parameter_Int_field
                                Description: "Example of a Int_Permanent"
                                Type: int
                                Max: 10
                                Min: 0
                                Behaviour:
                                Type: Random

```
## 2. Usage
Once the YAML configuration file is set up, the tool is ready to use.

It can be used directly from local by installing the libraries or from the provided container.

### 2.1 Local

Installation of dependencies

```
pip install -r requirements.txt
```
To run it, you need to specify the YAML configuration file with the `--config` or `-c` parameter. Additionally you can include the `--verbose` or `-v` parameter to display more information on the screen.

```
python src/main.py -c example_config.yml -v
```

### 2.2 Container

To make use of the tool from the container provided in the `Dockerfile` file, it is done as follows:

#### 2.2.1. Local files

The certificates must be included in the `certificates` folder so that they are copied into the container and they must be referenced correctly in the YAML configuration file.

During the build you must use the `CONFIG_FILE` parameter with the path to the YAML configuration file you want to use.

1. Build the container image
```
docker build --build-arg CONFIG_FILE=example_config.yml . -t mockiotopia
```

2. Run
```
docker run mockiotopia
```

#### 2.2.2. S3 Files

As mentioned in the [previous point](#111-configuration-files-in-s3), it is possible to make use of files stored in S3, both for the global configuration file and for the certificates.

To do this, follow the steps below:

1. Set the AWS credentials in the terminal from which the container image will be built:

```
export AWS_ACCESS_KEY_ID="...."
export AWS_SECRET_ACCESS_KEY="...."
export AWS_SESSION_TOKEN="...."
`````

2. Initiate the build while changing the parameter `CONFIG_FILE` to `CONFIG_FILE_S3`. Additionally, it is necessary to provide the following parameters to obtain the AWS credentials:
```
docker build . --no-cache \
    --build-arg CONFIG_FILE_S3=s3://<my-bucket>/config.yml \
    --build-arg AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    --build-arg AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    --build-arg AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN \
    -t mockiotopia
```

3. Run the container

```
docker run mockiotopia
```

If the certificates referenced in the configuration file are also hosted in S3, when executing it, you must include the environment variables `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_SESSION_TOKEN`.

```
docker run -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    -e AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN \
    mockiotopia
```

## 3. Connecting to an AWS IoTCore

To connect to an IoTCore you need to follow these steps

1. From **IoTCore** in the **Security > Certificates** section create a new certificate. 

> It is important to download the key and the cert, as well as the pem of the CA at that moment, as it will not be able to be downloaded again later.

2. Then **assign a policy to this certificate** that allows you to connect to IoT and publish messages.

3. To obtain the IoT Core connection endopint, go to the **Settings > Device data endpoint** section.

