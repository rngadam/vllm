#!/bin/bash
# This script processes every subdirectory ending with "_generated" in the directory passed as an argument.
# Using json_to_webvtt.py, it converts the transcription.json file to webvtt format
# and saves it as "transcription.vtt" in the same subdirectory.

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
# Loop through all subdirectories ending with "_generated"
for SUBDIR in "$BASE_DIR"/*_generated; do
    if [ -d "$SUBDIR" ]; then
        TRANSCRIPTION_FILE="$SUBDIR/transcription.json"
        OUTPUT_FILE="$SUBDIR/transcription.vtt"
        # Check if the transcription.json file exists
        if [ -f "$TRANSCRIPTION_FILE" ]; then
            # Run the json_to_webvtt.py script
            if [ ! -f "$OUTPUT_FILE" ]; then
                echo "Converting $TRANSCRIPTION_FILE to $OUTPUT_FILE"
                python3 "$DIRNAME/json_to_webvtt.py" "$TRANSCRIPTION_FILE" "$OUTPUT_FILE"
            else
                echo "Warning: $OUTPUT_FILE already exists. Skipping conversion."
                continue
            fi
        else
            echo "Warning: $TRANSCRIPTION_FILE does not exist in $SUBDIR. Skipping."
        fi
    else
        echo "Warning: $SUBDIR is not a directory. Skipping."
    fi
done
