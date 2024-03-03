#!/bin/bash

# Set the directory where the Dockerfile and requirements.txt are located
DIRECTORY="$(pwd)"

# build docker image
docker build -t create-postgresql-db "$DIRECTORY"

# run docker container
docker run --env-file "$DIRECTORY/.env" --name con-create-postgresql-db

# get timestamp
TIMESTAMP=$(date +"%Y-%m-%d-%H-%M-%S")

# copy log into local src
docker logs con-load-local-data-into-s3 > "$DIRECTORY/logs/logs_$TIMESTAMP.txt"

# stop docker container
docker stop con-create-postgresql-db

# removing docker container
docker rm con-create-postgresql-db

# remove docker image
docker rmi --force create-postgresql-db