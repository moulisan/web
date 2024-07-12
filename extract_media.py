import os
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Define paths
export_file = 'gcmoulicom.WordPress.2024-07-05.xml'  # Replace with the path to your XML export file
media_output_path = 'media'

# Create media output directory if it doesn't exist
if not os.path.exists(media_output_path):
    os.makedirs(media_output_path)

def parse_export_file(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return root
    except ET.ParseError as e:
        print(f"Failed to parse XML file: {e}")
        return None

def extract_media_urls(content):
    if not content:
        return []
    soup = BeautifulSoup(content, 'html.parser')
    media_urls = []

    # Extract all img tags
    for img in soup.find_all('img'):
        media_urls.append(img['src'])

    return media_urls

def download_media(url, save_directory):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        filepath = os.path.join(save_directory, filename)
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return filename
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return None

def process_posts(root):
    if root is None:
        print("No XML root found. Exiting.")
        return
    
    for item in root.findall('.//item'):
        title = item.find('title').text if item.find('title') is not None else 'Untitled'
        content = item.find('{http://purl.org/rss/1.0/modules/content/}encoded')
        content = content.text if content is not None else None
        
        if content is None:
            print(f"Skipping post '{title}' because it has no content.")
            continue
        
        print(f"Processing post: {title}")

        # Extract and download media
        media_urls = extract_media_urls(content)
        for url in media_urls:
            print(f"Downloading media: {url}")
            download_media(url, media_output_path)

if __name__ == "__main__":
    root = parse_export_file(export_file)
    process_posts(root)
    print("Media download process completed.")

