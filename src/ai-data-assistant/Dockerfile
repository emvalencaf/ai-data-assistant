# Use the official Python runtime as the base image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install any necessary dependencies
RUN apt-get update && apt-get install -y zip && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file to the working directory
COPY requirements.txt .

# Install the Python packages listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt -t /opt/python/

# Set the CMD to zip the installed packages into a layer
CMD cd /opt && zip -r9 /app/aiDataAssistant-layer.zip .