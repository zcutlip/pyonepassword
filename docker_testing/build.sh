#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

docker build "$SCRIPT_DIR"/docker/ -f "$SCRIPT_DIR"/docker/py38.Dockerfile -t docker_py38 || exit
docker build "$SCRIPT_DIR"/docker/ -f "$SCRIPT_DIR"/docker/py39.Dockerfile -t docker_py39 || exit
docker build "$SCRIPT_DIR"/docker/ -f "$SCRIPT_DIR"/docker/py310.Dockerfile -t docker_py310 || exit
