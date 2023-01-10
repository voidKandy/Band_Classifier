import sys
import os
import time
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui  import QIcon
from PyQt5.QtWidgets import QComboBox, QApplication, QFileDialog, QLabel, QPushButton, QWidget
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.io import wavfile
import librosa
import librosa.display

# Grab names of files in spec_graphs
print("Initializing")
existing_files = []
for root, dirs, files in os.walk('spec_graphs/'):
    for ef in files:
        name, extension = os.path.splitext(ef)
        mod_name = name + '.wav'
        existing_files.append(mod_name)
#print(existing_files)


# Widget init 
class mainwidget(QWidget):

    def __init__(self):
        super().__init__()
        self.title = '|SPECTROGRAPH|'
        self.initUI()
       
    # Window
    def initUI(self):
        self.setGeometry(1000,200,300,75)
        self.setWindowTitle(self.title)
    # Label
        self.label = QLabel("Select a sound file:")
    # Drop Down Band list
        self.bandselect = QComboBox(self)
        self.bandselect.addItem('voidkandy')
        self.bandselect.addItem('radiohead')
        self.bandselect.addItem('king_gizzard')
        self.bandselect.hide()
        self.bandselect.move(85,40)
    # Upload Button
        self.up_button = QPushButton("Choose Sounds", self)
        self.up_button.move(85,15)
        self.up_button.clicked.connect(self.upload_clck)
        self.show()
    # Specgraph Button
        self.spcg_button = QPushButton("Spectrographify", self)
        self.spcg_button.move(80,5)
        self.spcg_button.clicked.connect(self.spcg_clck)
        self.spcg_button.hide()
    # exit File Button
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.move(110,15)
        self.exit_button.clicked.connect(self.exit_clck)
        self.exit_button.hide()
        
    # Upload Clcked
    def upload_clck(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        # Assign sound_folder to a diretory
        self.sound_folder = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)
        # LIST COMPREHENSION                                             # Returns list of names of files in self.sound_folder
        self.sound_folder = [os.path.join(self.sound_folder, f) for f in os.listdir(self.sound_folder)]
        #print(self.sound_folder)
        self.up_button.hide()
        self.spcg_button.show()
        print("Folder Chosen")
        self.prex_checks = []
        for f in self.sound_folder: 
            file_name = os.path.basename(f)
            print(file_name)
            if file_name in existing_files:
                print(f'Removing {file_name}')
                continue
            else:
                print("Passed check")
                self.prex_checks.append(f)
        self.bandselect.show()


    # Spectrogram Clcked
    def spcg_clck(self):
        self.bandselect.hide()
        chosen_band = self.bandselect.currentText()
        for f in self.prex_checks:
        # Get file name
            file_name, file_ext = os.path.splitext(f)
            file_name = os.path.basename(f)
        # Skip files that are not audio files
            if file_ext not in ('.wav', '.mp3', '.flac', '.aac'):
                continue
            print(f'Iterating: {file_name}')
        # Open file with librosa
            x, sr = librosa.load(f)
            plt.figure(figsize=(14, 5))
            librosa.display.waveshow(x, sr=sr)
        # Short Time Fourier Transform
            X = librosa.stft(x)
        # Convert slices to amplitude
            Xdb = librosa.amplitude_to_db(abs(X))
        # Plot
            plt.figure(figsize=(14,5))
            librosa.display.specshow(Xdb, sr=sr)
        # Assign Variable for later and show next button
            self.img_plt = plt
            self.img_plt.savefig(f'../spec_graphs/{chosen_band}/{file_name}.png', transparent=True, bbox_inches='tight')
            self.img_plt.close()
            time.sleep(10)
        self.spcg_button.hide()
        self.exit_button.show()
        print("[Done]") 
    
    # Exit Clcked
    def exit_clck(self):

        sys.exit()



    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mainwidget()
    sys.exit(app.exec_())