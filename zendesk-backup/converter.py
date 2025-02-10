"""
This script will convert Zendesk html articles into Jekyll format using OpenAI GPT4o-Mini
"""

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Initialize OpenAI with your API key

def convert_html_to_jekyll_markdown(html_content, design_template):
    prompt = [{"role": "user", "content": f"Convert this HTML content to Jekyll markdown using the following design template. NOTE: Not all sections of the template will be used in each article, use your judgment to determine what sections are applicable for each article:\n\nHTML:\n{html_content}\n\nDesign Template:\n{design_template}\n\nJekyll Markdown:"}]

    response = client.chat.completions.create(model="gpt-4o-mini",  # You can use a different engine
    messages=prompt,
    max_tokens=5500,  # Adjust token limits as needed
    temperature=0.5,
    stream=False)

    markdown_content = response.choices[0].message.content.strip()
    print(markdown_content) 
    return markdown_content

def process_directory(directory_path, design_template, test_mode: bool = False):
    for filename in os.listdir(directory_path):
        if filename.endswith(".html"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            markdown_content = convert_html_to_jekyll_markdown(html_content, design_template)

            output_filename = filename.replace('.html', '.md')
            output_path = os.path.join(directory_path, output_filename)

            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(markdown_content)
            print(f"Converted {filename} to {output_filename}")

            if test_mode:
                break

# Define your design template here
design_template = """
# Jekyll Design Template Example
---
layout: default
title: "Article Title"
description: "A brief description of the article"
category: "Support Center"
tags: ["support", "faq", "article"]
parent: "Buyers|Vendors (depending on the tag used)"
---

# {{ page.title }}

## Introduction

This section provides a brief introduction to the topic discussed in this article.

## Table of Contents
1. [Section 1](#section-1)
2. [Section 2](#section-2)
3. [Section 3](#section-3)

## Section 1

### Subsection 1.1

Detailed information about this subsection. Include steps to take, examples, or screenshots if necessary.

### Subsection 1.2

Further details or additional tips related to Section 1.

## Section 2

Detailed explanation about this section. Discuss key points and provide actionable information for the readers.

### Common Issues in Section 2

- Issue 1: Description of issue and potential solutions.
- Issue 2: Description of issue and potential solutions.

## Section 3

Here you can discuss further topics. Provide insights or problem-solving strategies related to your support center article.

## Conclusion

Summarize the key takeaways from this article and provide any additional resources or links if applicable.

## Frequently Asked Questions (FAQ)

- **Q: What is the first question?**  
  **A:** Answer to the first question.
---

For more articles, visit our [Support Center](https://support.anamcraft.com).

### Instructions for Use (do NOT include in final files, for template instruction only):
#1. Do NOT wrap the output in a markdown block, just write the markdown
#2. Replace `"Article Title"` and the `description` with the appropriate title and description of your article.
#3. Fill in the sections (e.g., Section 1, Section 2) with relevant content.
#4. Update the FAQ section with common questions and answers pertinent to your article.
#5. If there is another article or page mentioned, be sure to link that article.
#6. In the tags, determine if this article is for vendors on ANAM Craft or this article is for buyers on ANAM Craft. Set the buyer/vendor tag accordingly.
#7. In the header, determine the parent/grandparent
#7. Important Links/Info:
#  - Support center - https://support.anamcraft.com
#  - Support email - support@anamcraft.com
#  - Main ANAM Craft website - https://anamcraft.com
"""

# Set the directory path where your HTML files are located
directory_path = './2025-02-07/en-us/'

# Process the directory
process_directory(directory_path, design_template)