#!/bin/bash

# Set the directory where the Dockerfile and requirements.txt are located
DIRECTORY="$(pwd)"

# build docker image
docker build -t load-local-data-into-s3 "$DIRECTORY"

# run docker container
docker run -v dataset:/dataset --env-file "$DIRECTORY/.env" --name con-load-local-data-into-s3 load-local-data-into-s3

# get timestamp
TIMESTAMP=$(date +"%Y-%m-%d-%H-%M-%S")

# copy log into local src
docker logs con-load-local-data-into-s3 > "$DIRECTORY/logs/logs_$TIMESTAMP.txt"

# stop docker container
docker stop con-load-local-data-into-s3

# removing docker container
docker rm con-load-local-data-into-s3

# remove docker image
docker rmi --force load-local-data-into-s3

# remove docker vol
docker volume rm dataset