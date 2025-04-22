#!/usr/bin/env python3

import requests
import os
import csv
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration from .env
PEERTUBE_BASE_URL = os.getenv("PEERTUBE_URL")
TOKEN_FILE = os.getenv("PEERTUBE_TOKEN_FILE")
CSV_FILE = "map_uuid_filename.csv"
BASE_DIR = "/media/Videos"

def load_token():
    """Load the token data from a file if it exists."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as token_file:
            return json.load(token_file)
    return None

def extract_language_from_json(json_path):
    """Extract the language field from transcription.json if it exists."""
    if not os.path.exists(json_path):
        return "en"  # Default to English if no JSON file exists
    try:
        with open(json_path, "r") as json_file:
            data = json.load(json_file)
            return data.get("language", "en")  # Default to English if language is missing
    except Exception as e:
        print(f"Error reading JSON file {json_path}: {e}")
        return "en"

def upload_caption(uuid, caption_path, language="en"):
    """Upload a caption file to a specific video on PeerTube."""
    token_data = load_token()
    if not token_data:
        print("Error: No token found. Please authenticate first.")
        return

    headers = {
        "Authorization": f"Bearer {token_data['access_token']}"
    }

    with open(caption_path, "rb") as caption_file:
        files = {
            "captionfile": (os.path.basename(caption_path), caption_file)
        }

        response = requests.put(f"{PEERTUBE_BASE_URL}/api/v1/videos/{uuid}/captions/{language}", headers=headers, files=files)
        if response.status_code == 204:
            print(f"Successfully uploaded caption for video UUID {uuid}")
        else:
            print(f"Error uploading caption for video UUID {uuid}: {response.status_code} {response.reason}")

def process_csv_and_upload_captions(csv_file, base_dir):
    """Iterate through the CSV file and upload captions based on VTT files."""
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        next(reader, None)  # skip the headers
        for row in reader:
            if len(row) != 2:
                print(f"Skipping invalid row: {row}")
                continue

            uuid, filename = row
            filename_without_ext = os.path.splitext(filename)[0]
            vtt_path = os.path.join(base_dir, f"{filename_without_ext}_generated/transcription.vtt")
            json_path = os.path.join(base_dir, f"{filename_without_ext}_generated/transcription.json")

            # Check if the VTT file exists
            if not os.path.exists(vtt_path):
                print(f"VTT file not found for {filename}: {vtt_path}")
                continue

            # Extract language from the JSON file
            language = extract_language_from_json(json_path)

            # Upload the caption
            print(f"Uploading caption for video UUID {uuid} from {vtt_path} with language '{language}'...")
            try:
                upload_caption(uuid, vtt_path, language)
            except Exception as e:
                print(f"Error uploading caption for video UUID {uuid}: {e}")

def main():
    if not os.path.exists(CSV_FILE):
        print(f"Error: CSV file {CSV_FILE} not found.")
        exit(1)

    print("Processing CSV file and uploading captions...")
    process_csv_and_upload_captions(CSV_FILE, BASE_DIR)

if __name__ == "__main__":
    if not PEERTUBE_BASE_URL:
        print("Error: Missing PEERTUBE_URL in the .env file.")
        exit(1)
    main()
