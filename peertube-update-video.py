#!/usr/bin/env python3

import requests
import json
import os
import csv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration from .env
PEERTUBE_BASE_URL = os.getenv("PEERTUBE_URL")
TOKEN_FILE = os.getenv("PEERTUBE_TOKEN_FILE", "peertube_token.json")
CSV_FILE = "map_uuid_filename.csv"
BASE_DIR = "/media/Videos"

def load_token():
    """Load the token data from a file if it exists."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as token_file:
            return json.load(token_file)
    return None

def update_video_metadata(uuid, name, description, tags):
    """Update the metadata of a specific video on PeerTube."""
    token_data = load_token()
    if not token_data:
        print("Error: No token found. Please authenticate first.")
        return

    headers = {
        "Authorization": f"Bearer {token_data['access_token']}",
        "Content-Type": "application/json"
    }

    data = {
        "name": name,
        "description": description,
        "tags": tags[0:5]  # Limit to the first 5 tags
    }

    response = requests.put(f"{PEERTUBE_BASE_URL}/api/v1/videos/{uuid}", headers=headers, json=data)
    print(response.text)
    response.raise_for_status()
    return response

def process_csv_and_update_metadata(csv_file, base_dir):
    """Iterate through the CSV file and update video metadata based on JSON files."""
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        next(reader, None)  # skip the headers
        for row in reader:
            if len(row) != 2:
                print(f"Skipping invalid row: {row}")
                continue

            uuid, filename = row
            filename_without_ext = os.path.splitext(filename)[0]
            json_path = os.path.join(base_dir, f"{filename_without_ext}_generated/generate_image_descriptions.response.json")

            # Check if the JSON file exists
            if not os.path.exists(json_path):
                print(f"JSON file not found for {filename}: {json_path}")
                continue

            # Load the JSON file
            try:
                with open(json_path, "r") as json_file:
                    data = json.load(json_file)
            except Exception as e:
                print(f"Error reading JSON file {json_path}: {e}")
                continue

            # Extract fields from the JSON
            suggested_title = data.get("suggested_title")
            detailed_description = data.get("detailed_description")
            relevant_keywords = data.get("relevant_keywords")

            # Update metadata on PeerTube
            print(f"Updating metadata for video UUID {uuid}...")
            try:
                updated_video = update_video_metadata(uuid, suggested_title, detailed_description, relevant_keywords)
                print(f"Successfully updated video UUID {uuid}:")
            except requests.exceptions.RequestException as e:
                print(f"Error updating video UUID {uuid}: {e}")
                raise

def main():
    if not os.path.exists(CSV_FILE):
        print(f"Error: CSV file {CSV_FILE} not found.")
        exit(1)

    print("Processing CSV file and updating video metadata...")
    process_csv_and_update_metadata(CSV_FILE, BASE_DIR)

if __name__ == "__main__":
    if not PEERTUBE_BASE_URL:
        print("Error: Missing PEERTUBE_URL in the .env file.")
        exit(1)
    main()
