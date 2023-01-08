from bs4 import BeautifulSoup
from youtube_dl import YoutubeDL
import requests
import json
import re
import os
import sys


# Some setup stuff
url = "https://www.youtube.com/playlist?list=PLHTo__bpnlYWTUomlfikb6UC3VUsZVMgU"
yt_prefix = 'http://www.youtube.com'
# Send Request and parse
req = requests.get(url)
soup = BeautifulSoup(req.content, "html.parser")

# Get title tag and make Dir
title_tag = soup.find('title')
dir_title = title_tag.text
directory = f'{dir_title}'
if not os.path.exists(directory):
    os.makedirs(directory)
    print("FoLDer made")


# Get JSON data from page
json_data = None
for script in soup.find_all('script'):
    if script.text.strip().startswith('var ytInitialData = '):
        json_data = script.text.strip()[len('var ytInitialData = '):-1]
if json_data:
    data = json.loads(json_data)

# Add anything assigned to urls in JSON
links = []
def find_urls(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "url":
                #print("Link Found")
                links.append(value)
            else:
                find_urls(value)
    elif isinstance(data, list):
            for item in data:
                find_urls(item)

find_urls(data)
#print(f'Links: {links}')

# Check for correct links startswith: /watch endswith: index=[no.]
vid_links = []
for link in links:
    if link.startswith('/watch'):
        if re.search(r"&index=\d+", link):
            vid_links.append(yt_prefix+link)
        else:
            continue 
    else:
        continue
#print(f'VIDEO URLS: {vid_links}')
print(f'{len(vid_links)} links found')

# Download each link!
aud_download = YoutubeDL({'format':'bestaudio/best',  
                        'outtmpl': f'{dir_title}/%(title)s.%(ext)s'
                        })

for l in vid_links:
    try:
        aud_download.extract_info(l)
        print(f"DOWNLOADED {l}")
    except Exception as e:
        print(f'Problem with downloader: {e}')


if __name__ == '__main__':
    sys.exit()





