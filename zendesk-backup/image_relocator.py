"""
This script will find all images within Jekyll Markdown that are hosted on a web server. Download each file, then update the markdown with the new local file location.
"""

import os
import re
import requests
import magic  # use python-magic to detect file types


# Set the input directory (directory containing markdown files)
input_directory = './converted_articles/'
# Set the output directory (where images will be saved)
output_directory = '../images'

# Create output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Markdown image link regex pattern
image_pattern = re.compile(r'!\[.*?\]\((.*?)\)')

def download_image(url, output_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error on bad request
        
        # Detect the MIME type using the magic library
        mime = magic.Magic(mime=True)
        mime_type = mime.from_buffer(response.content)
        
        # Map MIME type to file extension
        ext_mapping = {
            'image/jpeg': '.jpg',
            'image/png': '.png',
            'image/gif': '.gif',
            'image/webp': '.webp',
            # Add more mappings if needed
        }
        
        # Determine the appropriate extension
        extension = ext_mapping.get(mime_type, '')
        
        if not extension:
            print(f"Unsupported image type for URL: {url}")
            return False

        # Construct the full output path with the extension
        output_path_with_ext = output_path + extension
        
        # Save the image to the designated directory
        with open(output_path_with_ext, 'wb') as f:
            f.write(response.content)
        
        return output_path_with_ext  # Return the path with the extension for updating markdown
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def process_markdown_file(md_file_path):
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all image links
    image_links = image_pattern.findall(content)

    for image_link in image_links:
        # Check if it's an absolute URL
        if image_link.startswith('http://') or image_link.startswith('https://'):
            # Get a base output name (could use any naming pattern here)
            filename = os.path.basename(image_link).split('.')[0]  # Use the name before any extension
            image_output_path = os.path.join(output_directory, filename)
            
            # Download the image and get the new path with extension if successful
            new_image_path = download_image(image_link, image_output_path)
            if new_image_path:
                # Replace the original link with the relative path to the saved image with the appropriate extension
                content = content.replace(image_link, f'/images/{os.path.basename(new_image_path)}')

    # Write the updated content back to the markdown file
    with open(md_file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    # Loop through all Markdown files in the input directory
    for root, _, files in os.walk(input_directory):
        for filename in files:
            if filename.endswith('.md'):
                md_file_path = os.path.join(root, filename)
                print(f'Processing {md_file_path}...')
                process_markdown_file(md_file_path)

if __name__ == '__main__':
    main()