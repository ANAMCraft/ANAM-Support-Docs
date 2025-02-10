"""
This script will download all Zendesk 'Guide' articles into HTML.
"""

import os
import datetime
import csv

import requests

ZENDESK_API_TOKEN = os.getenv('ZENDESK_API_TOKEN') 
ZENDESK_USER_EMAIL = 'Support@anamcraft.com'
ZENDESK_SUBDOMAIN = 'https://anamcraft.zendesk.com/'
language = 'en-us'

date = datetime.date.today()
backup_path = os.path.join(str(date), language)
if not os.path.exists(backup_path):
    os.makedirs(backup_path)

log = []

credentials = f'{ZENDESK_USER_EMAIL}/token', ZENDESK_API_TOKEN

endpoint = f'{ZENDESK_SUBDOMAIN}/api/v2/help_center/{language.lower()}/articles.json'
while endpoint:
    response = requests.get(endpoint, auth=credentials)
    if response.status_code != 200:
        print(f'Failed to retrieve articles with error {response.status_code}')
        exit()
    data = response.json()

    for article in data['articles']:
        if article['body'] is None:
            continue
        title = '<h1>' + article['title'] + '</h1>'
        filename = f'{article["id"]}.html'
        with open(os.path.join(backup_path, filename), mode='w', encoding='utf-8') as f:
            f.write(title + '\n' + article['body'])
        print(f'{article["id"]} copied!')

        log.append((filename, article['title'], article['author_id']))

    endpoint = data.get('next_page', None)

with open(os.path.join(backup_path, '_log.csv'), mode='wt', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(('File', 'Title', 'Author ID'))
    for article in log:
        writer.writerow(article)