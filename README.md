# MockIoTopia
MockIoTopia: MQTT Adventures in Simulated IoT



# Obtención de Certificados IoT Core

Desde IotCore en la sección Seguridad > Certificados crear un nuevo certificado. Importante descargar en ese momento la key y el cert, así como el pem de la CA dado que luego no podrá volver a ser descargado.

Despues asignar una policy a ese certificado que le permita conectarse a IoT y publicar mensajes.

Para obtener el endopint de conexión de IoT Core se va a la sección Settings > Device data endpoint

