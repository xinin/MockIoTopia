FROM python:3.10-alpine

# Path to the configuration file
ARG CONFIG_FILE
ARG CONFIG_FILE_S3=""
ARG AWS_ACCESS_KEY_ID=""
ARG AWS_SECRET_ACCESS_KEY=""
ARG AWS_SESSION_TOKEN=""

# Sets the working directory within the container
WORKDIR /app

# Copy the requirements file to the image
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Establece las variables de entorno para las credenciales de AWS
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN

# Copy application files to the container
COPY src src

# Copy application files to the container
COPY certificates certificates

# Always try to copy the local config file
COPY $CONFIG_FILE config.yml

# Selecting an s3 file overwrites the local one
RUN if [ -n "$CONFIG_FILE_S3" ] && [ "$CONFIG_FILE_S3" != "" ]; then \
        pip install awscli && \
        rm -rf config.yml && \
        aws s3 cp "$CONFIG_FILE_S3" config.yml; \
    fi

# Run application when the container starts
CMD ["python", "/app/src/main.py", "-c", "config.yml", "-v"]