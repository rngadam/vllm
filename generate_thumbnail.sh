#!/bin/bash

FILENAME=$1.thumbnail.jpg
if [ -f "$FILENAME" ]; then
    echo "exists: $FILENAME"
    exit
fi
ffmpeg -y -loglevel error -stats -i $1 -vf "select='eq(pict_type,I)',scale=320:-1" -vsync vfr -q:v 2 -frames:v 1 $FILENAME
echo "extracted $FILENAME"