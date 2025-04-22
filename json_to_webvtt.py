#!/usr/bin/env python3

import json
import os
import argparse

def format_timestamp(seconds):
    """Convert seconds to WebVTT timestamp format (hh:mm:ss.mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds):02}.{milliseconds:03}"

def json_to_webvtt(json_path, output_path):
    """Convert transcription.json to WebVTT format."""
    try:
        with open(json_path, "r") as json_file:
            data = json.load(json_file)
    except Exception as e:
        print(f"Error reading JSON file {json_path}: {e}")
        return

    if "segments" not in data:
        print(f"Error: No 'segments' key found in {json_path}")
        return

    try:
        with open(output_path, "w") as vtt_file:
            # Write WebVTT header
            vtt_file.write("WEBVTT\n\n")

            # Write each segment
            for segment in data["segments"]:
                start = format_timestamp(segment["start"])
                end = format_timestamp(segment["end"])
                text = segment["text"].strip()

                vtt_file.write(f"{start} --> {end}\n{text}\n\n")

        print(f"WebVTT file created: {output_path}")
    except Exception as e:
        print(f"Error writing WebVTT file {output_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Convert a JSON transcription file to WebVTT format.")
    parser.add_argument("json_path", help="Path to the input JSON file")
    parser.add_argument("output_path", help="Path to the output WebVTT file")
    args = parser.parse_args()

    # Convert JSON to WebVTT
    json_to_webvtt(args.json_path, args.output_path)

if __name__ == "__main__":
    main()
