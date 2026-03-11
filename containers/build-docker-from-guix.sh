#!/bin/bash

# Arguments management :
#  - No arguments : build the docker image and update the Dockerfile
#  - With argument "compose" : build the docker image and update the Dockerfile, then run the docker-compose command

export docker_archive=$(guix time-machine --channels=guix/channels.scm -- pack -f docker --manifest=guix/theo_opt_lectures-manifest.scm -S /bin=bin | tail -n 1)

echo "Docker archive created: ${docker_archive}"

docker_image_name=$(docker load < ${docker_archive} | grep -o 'Loaded image: [^ ]*' | cut -d ' ' -f 3)

sed -i "s/FROM.*/FROM ${docker_image_name}/" Dockerfile

if [ "$1" = "compose" ]; then
    docker compose up
else
    echo "Source image built and Dockerfile updated."
    echo "Run `docker compose up` to start the container."
fi