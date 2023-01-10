import os 
import sys
import subprocess
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFileDialog, QApplication

# Define directory 
class mainwidget(QWidget):
    def __init__(self):
        super().__init__()
        self.show()
        self.setGeometry(1000,200,200,100)

        # Choose directory button
        up_button = QPushButton("Choose Sounds")
        up_button.move(85,15)
        up_button.show()
        # Convert to wav button
        wav_but = QPushButton('WaViFy')
        wav_but.resize(200,32)
        wav_but.move(60,75)
        wav_but.hide()
        # Remove non wav button
        clean_but = QPushButton('Clean')
        clean_but.move(85,15)
        clean_but.hide()
        # Exit Button
        exit_but = QPushButton('Exit')
        exit_but.resize(200,32)
        exit_but.move(60,75)
        exit_but.hide()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(up_button)
        layout.addWidget(wav_but)

        self.setLayout(layout)
        
        def upload_clck():
            global dir_name
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            dir_name = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)
            wav_but.show()
        up_button.clicked.connect(upload_clck)
        def wav_clck(): 
            # Iterated over all files in directory
            for file in os.listdir(dir_name):
                # Use ffmpeg to convert to wav
                input_filename = os.path.join(dir_name, file)
                output_filename = os.path.splitext(input_filename)[0] + '.wav'
                subprocess.run(['ffmpeg','-i', input_filename, output_filename])
            up_button.hide()
            wav_but.hide()
            layout.removeWidget(wav_but)
            layout.removeWidget(up_button)
            layout.addWidget(clean_but)
            clean_but.show()
            print('[DONE]')
        wav_but.clicked.connect(wav_clck)
        layout.addWidget(exit_but)
        def clean_clck():
            for file in os.listdir(dir_name):
                    if not file.endswith(".wav"):
                        os.remove(os.path.join(dir_name, file))
            exit_but.show()
            clean_but.hide()
        clean_but.clicked.connect(clean_clck)
        def exit_clck():
            sys.exit()
        exit_but.clicked.connect(exit_clck)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mainwidget()
    sys.exit(app.exec_())
