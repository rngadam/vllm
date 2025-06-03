#!/usr/bin/env python3

import os
import json
import requests
from collections import defaultdict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration from .env
PEERTUBE_BASE_URL = os.getenv("PEERTUBE_URL")
TOKEN_FILE = os.getenv("PEERTUBE_TOKEN_FILE", "peertube_token.json")
BASE_DIR = "/media/Videos"
CHANNEL_ID = os.getenv("PEERTUBE_CHANNEL_ID")  # The channel ID where playlists will be created
PLAYLIST_SIZE_LOWERBOUND = int(os.getenv("PEERTUBE_PLAYLIST_SIZE_LOWERBOUND", 10))
PLAYLIST_SIZE_UPPERBOUND = int(os.getenv("PEERTUBE_PLAYLIST_SIZE_UPPERBOUND", 25))

def load_token():
    """Load the token data from a file if it exists."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as token_file:
            return json.load(token_file)
    return None

def create_playlist(name, description, privacy=3):
    """Create a new playlist on PeerTube."""
    token_data = load_token()
    if not token_data:
        print("Error: No token found. Please authenticate first.")
        return None

    headers = {
        "Authorization": f"Bearer {token_data['access_token']}"
    }

    data = {
        "displayName": name,
        "description": description,
        "privacy": privacy,
        "videoChannelId": CHANNEL_ID
    }

    response = requests.post(f"{PEERTUBE_BASE_URL}/api/v1/video-playlists", headers=headers, data=data)
    if response.status_code == 200:
        playlist = response.json()
        print(f"Successfully created playlist: {name} (ID: {playlist['videoPlaylist']['id']})")
        return playlist["videoPlaylist"]["id"]
    else:
        print(f"Error creating playlist {name}: {response.status_code} {response.text}")
        return None

def add_video_to_playlist(playlist_id, video_id):
    """Add a video to a playlist on PeerTube."""
    token_data = load_token()
    if not token_data:
        print("Error: No token found. Please authenticate first.")
        return

    headers = {
        "Authorization": f"Bearer {token_data['access_token']}",
        "Content-Type": "application/json"
    }

    data = {
        "videoId": video_id
    }

    response = requests.post(f"{PEERTUBE_BASE_URL}/api/v1/video-playlists/{playlist_id}/videos", headers=headers, json=data)
    if response.status_code == 200:
        print(f"Successfully added video ID {video_id} to playlist ID {playlist_id}")
    else:
        print(f"Error adding video ID {video_id} to playlist ID {playlist_id}: {response.status_code} {response.text}")

def get_video_id_from_directory(directory):
    """Read the video ID (uuid) from the id.json file in the directory."""
    id_json_path = os.path.join(directory, "id.json")
    if not os.path.exists(id_json_path):
        print(f"Warning: id.json not found in {directory}")
        return None

    try:
        with open(id_json_path, "r") as json_file:
            data = json.load(json_file)
            return data.get("uuid")
    except Exception as e:
        print(f"Error reading id.json in {directory}: {e}")
        return None

def cluster_videos_by_keywords(base_dir):
    """Cluster videos into groups based on their keywords."""
    clusters = defaultdict(list)

    # Iterate through all JSON files in the base directory
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith("generate_image_descriptions.response.json"):
                json_path = os.path.join(root, file)
                try:
                    with open(json_path, "r") as json_file:
                        data = json.load(json_file)
                        keywords = data.get("relevant_keywords", [])
                        video_id = get_video_id_from_directory(root)

                        if not video_id:
                            continue

                        # Add the video to clusters based on keywords
                        for keyword in keywords:
                            clusters[keyword].append(video_id)
                except Exception as e:
                    print(f"Error reading JSON file {json_path}: {e}")

    return clusters

def get_existing_playlists():
    """Retrieve all playlists for the channel."""
    token_data = load_token()
    if not token_data:
        print("Error: No token found. Please authenticate first.")
        return {}

    headers = {
        "Authorization": f"Bearer {token_data['access_token']}"
    }

    response = requests.get(f"{PEERTUBE_BASE_URL}/api/v1/video-channels/{CHANNEL_ID}/video-playlists", headers=headers)
    if response.status_code == 200:
        playlists = response.json().get("data", [])
        return {playlist["displayName"]: playlist["id"] for playlist in playlists}
    else:
        print(f"Error retrieving playlists: {response.status_code} {response.text}")
        return {}

def get_videos_in_playlist(playlist_id):
    """Retrieve all video IDs in a playlist."""
    token_data = load_token()
    if not token_data:
        print("Error: No token found. Please authenticate first.")
        return set()

    headers = {
        "Authorization": f"Bearer {token_data['access_token']}"
    }

    response = requests.get(f"{PEERTUBE_BASE_URL}/api/v1/video-playlists/{playlist_id}/videos", headers=headers)
    if response.status_code == 200:
        videos = response.json().get("data", [])
        return {video["id"] for video in videos}
    else:
        print(f"Error retrieving videos for playlist ID {playlist_id}: {response.status_code} {response.text}")
        return set()

def main():
    # Cluster videos by keywords
    print("Clustering videos by keywords...")
    clusters = cluster_videos_by_keywords(BASE_DIR)

    # Sort clusters by the number of videos in descending order
    sorted_clusters = sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True)

    # Filter clusters to include only those within the specified size range
    filtered_clusters = [(keyword, video_ids) for keyword, video_ids in sorted_clusters
                         if PLAYLIST_SIZE_LOWERBOUND <= len(video_ids) <= PLAYLIST_SIZE_UPPERBOUND]

    # Retrieve existing playlists
    existing_playlists = get_existing_playlists()

    # Create playlists and add videos
    for keyword, video_ids in filtered_clusters:
        print(f"Processing playlist for keyword: {keyword}")

        # Check if the playlist already exists
        if keyword in existing_playlists:
            playlist_id = existing_playlists[keyword]
            print(f"Playlist '{keyword}' already exists (ID: {playlist_id}).")
        else:
            # Create a new playlist
            playlist_id = create_playlist(name=keyword, description=f"Playlist for videos related to {keyword}")
            if not playlist_id:
                continue

        # Get existing videos in the playlist
        existing_videos = get_videos_in_playlist(playlist_id)

        # Add only videos that are not already in the playlist
        for video_id in video_ids:
            if video_id not in existing_videos:
                add_video_to_playlist(playlist_id, video_id)
            else:
                print(f"Video ID {video_id} is already in playlist '{keyword}' (ID: {playlist_id}).")

if __name__ == "__main__":
    if not PEERTUBE_BASE_URL or not CHANNEL_ID:
        print("Error: Missing PEERTUBE_URL or PEERTUBE_CHANNEL_ID in the .env file.")
        exit(1)
    main()
