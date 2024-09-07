import os
from bs4 import BeautifulSoup

def extract_referenced_html_files(file_path):
    referenced_files = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.endswith('.html'):
                # Resolve relative paths
                referenced_file = os.path.normpath(os.path.join(os.path.dirname(file_path), href))
                referenced_files.add(referenced_file)
    return referenced_files

def check_html_references(html_files_list, search_folder):
    for file in os.listdir(search_folder):
        if file.endswith(".html"):
            file_path = os.path.join(search_folder, file)
            is_referenced = False
            for html_file in html_files_list:
                referenced_files = extract_referenced_html_files(html_file)
                if file_path in referenced_files:
                    is_referenced = True
                    break
            if not is_referenced:
                print(f"File {file} not referenced in any of the html files")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python cleanUpUnreffedHTMLfiles.py <root_folder> <search_folder>")
        sys.exit(1)
    root_folder = sys.argv[1]
    search_folder = sys.argv[2]

    # Convert relative paths to absolute paths
    root_folder = os.path.abspath(root_folder)
    search_folder = os.path.abspath(search_folder)

    # List all HTML files in root_folder without going recursive into folders
    html_files_list = []
    for file in os.listdir(root_folder):
        if file.endswith(".html"):
            html_files_list.append(os.path.join(root_folder, file))

    check_html_references(html_files_list, search_folder)