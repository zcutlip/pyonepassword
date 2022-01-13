#!/bin/sh

ret=0

docker run   --rm -it -v "$(pwd):/usr/src/testdir" docker_py38
ret=`expr $? + $ret`
docker run   --rm -it -v "$(pwd):/usr/src/testdir" docker_py39
ret=`expr $? + $ret`
exit $ret
