FROM python:3.10

# Create new user
RUN useradd -ms /bin/bash appuser


# Sets the working directory within the container
WORKDIR /app

# Copy the requirements file to the image
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files to the container
COPY src src
COPY certificates certificates
COPY config.yml config.yml

# New user as admin, giving permissions and setting it default user
RUN chmod 777 /tmp
RUN chmod 777 /app
RUN usermod -aG sudo appuser
USER appuser

# Run application when the container starts
CMD ["python", "/app/src/main.py"]
