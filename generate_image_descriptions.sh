 #!/bin/bash
 # for every subdirectory ending with "_generated" in the directory passed as an argument
    # if the subdirectory does NOT contain a file named "generate_image_descriptions.flag"
    # run the `generate_image_descriptions.py` script on all "thumbnail-*.jpeg" files in that subdirectory
# and then create the "generate_image_descriptions.flag" file.
#
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
        FLAG_FILE="$SUBDIR/generate_image_descriptions.flag"
        # Check if the flag file exists
        if [ ! -f "$FLAG_FILE" ]; then
            echo "Processing $SUBDIR..."
            # Run the Python script on all "thumbnail-*.jpeg" files in the subdirectory
            $DIRNAME/generate_image_descriptions.py "$SUBDIR"/generate_image_descriptions.json "$SUBDIR"/thumbnail-*.jpeg
            # Create the flag file to mark the directory as processed
            touch "$FLAG_FILE"
            echo "Finished processing $SUBDIR."
        else
            echo "Skipping $SUBDIR: already processed."
        fi
    fi
done
