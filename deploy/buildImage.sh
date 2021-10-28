#!/bin/sh

docker rmi python-web
echo "remove old image"
docker build --network=host -t python-web .
