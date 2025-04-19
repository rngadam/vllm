#!/bin/bash

# Using ffmpeg, extract audio track only from a video file
# Usage: ./extract_audio.sh input_video.mp4 output_audio.mp3
# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 input_video output_audio"
    exit 1
fi
# Assign input arguments to variables
input_video="$1"
output_audio="$2"
# Check if the input video file exists
if [ ! -f "$input_video" ]; then
    echo "Error: Input video file '$input_video' not found!"
    exit 1
fi
# Check if the input video contains an audio stream
if ! ffprobe -loglevel error -show_streams -select_streams a "$input_video" | grep -q "codec_type=audio"; then
    echo "Error: No audio stream found in '$input_video'!"
    exit 32
fi
# Use ffmpeg to extract the audio track from the video file
ffmpeg -loglevel error -i "$input_video" -q:a 0 -map a "$output_audio"
# Check if the ffmpeg command was successful
ERRCODE=$?
if [ $ERRCODE -eq 0 ]; then
    echo "Audio extracted successfully to '$output_audio'"
else
    echo "Error $ERRCODE: Failed to extract audio from '$input_video'"
    exit 1
fi
