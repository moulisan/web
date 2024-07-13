import os
import sys
from bs4 import BeautifulSoup

def find_links(html_file):
    """
    Identify and print all <a href> links in the given HTML file.
    
    Parameters:
    html_file (str): Path to the HTML file to be processed.
    """
    
    # Check if the file exists
    if not os.path.exists(html_file):
        print(f"File not found: {html_file}")
        return
    
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all <a> tags with href attributes
    a_tags = soup.find_all('a', href=True)
    
    # Print out all the href links
    for a in a_tags:
        print(a['href'])

if __name__ == "__main__":
    # Check if the correct number of arguments are provided
    if len(sys.argv) != 2:
        print("Usage: python find_links.py <path_to_html_file>")
        sys.exit(1)
    
    # Get the HTML file path from the command line arguments
    html_file = sys.argv[1]
    
    # Find and print all <a href> links in the HTML file
    find_links(html_file)
