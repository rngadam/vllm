#!/usr/bin/env bash

set +x

FILENAME=$1
THUMBNAIL_FILENAME=$1.thumbnail.jpg
CAPTION_FILENAME=$1.thumbnail.jpg.caption.txt
TRANSCRIBE_FILENAME=$1.whisper.json
OUTPUT=$FILENAME.upload

function check_file_exists() {
    if [ ! -f "$1" -o ! -s "$1" ]; then
        echo "Missing or empty $1"
        exit 1
    fi
}

if [ -f "$OUTPUT" ]; then
    echo "$OUTPUT exists, this has already been processed, exiting"
    exit
fi
check_file_exists $FILENAME
check_file_exists $THUMBNAIL_FILENAME
check_file_exists $CAPTION_FILENAME
check_file_exists $TRANSCRIBE_FILENAME

LANGUAGE=`jq -r .language $TRANSCRIBE_FILENAME`
DESCRIPTION=`jq -r .text $TRANSCRIBE_FILENAME`
CAPTION=`cat $CAPTION_FILENAME`
BASENAME=`basename $FILENAME`

echo "FILENAME=$FILENAME"
echo "LANGUAGE=$LANGUAGE"
echo "DESCRIPTION=$DESCRIPTION"
echo "CAPTION=$CAPTION"

echo "$FILENAME"
peertube-cli upload \
    --verbose 4 \
    --file "$FILENAME" \
    --video-name "$CAPTION" \
    --url https://peertube.coderbunker.ca \
    --thumbnail "$THUMBNAIL" \
    --video-description "$BASENAME: $DESCRIPTION" \
    --language "$LANGUAGE" \
    --privacy 2 \
    --channel-name ricky \
    --no-wait-transcoding > $OUTPUT
