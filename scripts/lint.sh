#!/bin/bash

default_tag="latest"
lint_tag="lint"

for service in "python/backend backend/." "node/frontend frontend/.";
do
    set -- $service
    default_image="$1:$default_tag"
    lint_image="$1:$lint_tag"
    
    if [[ $(docker images -q $default_image) ]]; then
        echo "Running linting for $default_image..."
        docker build --tag=$lint_image --target=$lint_tag $2
        docker run --rm $lint_image
        docker image rm $lint_image
    else
        echo "The docker image '$default_image' does not exist, please create the containers first with './scripts/create.sh'."
        exit 1
    fi
done
