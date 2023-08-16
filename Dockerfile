FROM python:3.10-alpine

# Path to the configuration file
ARG CONFIG_FILE

# Sets the working directory within the container
WORKDIR /app

# Copy the requirements file to the image
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files to the container
COPY src src

# Copy application files to the container
COPY certificates certificates

# Copy configuration file
COPY $CONFIG_FILE config.yml

# Run application when the container starts
CMD ["python", "/app/src/main.py", "-c", "config.yml", "-v"]