from bs4 import BeautifulSoup
from youtube_dl import YoutubeDL
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QPushButton
import requests
import json
import re
import os
import sys
import time
import subprocess
import art
from colorama import *
from tqdm import tqdm

# Some setup stuff
class mainwidget(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'YouTube Playlist Scraper'
        self.initUI()    
    # Window
    def initUI(self):
        self.setGeometry(1000,200,320,140)
        self.setWindowTitle(self.title)
        self.label = QLabel(self)
        self.label.setText("Paste URL: ")
        self.url_in = QLineEdit(self)

        self.label.move(20,30)
        self.url_in.move(100,20)
        self.url_in.resize(175,32)

        self.scrape_but = QPushButton('Scrape',self)
        self.scrape_but.clicked.connect(self.scrape)
        self.scrape_but.resize(200,32)
        self.scrape_but.move(60,75)

        self.show()

    def scrape(self):
        self.hide()
        url = self.url_in.text() 
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

        if 'playlist?list' in url:
            link_mess=(f'Playlist with {len(vid_links)} links found')
            playlist = True

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
        else:
            link_mess = ('Video Found')
            playlist = False
        # Check for correct links startswith: /watch endswith: index=[no.]
        if playlist == True:
            vid_links = []
            for link in links:
                if link.startswith('/watch'):
                    if re.search(r"&index=\d+", link):
                        vid_links.append(yt_prefix+link)
                    else:
                        continue 
                else:
                    continue
        else: 
            vid_links = [url]
        #print(f'VIDEO URLS: {vid_links}')
        for letter in link_mess:
            print(Fore.GREEN+letter,end='') 
            time.sleep(.1)

        print(Fore.WHITE)

        # Download each link!
        # tell youtubeDL how to save the link
        aud_download = YoutubeDL({'format':'bestaudio/best',  
                                'outtmpl': f'{dir_title}/%(title)s.%(ext)s'
                                })
        counter = 0
        # Save those bitches
        for l in vid_links:
            try:
                aud_download.extract_info(l)
                print(f"DOWNLOADED {l}")
                f_name = aud_download.prepare_filename(aud_download.extract_info(l))
                print(f"Filename: {f_name}")
                # Change to wav files
                input_filename = os.path.join(f_name)
                output_filename = os.path.splitext(input_filename)[0] + '.wav'
                subprocess.run(['ffmpeg','-i', input_filename, output_filename])   
                counter += 1
            except Exception as e:
                print(f'Problem with downloader: {e}')
        if counter == int(len(vid_links)):
            scraped = True

        if scraped is True:
            self.scrape_but.hide()
            self.url_in.hide()
            self.label.hide()
            print("[CLEANING]")
            for file in os.listdir(dir_title):
                    if not file.endswith(".wav"):
                        os.remove(os.path.join(dir_title, file))
                        continue
                    special_chars = re.findall(r'[^A-Za-z0-9._-]', file)
                    if special_chars:
                        newname = re.sub(r'[^A-Za-z0-9._-]','',file)
                        os.rename(os.path.join(dir_title, file), os.path.join(dir_title, newname)) 
            print("[DONE]")          
            sys.exit()


        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mainwidget()
    sys.exit(app.exec_())





