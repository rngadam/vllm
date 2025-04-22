#!/usr/bin/env python3

import os
import json
import csv
from glob import glob

# Paths
BASE_DIR = "/media/Videos"
OUTPUT_CSV = "video_durations.csv"

def extract_durations_from_json(json_path):
    """Extract duration-related keys from a JSON file."""
    try:
        with open(json_path, "r") as json_file:
            data = json.load(json_file)
            return {
                "filename": os.path.basename(os.path.dirname(json_path)).replace("_generated", ""),
                "eval_duration": data.get("eval_duration", 0),
                "load_duration": data.get("load_duration", 0),
                "prompt_eval_duration": data.get("prompt_eval_duration", 0),
                "total_duration": data.get("total_duration", 0)
            }
    except Exception as e:
        print(f"Error reading JSON file {json_path}: {e}")
        return None

def collect_durations(base_dir, output_csv):
    """Collect durations from all JSON files and save them to a CSV file."""
    # Find all JSON files in *_generated directories
    json_files = glob(os.path.join(base_dir, "*_generated/generate_image_descriptions.json"))

    # Prepare CSV file
    with open(output_csv, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["filename", "eval_duration", "load_duration", "prompt_eval_duration", "total_duration"])
        writer.writeheader()

        # Process each JSON file
        for json_path in json_files:
            durations = extract_durations_from_json(json_path)
            if durations:
                writer.writerow(durations)

    print(f"Durations collected and saved to {output_csv}")

def main():
    collect_durations(BASE_DIR, OUTPUT_CSV)

if __name__ == "__main__":
    main()
