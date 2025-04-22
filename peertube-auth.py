#!/usr/bin/env python3

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration from .env
PEERTUBE_BASE_URL = os.getenv("PEERTUBE_URL")
USERNAME = os.getenv("PEERTUBE_USERNAME")
PASSWORD = os.getenv("PEERTUBE_PASSWORD")
TOKEN_FILE = os.getenv("PEERTUBE_TOKEN_FILE", "peertube_token.json")

def get_client_credentials():
    """Fetch client credentials from the PeerTube instance."""
    response = requests.get(f"{PEERTUBE_BASE_URL}/api/v1/oauth-clients/local")
    response.raise_for_status()
    return response.json()

def get_user_token(client_id, client_secret):
    """Fetch the user token using client credentials and user credentials."""
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "password",
        "response_type": "code",
        "username": USERNAME,
        "password": PASSWORD
    }
    response = requests.post(f"{PEERTUBE_BASE_URL}/api/v1/users/token", data=data)
    response.raise_for_status()
    return response.json()

def save_token(token_data):
    """Save the token data to a file."""
    with open(TOKEN_FILE, "w") as token_file:
        json.dump(token_data, token_file)
    print(f"Token saved to {TOKEN_FILE}")

def load_token():
    """Load the token data from a file if it exists and check its expiration."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as token_file:
            token_data = json.load(token_file)

        # Check if the token has expired
        file_timestamp = os.path.getmtime(TOKEN_FILE)
        expires_in = token_data.get("expires_in", 0)
        if (file_timestamp + expires_in) > os.path.getmtime(TOKEN_FILE):
            return token_data
        else:
            print("Token has expired.")
            return None
    return None

def main():
    # Check if a token already exists
    token_data = load_token()
    if token_data:
        print("Token already exists:")
        print(json.dumps(token_data, indent=4))
        return

    # Fetch client credentials
    print("Fetching client credentials...")
    client_credentials = get_client_credentials()
    client_id = client_credentials["client_id"]
    client_secret = client_credentials["client_secret"]

    # Fetch user token
    print("Fetching user token...")
    token_data = get_user_token(client_id, client_secret)

    # Save the token
    save_token(token_data)

if __name__ == "__main__":
    if not PEERTUBE_BASE_URL or not USERNAME or not PASSWORD:
        print("Error: Missing required environment variables. Check your .env file.")
        exit(1)
    main()
