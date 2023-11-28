#!/bin/sh -e


image_num="$1"
count="$2"
output_path="$3"

if [ -z "$image_num" ] || [ -z "$count" ] || [ -z "$output_path" ];
then
    echo "USAGE: $0 <starting number> <count> <output path>"
    exit 1
fi

_gen_filename(){
    printf "image_%02d.png" "$1"
}

_gen_image_text(){
    printf "image %02d" "$1"
}

_gen_replacement_filename(){
    printf "replacement_image_%02d.png" "$1"
}

_gen_replacement_image_text(){
    printf "replacement image %02d" "$1"
}


max=$((image_num + count))

while [ "$image_num" -lt $max ];
do
    _image_filename_1="$(_gen_filename "$image_num")"
    _image_path_1="$output_path/$_image_filename_1"
    _image_text_1="$(_gen_image_text "$image_num")"

    _image_filename_2="$(_gen_replacement_filename "$image_num")"
    _image_path_2="$output_path/$_image_filename_2"
    _image_text_2="$(_gen_replacement_image_text "$image_num")"

    echo "Creating $_image_path_1"
    convert -size 400x100 -background "red" -fill "white" -pointsize 24 -gravity center label:"$_image_text_1" "$_image_path_1"
    echo "Creating $_image_path_2"
    convert -size 400x100 -background "blue" -fill "white" -pointsize 24 -gravity center label:"$_image_text_2" "$_image_path_2"

    image_num=$((image_num + 1))
done
