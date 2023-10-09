#!/bin/bash

path="`dirname -- "$0"`/.."
echo $(ls -al)
docker-compose -f "$path/infra/docker-compose.yaml" up -d --wait
