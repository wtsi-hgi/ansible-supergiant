#!/usr/bin/env bash

docker-compose -f tests/docker/docker-compose.test.yml up \
    --build --exit-code-from supergiant-test-runner --force-recreate --remove-orphans
