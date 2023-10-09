#!/bin/bash

path="`dirname -- "$0"`/.."
docker-compose -f "$path/infra/docker-compose.yaml" up -d
