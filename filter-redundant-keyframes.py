#!/usr/bin/env python3

# This script compares images in filename order and removes redundant images
# based on perceptual similarity. Only the first unique image in a sequence
# of perceptually similar images is kept.

from PIL import Image
import imagehash
import os
import sys

def calculate_phash(image_path):
    """Calculate the perceptual hash (phash) of an image."""
    try:
        image = Image.open(image_path)
        return imagehash.phash(image)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def filter_unique_images(image_paths, threshold=10):
    """Filter images, keeping only the first unique image in a sequence."""
    unique_images = []
    last_unique_hash = None

    for image_path in image_paths:
        phash = calculate_phash(image_path)
        if phash is None:
            continue

        # Compare with the last unique hash
        if last_unique_hash is None or (phash - last_unique_hash) > threshold:
            unique_images.append(image_path)
            last_unique_hash = phash
        else:
            # Remove redundant image
            try:
                os.remove(image_path)
                print(f"Removed redundant image: {image_path}")
            except Exception as e:
                print(f"Failed to remove {image_path}: {e}")

    return unique_images

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python filter-redundant-keyframes.py <image1_path> <image2_path> ...")
        sys.exit(1)

    # Sort image paths by filename to ensure sequential processing
    image_paths = sorted(sys.argv[1:])
    unique_images = filter_unique_images(image_paths)

    print("Unique images kept:")
    for image in unique_images:
        print(image)
