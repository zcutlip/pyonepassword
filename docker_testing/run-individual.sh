#!/bin/sh

quit(){
    set -x
    if [ $# -ge 2 ];
    then
        echo "$1"
        shift
    fi
    exit "$1"
}

handle_sig(){
    quit "Caught keyboard interrupt" 1
}

trap handle_sig INT


container=""

if [ "$1" = "py310" ];
then
    container="docker_py310"
    shift
elif [ "$1" = "py311" ];
then
    container="docker_py311"
    shift
elif [ "$1" = "py312" ];
then
    container="docker_py312"
    shift
elif [ "$1" = "py313" ];
then
    container="docker_py313"
    shift
fi

if [ -z "$container" ];
then
    quit "Specify py310, py311, py312, or py313" 1
fi


ret=0

docker run   --rm -it -v "$(pwd):/usr/src/testdir" "$container" /test.sh "$@"
ret="$(($?+ret))";

exit "$ret"
