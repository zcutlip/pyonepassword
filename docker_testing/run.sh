#!/bin/sh

ret=0

docker run   --rm -it -v "$(pwd):/usr/src/testdir" docker_py38 /test.sh "$@"
ret="$(($?+ret))"
docker run   --rm -it -v "$(pwd):/usr/src/testdir" docker_py39 /test.sh "$@"
ret="$(($?+ret))"
docker run   --rm -it -v "$(pwd):/usr/src/testdir" docker_py310 /test.sh "$@"
ret="$(($?+ret))"
exit "$ret"
