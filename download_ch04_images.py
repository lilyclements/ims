#!/usr/bin/env python3
"""
Download Chapter 4 Exercise Images

This script downloads the required images for Chapter 4 exercises from GitHub.
"""

import urllib.request
import os
import sys

# Image URLs and filenames
IMAGES = {
    '04-ex-q1-antibiotic-conditions.png': 'https://github.com/user-attachments/assets/c7d22aad-bb23-4c90-b26d-4c50c81c00e6',
    '04-ex-q3-george-floyd-protests.png': 'https://github.com/user-attachments/assets/40efecfa-6d65-4d50-9989-1086df91dc42',
    '04-ex-q7-meat-life-expectancy.png': 'https://github.com/user-attachments/assets/cd16fad0-5190-4c28-aa96-f4f62c7049ae'
}

def download_images():
    """Download all required images."""
    # Change to the exercises/images directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, 'exercises', 'images')
    
    if not os.path.exists(images_dir):
        print(f"Error: Directory not found: {images_dir}")
        print("Make sure you're running this script from the repository root.")
        sys.exit(1)
    
    os.chdir(images_dir)
    print(f"Downloading images to: {images_dir}")
    print("-" * 60)
    
    success_count = 0
    failed_count = 0
    
    for filename, url in IMAGES.items():
        try:
            print(f"Downloading {filename}...")
            urllib.request.urlretrieve(url, filename)
            file_size = os.path.getsize(filename)
            print(f"  ✓ Success: {filename} ({file_size:,} bytes)")
            success_count += 1
        except Exception as e:
            print(f"  ✗ Failed: {filename}")
            print(f"    Error: {e}")
            failed_count += 1
    
    print("-" * 60)
    print(f"Download complete!")
    print(f"  Success: {success_count}/{len(IMAGES)}")
    print(f"  Failed: {failed_count}/{len(IMAGES)}")
    
    if failed_count > 0:
        print("\nPlease try downloading the failed images manually:")
        print("See exercises/images/README_CH04_IMAGES.md for instructions.")
        sys.exit(1)

if __name__ == '__main__':
    download_images()
