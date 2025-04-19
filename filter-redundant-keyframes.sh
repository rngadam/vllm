#!/bin/bash
# filepath: /workspaces/vllm/filter-redundant-keyframes.sh

# This script processes every subdirectory ending with "_generated" in the directory passed as an argument.
# If the subdirectory does NOT contain a file named "filtered-thumbnail.flag",
# it runs the `filter-redundant-keyframes.py` script on all "thumbnail-*.jpeg" files in that subdirectory
# and then creates the "filtered-thumbnail.flag" file.

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
        FLAG_FILE="$SUBDIR/filtered-thumbnail.flag"

        # Check if the flag file exists
        if [ ! -f "$FLAG_FILE" ]; then
            echo "Processing $SUBDIR..."

            # Run the Python script on all "thumbnail-*.jpeg" files in the subdirectory
            $DIRNAME/filter-redundant-keyframes.py "$SUBDIR"/thumbnail-*.jpeg

            # Create the flag file to mark the directory as processed
            touch "$FLAG_FILE"
            echo "Finished processing $SUBDIR."
        else
            echo "Skipping $SUBDIR: already processed."
        fi
    fi
done
