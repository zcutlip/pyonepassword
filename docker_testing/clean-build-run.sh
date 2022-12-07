#!/bin/sh

curdir="$(cd "$(dirname "$0")" || exit; pwd)"

clean_script="$curdir/clean.sh"
build_script="$curdir/build.sh"
run_script="$curdir/run.sh"

"$clean_script" || exit
"$build_script" || exit
"$run_script" || exit
