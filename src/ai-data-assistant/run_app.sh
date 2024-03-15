#!/bin/bash

# Set the directory where the Dockerfile and requirements.txt are located
DIRECTORY="$(pwd)"

# Change it as per your requirement
LAYER_NAME="aiDataAssistant-layer"

# Build the Docker image
docker build -t lambda-layer "$DIRECTORY"

# Run the Docker container to create the layer
docker run --name lambda-layer-container -v "$DIRECTORY:/app" lambda-layer

# create layers directory, if not created.

mkdir -p layers

# List files in the current directory (for debugging purposes)
ls

# Move the zip file in layers directory.
mv "$DIRECTORY/$LAYER_NAME.zip" "$DIRECTORY/layers"

# Stop the conainer
docker stop lambda-layer-container

# Remove the running conainer
docker rm lambda-layer-container

# Cleanup: remove the Docker image
docker rmi --force lambda-layer