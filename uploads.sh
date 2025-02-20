#!/usr/bin/env bash
OIFS="$IFS"
IFS=$'\n'
for f in $*
do
    mimetype=`file -b -i "$f"`
    if [[ $mimetype == video* ]]; then
        echo "$f"
        ./upload.sh "$f"
        if [ "$?" -eq 0 ]; then
            echo "upload reports successful"
        else
            echo "upload failed"
        fi
    fi
done
IFS="$OIFS"
