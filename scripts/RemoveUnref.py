# Simple python script to git rm a list of files that are present in a file given in command line
# Usage: python RemoveUnref.py <file_with_list_of_files>
import os
import sys
import subprocess

# Check if the file with list of files is given
if len(sys.argv) != 2:
    print("Usage: python RemoveUnref.py <file_with_list_of_files>")
    sys.exit(1)

# Read the file with list of files
file_with_list_of_files = sys.argv[1]
with open(file_with_list_of_files, 'r') as file:
    files_to_remove = file.readlines()
    # Remove the newline character from the end of each line
    files_to_remove = [file.strip() for file in files_to_remove]
    # print each file to be removed
    for file in files_to_remove:
        print(f"Removing file: {file}")
        # git rm the file
        subprocess.run(["git", "rm", file]) 

# Commit the changes
#subprocess.run(["git", "commit", "-m", "Remove unreferenced files"])



