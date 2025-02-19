#!/bin/bash
OIFS="$IFS"
IFS=$'\n'
for f in $*
do
    mimetype=`file -b -i "$f"`
    if [[ $mimetype == video* ]]; then
        echo "$f"
        ./generate_thumbnail.sh "$f"
    fi
done
IFS="$OIFS"
