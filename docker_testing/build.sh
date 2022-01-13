#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

docker build "$SCRIPT_DIR"/docker/3.8 -t docker_py38
docker build "$SCRIPT_DIR"/docker/3.9 -t docker_py39
