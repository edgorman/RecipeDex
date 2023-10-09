#!/bin/bash

default_tag="latest"
test_tag="test"

for service in "python/backend backend/." "node/frontend frontend/.";
do
    set -- $service
    default_image="$1:$default_tag"
    test_image="$1:$test_tag"
    
    if [[ $(docker images -q $default_image) ]]; then
        echo "Running tests for $default_image..."
        docker build --tag=$test_image --target=$test_tag $2
        docker run --rm $test_image
        docker image rm $test_image
    else
        echo "The docker image '$default_image' does not exist, please create the containers first with './scripts/create.sh'."
        exit 1
    fi
done
