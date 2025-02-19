#!/usr/bin/env bash
OIFS="$IFS"
IFS=$'\n'
for f in $*
do
    mimetype=`file -b -i "$f"`
    if [[ $mimetype == video* ]]; then
        echo "$f"
        ./upload.sh "$f"
    fi
done
IFS="$OIFS"
