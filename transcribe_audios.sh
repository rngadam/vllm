#!/bin/bash
# This script processes every subdirectory ending with "_generated" in the directory passed as an argument.
# If the subdirectory does NOT contain a file named "transcription.json",
# it runs the `extract_audio.sh` script to extract audio from video files in that subdirectory
# and then uses a call to the whisper_server to obtain the transcription json output
# and writes that output to $BASENAME_generated/transcription.json.
#
# # Call example:
# # curl -X POST http://localhost:4000/ -F "file=@/media/Videos/PXL_20241111_213849122_generated/audio.wav"
#

set -euo pipefail

DIRNAME=$(dirname "$0")
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi
BASE_DIR="$1"
# Check if the base directory exists
if [ ! -d "$BASE_DIR" ]; then
    echo "Error: Directory $BASE_DIR does not exist."
    exit 1
fi
# Loop through all video files in $BASE_DIR (check that the mimetype is video)
for VIDEO_FILE in "$BASE_DIR"/*; do
    if file --mime-type "$VIDEO_FILE" | grep -q 'video/'; then
        SUBDIR="${VIDEO_FILE%.*}_generated"
        mkdir -p "$SUBDIR"
        OUTPUT_FILE="$SUBDIR/transcription.json"
        # Check if the flag file exists
        if [ ! -f "$OUTPUT_FILE" ]; then
            echo "Processing $SUBDIR..."
            if [ ! -f "$SUBDIR"/audio.wav ]; then
                set +e
                $DIRNAME/extract_audio.sh "$VIDEO_FILE" "$SUBDIR"/audio.wav
                set -e
                if [ $? -eq 32 ]; then
                    echo "No audio stream in $VIDEO_FILE, skipping"
                    continue
                fi
            fi
            # call the whisper server to obtain the transcription json output
            # and write that output to $BASENAME_generated/transcription.json
            BASENAME=$(basename "$SUBDIR")
            # Call the Whisper server
            if ! curl -X POST http://localhost:4000/ -F "file=@$SUBDIR/audio.wav" > "$OUTPUT_FILE"; then
                echo "Error : Failed to obtain transcription for $SUBDIR/audio.wav. Skipping..."
                continue
            fi
            echo "Finished processing $SUBDIR."
        else
            echo "Skipping $SUBDIR: already processed."
        fi
    fi
done
