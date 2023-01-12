import sys
import os
import time
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui  import QIcon
from PyQt5.QtWidgets import QBoxLayout, QLineEdit, QComboBox, QDialog, QApplication, QFileDialog, QLabel, QPushButton, QWidget
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

# Widget init 
class mainwidget(QWidget):
    def __init__(self):
        super().__init__()
        self.title = '|SPECTROGRAPHIFIER|'
        self.initUI()
       
    # Window
    def initUI(self):
        self.setGeometry(1000,200,300,75)
        self.setWindowTitle(self.title)
    # Label
        self.label = QLabel("Select a sound file:")
    # Check folders in spec_graphs
        spec_graphs = '../spec_graphs'
        parent = os.listdir(spec_graphs)
        self.categories= []
    # Assing folders to categories
        for filename in parent:
            if filename[0] == '.':
                continue
            self.categories.append(filename)
    # Drop Down Band list
        self.bandselect = QComboBox(self)
        for cat in self.categories:
            self.bandselect.addItem(cat)
        self.bandselect.hide()
        self.bandselect.move(65,40)
    # New category button
        self.new_button = QPushButton('+', self)
        self.new_button.hide()
        self.new_button.clicked.connect(self.new_clck)
        self.new_button.move(200,40)
    # Upload Button
        self.up_button = QPushButton("Choose Sounds", self)
        self.up_button.move(83,15)
        self.up_button.clicked.connect(self.upload_clck)
        self.show()
    # Specgraph Button
        self.spcg_button = QPushButton("Spectrographify", self)
        self.spcg_button.move(80,5)
        self.spcg_button.clicked.connect(self.spcg_clck)
        self.spcg_button.hide()
    # Exit File Button
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.move(110,15)
        self.exit_button.clicked.connect(self.exit_clck)
        self.exit_button.hide()

    # New folder dialog
    class new_folder(QDialog):
        def __init__(self, mainwidget, categories, parent=None):
            super().__init__(parent)

            self.mainwidget = mainwidget
            self.categories = categories

            name_label = QLabel('Name Folder')
            name_line = QLineEdit()
            name_button = QPushButton('Make Folder')

            layout = QBoxLayout(QBoxLayout.TopToBottom)
            layout.addWidget(name_label)
            layout.addWidget(name_line)
            layout.addWidget(name_button)
            self.setLayout(layout)

            def name_clck():
                new_folder_name = name_line.text()
                os.mkdir(new_folder_name)
                self.mainwidget.bandselect.addItem(new_folder_name)
                os.chdir('../data_pipeline')
                self.accept()
            name_button.clicked.connect(name_clck)    
    def new_clck(self):
        os.chdir('../spec_graphs')
        new_folder_dialog = mainwidget.new_folder(self, self.categories)
        new_folder_dialog.exec() 
        
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
            #print(file_name)
            if file_name in existing_files:
                print(f'Removing {file_name}')
                continue
            else:
                #print("Passed check")
                self.prex_checks.append(f)
        self.new_button.show()
        self.bandselect.show()


    # Spectrogram Clcked
    def spcg_clck(self):
        self.bandselect.hide()
        chosen_band = self.bandselect.currentText()
        for f in self.prex_checks:
        # Get file name
            file_name, file_ext = os.path.splitext(f)
            if ".wav" in file_name:
                file_name = file_name.replace('.wav','')
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
        self.new_button.hide()
        self.exit_button.show()
        print("[Done]") 
    
    # Exit Clcked
    def exit_clck(self):
        sys.exit()



    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mainwidget()
    sys.exit(app.exec_())
