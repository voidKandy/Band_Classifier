import os 
import subprocess

# Define directory 
dir_name = 'King Gizzard & the Lizard Wizard - Butterfly 3000 - YouTube'
# Iterated over all files in directory
for file in os.listdir(dir_name):
    # Use ffmpeg to convert to wav
    input_filename = os.path.join(dir_name, file)
    output_filename = os.path.splitext(input_filename)[0] + '.wav'
    subprocess.run(['ffmpeg','-i', input_filename, output_filename])

print('[DONE]')
response = input('Delete non wav files? (y/n)')
if response == 'y':
    for file in os.listdir(dir_name):
        if not file.endswith(".wav"):
            os.remove(os.path.join(dir_name, file))
else:
    exit()
print("[DONE]")
response = input("Do you want to exit? (y/n)")
if response == 'y':
    exit() 
