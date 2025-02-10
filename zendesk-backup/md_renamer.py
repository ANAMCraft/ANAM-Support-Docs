"""
This script will rename all Jekyll markdown files with the title of the page, to allow for easier managment instad of filenames of just the timecode.
"""

import os
import yaml
import re

# The directory to scan for the .md files
directory = "../articles/"

def hyphenate_title(title):
    """Convert a title to a lowercase hyphenated format."""
    # Remove any characters that are not alphanumeric or spaces
    title = re.sub(r'[^a-zA-Z0-9\s]', '', title)
    # Replace spaces with hyphens and convert to lowercase
    return '-'.join(title.lower().split())

def get_title_from_file(file_path):
    """Extract the title from the Markdown file's front matter."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Try to extract the front matter
    try:
        front_matter = yaml.safe_load(content.split('---')[1])  # Load YAML between ---
        return front_matter.get('title', None)
    except Exception as e:
        print(f"Error reading front matter from {file_path}: {e}")
        return None

def rename_markdown_files(directory):
    """Scan a directory for Markdown files and rename them based on their title."""
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            file_path = os.path.join(directory, filename)
            title = get_title_from_file(file_path)
            if title:
                new_filename = hyphenate_title(title) + '.md'
                new_file_path = os.path.join(directory, new_filename)
                if file_path != new_file_path:  # Only rename if the names are different
                    os.rename(file_path, new_file_path)
                    print(f'Renamed: {filename} -> {new_filename}')
                else:
                    print(f'Skipped renaming {filename}, because the new name is the same.')

if __name__ == "__main__":
    rename_markdown_files(directory)