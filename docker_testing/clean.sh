#!/bin/sh

# keep unused docker image names so we can ensure they get removed
# this should not be an error
echo "Cleaning..."
echo "removing docker images"
docker image rm docker_py39 docker_py310 docker_py311 docker_py312 docker_py313
echo "removing .tox-docker"
rm -rf .tox-docker
echo "...done"
echo ""
