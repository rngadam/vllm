#!/usr/bin/env python3

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration from .env
PEERTUBE_BASE_URL = os.getenv("PEERTUBE_URL")
TOKEN_FILE = os.getenv("PEERTUBE_TOKEN_FILE", "peertube_token.json")

def load_token():
    """Load the token data from a file if it exists."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as token_file:
            return json.load(token_file)
    return None

def get_videos(params=None):
    """Fetch a list of videos for the authenticated user."""
    token_data = load_token()
    if not token_data:
        print("Error: No token found. Please authenticate first.")
        return

    headers = {
        "Authorization": f"Bearer {token_data['access_token']}"
    }

    # Default query parameters
    default_params = {
        "count": 15,  # Number of items to return
        "sort": "-publishedAt",  # Sort by publication date in descending order
    }

    # Merge default parameters with user-provided parameters
    if params:
        default_params.update(params)

    response = requests.get(f"{PEERTUBE_BASE_URL}/api/v1/videos", headers=headers, params=default_params)
    response.raise_for_status()
    return response.json()

def main():
    print("Fetching videos...")
    try:
        # Example: Fetch the first 10 videos sorted by views
        params = {
            "count": 10,
            "isLocal": True,
            "search": "IMG_6356.MOV"
        }
        videos = get_videos(params)

        # Print the list of videos
        print(json.dumps(videos, indent=4))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching videos: {e}")

if __name__ == "__main__":
    if not PEERTUBE_BASE_URL:
        print("Error: Missing PEERTUBE_URL in the .env file.")
        exit(1)
    main()
