from bs4 import BeautifulSoup
from youtube_dl import YoutubeDL
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QPushButton
import requests
import json
import re
import os
import sys


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

        self.exit_button = QPushButton("Exit", self)
        self.exit_button.move(60,55)
        self.exit_button.resize(200,32)
        self.exit_button.clicked.connect(self.exit_clck)
        self.exit_button.hide()

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
        counter = 0
        for l in vid_links:
            try:
                aud_download.extract_info(l)
                print(f"DOWNLOADED {l}")
                counter += 1
            except Exception as e:
                print(f'Problem with downloader: {e}')
        if counter == int(len(vid_links)):
            scraped = True
            print("[DONE]")
        if scraped is True:
            self.scrape_but.hide()
            self.url_in.hide()
            self.label.hide()
            self.exit_button.show()
            self.show()

        # Exit Clcked
    def exit_clck(self):
        sys.exit()


        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mainwidget()
    sys.exit(app.exec_())





