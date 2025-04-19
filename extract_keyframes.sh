#!/bin/bash
# This script extracts keyframes from a video file and saves them as JPEG images.
# Usage: ./extract_keyframes.sh filenames

set -euo pipefail

# Loop through all provided filenames
for filename in "$@"; do
    # Check if the file exists and is a regular file
    if [ ! -f "$filename" ]; then
        continue
    fi

    # Check if the file is a video file (optional)
    mimetype=`file -b -i "$filename"`
    if [[ $mimetype != video* ]]; then
        continue
    fi

    # Extract the base name of the file (without extension, whatever it is)
    base_name="${filename%.*}"

    # Create a directory for the generated
    OUTPUT_DIR="${base_name}_generated"
    mkdir -p "$OUTPUT_DIR"

    FLAG="$OUTPUT_DIR/thumbnails.flag"
    # Check if the flag file already exists
    if [ -f "$FLAG" ]; then
        echo "Thumbnails already generated for $filename"
        continue
    fi

    # Extract keyframes and save them as JPEG images in the created directory
    if ffmpeg -loglevel error -skip_frame nokey -i "$filename" -vsync 0 -f image2 -vf "select=eq(pict_type\,I),showinfo" -hide_banner - |
       awk '/showinfo/ {match($0, /pts_time:([0-9.]+)/, arr); if (arr[1] != "") print arr[1]}' |
       while read -r timestamp; do
           formatted_time=$(printf "%06.2f" "$timestamp")
           ffmpeg -loglevel error -skip_frame nokey -i "$filename" -vsync 0 -f image2 -vf "select=eq(pict_type\,I)" -frames:v 1 "$OUTPUT_DIR/thumbnail-${formatted_time}.jpeg" -ss "$timestamp"
       done && touch "$FLAG"
    else
        echo "Failed to extract keyframes for $filename"
    fi
done
