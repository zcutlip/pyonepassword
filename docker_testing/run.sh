#!/bin/sh

# shellcheck disable=SC2317
# shell-check can't see handle_sig() or quit()
# since they get called via trap
quit(){
    set -x
    if [ $# -ge 2 ];
    then
        echo "$1"
        shift
    fi
    kill -TERM $$
}

handle_sig(){
    quit "Got keyboard interrupt" 1
}

trap handle_sig INT


ret=0

echo "Running docker tests..."
docker run   --rm -it -v "$(pwd):/usr/src/testdir" docker_py39 /test.sh "$@"
ret="$(($?+ret))"
docker run   --rm -it -v "$(pwd):/usr/src/testdir" docker_py310 /test.sh "$@"
ret="$(($?+ret))"
docker run   --rm -it -v "$(pwd):/usr/src/testdir" docker_py311 /test.sh "$@"
ret="$(($?+ret))"
docker run   --rm -it -v "$(pwd):/usr/src/testdir" docker_py312 /test.sh "$@"
ret="$(($?+ret))"

echo "...done"
echo ""
exit "$ret"
