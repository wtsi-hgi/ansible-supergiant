#!/usr/bin/env bash

set -euf -o pipefail

docker-compose -f tests/docker/docker-compose.test.yml rm -fs
docker-compose -f tests/docker/docker-compose.test.yml up \
    --build --exit-code-from supergiant-test-runner --force-recreate --remove-orphans
