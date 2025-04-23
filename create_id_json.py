#!/usr/bin/env python3

import os
import csv
import json

# Configuration
CSV_FILE = "map_uuid_filename.csv"
BASE_DIR = "/media/Videos"

def create_id_json(base_dir, csv_file):
    """Create an id.json file in each video directory based on the CSV file."""
    if not os.path.exists(csv_file):
        print(f"Error: CSV file {csv_file} not found.")
        return

    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header row

        for row in reader:
            if len(row) != 2:
                print(f"Skipping invalid row: {row}")
                continue

            uuid, filename = row
            filename_without_ext = os.path.splitext(filename)[0]
            video_dir = os.path.join(base_dir, f"{filename_without_ext}_generated")

            # Ensure the directory exists
            if not os.path.exists(video_dir):
                print(f"Directory not found for {filename}: {video_dir}")
                continue

            # Create the id.json file
            id_json_path = os.path.join(video_dir, "id.json")
            id_data = {
                "uuid": uuid,
                "filename": filename
            }

            try:
                with open(id_json_path, "w") as json_file:
                    json.dump(id_data, json_file, indent=4)
                print(f"Created id.json for {filename} in {video_dir}")
            except Exception as e:
                print(f"Error writing id.json for {filename}: {e}")

def main():
    create_id_json(BASE_DIR, CSV_FILE)

if __name__ == "__main__":
    main()
