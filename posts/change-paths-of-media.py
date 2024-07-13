import os
import sys
from bs4 import BeautifulSoup

def update_image_urls(html_file, media_folder):
    """
    Update image URLs in the given HTML file.
    
    Parameters:
    html_file (str): Path to the HTML file to be updated.
    media_folder (str): Path to the folder containing media files.
    """
    
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all image tags
    img_tags = soup.find_all('img')
    
    for img in img_tags:
        # Extract the original src attribute
        old_src = img.get('src')
        
        if old_src:
            # Extract the filename from the old src
            filename = os.path.basename(old_src)
            
            # Create the new src path
            new_src = os.path.join('..', 'media', filename)
            
            # Check if the file exists in the media folder
            if os.path.exists(os.path.join(media_folder, filename)):
                # Update the src attribute
                img['src'] = new_src
            else:
                # Remove the img tag if the file does not exist
                img.decompose()
    
    # Write the updated HTML back to the file
    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))

if __name__ == "__main__":
    # Check if the correct number of arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python update_image_urls.py <path_to_html_file> <path_to_media_folder>")
        sys.exit(1)
    
    # Get the HTML file and media folder path from the command line arguments
    html_file = sys.argv[1]
    media_folder = sys.argv[2]
    
    # Update the image URLs
    update_image_urls(html_file, media_folder)
