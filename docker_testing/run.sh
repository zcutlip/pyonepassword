#!/bin/sh

quit(){
    set -x
    if [ $# -ge 2 ];
    then
        echo "$1"
        shift
    fi
    kill -TERM -$$
}

handle_sig(){
    quit "Got keyboard interrupt" 1
}

trap handle_sig INT


ret=0

docker run   --rm -it -v "$(pwd):/usr/src/testdir" docker_py38 /test.sh "$@"
ret="$(($?+ret))"
docker run   --rm -it -v "$(pwd):/usr/src/testdir" docker_py39 /test.sh "$@"
ret="$(($?+ret))"
docker run   --rm -it -v "$(pwd):/usr/src/testdir" docker_py310 /test.sh "$@"
ret="$(($?+ret))"
docker run   --rm -it -v "$(pwd):/usr/src/testdir" docker_py311 /test.sh "$@"
ret="$(($?+ret))"
docker run   --rm -it -v "$(pwd):/usr/src/testdir" docker_mypy /test.sh "$@"
ret="$(($?+ret))"
exit "$ret"
