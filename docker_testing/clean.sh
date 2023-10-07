#!/bin/sh

# keep unused docker image names so we can ensure they get removed
# this should not be an error
docker image rm docker_py38 docker_py39 docker_py310 docker_py311 docker_py312
rm -rf .tox-docker
