#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Building..."

docker buildx build "$SCRIPT_DIR"/docker/ -f "$SCRIPT_DIR"/docker/py310.Dockerfile -t docker_py310 || exit
docker buildx build "$SCRIPT_DIR"/docker/ -f "$SCRIPT_DIR"/docker/py311.Dockerfile -t docker_py311 || exit
docker buildx build "$SCRIPT_DIR"/docker/ -f "$SCRIPT_DIR"/docker/py312.Dockerfile -t docker_py312 || exit
docker buildx build "$SCRIPT_DIR"/docker/ -f "$SCRIPT_DIR"/docker/py313.Dockerfile -t docker_py313 || exit

echo "...done"
echo ""
