# Usa una imagen base de Python
FROM python:3.10-alpine

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requerimientos a la imagen
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia los archivos de tu aplicación al contenedor
COPY src .

# Ejecuta tu aplicación cuando el contenedor se inicia
#CMD ["python", "app.py"]
