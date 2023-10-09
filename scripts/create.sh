#!/bin/bash

path="`dirname -- "$0"`/.."
echo $path
echo 'docker-compose -f "'$path'/infra/docker-compose.yaml" up -d --wait'
docker-compose -f "$path/infra/docker-compose.yaml" up -d --wait
