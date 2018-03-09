#!/usr/bin/env bash

docker-compose -f tests/docker/docker-compose.test.yml up \
    --build --exit-code-from ansible-supergiant-test --force-recreate --remove-orphans
