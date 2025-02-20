#!/bin/bash
OIFS="$IFS"
IFS=$'\n'
for f in $*
do
    mimetype=`file -b -i "$f"`
    if [[ $mimetype == video* ]]; then
        echo "$f"
        ./whisper_transcribe.sh "$f"
    fi
done
IFS="$OIFS"
