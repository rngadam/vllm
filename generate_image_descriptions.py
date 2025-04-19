#!/usr/bin/env python3
import base64
import json
import requests
import sys

def encode_images_to_base64(image_paths):
    """Encode a list of image paths to base64 strings."""
    images_base64 = []
    for image_path in image_paths:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            image_base64 = base64.b64encode(image_data).decode("utf-8")
            images_base64.append(image_base64)
    return images_base64

def create_payload(images_base64):
    """Create the JSON payload for the API request."""
    with open("generate_image_descriptions.md", "r", encoding="utf-8") as file:
        prompt = file.read()
    return {
        "model": "gemma3:27b-it-q8_0",
        "prompt": prompt,
        "stream": False,
        "images": images_base64
    }

def send_request(payload):
    """Send the API request with the given payload."""
    url = "http://localhost:11434/api/generate"
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    return response.text

def process(image_paths):
    """Main function to process images and send the request."""
    # Encode images to base64
    images_base64 = encode_images_to_base64(image_paths)

    # Create the JSON payload
    payload = create_payload(images_base64)

    # Send the request and print the response
    response = send_request(payload)
    return response

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python multimodal.py <image_path1> <image_path2> ...")
        sys.exit(1)

    output_json_path = sys.argv[1]
    image_paths = sys.argv[2:]
    print(image_paths)
    response = process(image_paths)
    with open(output_json_path, "w") as output_file:
        output_file.write(response)
        #json.dump(response, output_file, indent=4)
