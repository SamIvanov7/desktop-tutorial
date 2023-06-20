#!/bin/bash

# Define variables
APP_NAME="JunoSolar Home Application"  # Name of your Django web app
DOCKERFILE_PATH="."  # The path to your Dockerfile
REGISTRY="registry.digitalocean.com"  # The registry domain
MY_REGISTRY_NAME="jsh-home-registry"  # Name of your registry
MY_IMAGE="jsh-app-image"  # The image tag you want to use

# Build Docker image
docker build -t $APP_NAME -f $DOCKERFILE_PATH/Dockerfile .

# Tag Docker image
docker tag $APP_NAME $REGISTRY/$MY_REGISTRY_NAME/$MY_IMAGE

# Login to DigitalOcean Registry
doctl registry login

# Push Docker image to DigitalOcean Registry
docker push $REGISTRY/$MY_REGISTRY_NAME/$MY_IMAGE
