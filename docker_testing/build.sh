#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

docker build "$SCRIPT_DIR"/docker/ -f "$SCRIPT_DIR"/docker/Dockerfile_py38 -t docker_py38 || exit
docker build "$SCRIPT_DIR"/docker/ -f "$SCRIPT_DIR"/docker/Dockerfile_py39 -t docker_py39 || exit
