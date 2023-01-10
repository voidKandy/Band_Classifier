import subprocess
from colorama import init, Fore, Style, Back
import time
import io
from art import *
import sys

global scraped
global converted
global spectrographed
scraped = False
converted = False
spectrographed = False

def scraper():
    global scraped
    process = subprocess.Popen(['python', 'yt_playlist_scraper.py'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while process.poll() is None:
        # Read all of the output from the subprocess
        output = process.stdout.read(2048)
        # Split the output on the newline character
        lines = output.decode('utf-8').strip().split('\n')
        if lines[-1] == '[DONE]':
            scraped = True  
        else:
            print(Fore.CYAN+lines[-1], end='\r', flush=True)
def converter():
    global converted
    print('\n')
    process = subprocess.Popen(['python', 'webm>wav.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while process.poll() is None:
         # Read all of the output from the subprocess
        output = process.stdout.read(2048)
        # Split the output on the newline character
        lines = output.decode('utf-8').strip().split('\n')
        if lines[-1] == '[DONE]':
            converted = True 
        else:
            print(Fore.CYAN+lines[-1], end='\r', flush=True)
def spectrograph():
    global spectrographed
    process = subprocess.Popen(['python', 'spectrographifier.py'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while process.poll() is None:
        # Read all of the output from the subprocess
        output = process.stdout.read(2048)
        # Split the output on the newline character
        lines = output.decode('utf-8').strip().split('\n')
        if lines[-1] == '[DONE]':
            spectrographed = True 
        else:
            print(Fore.CYAN+lines[-1], end='\r', flush=True)

print(" ------------------------------------ ")
print(" |       0                 0        |") 
print(" |       0                 0        |")
print(" ------------------------------------ ")
print(Fore.GREEN + Style.BRIGHT+ ' [.....WELCOME TO THE DATA PIPE.....]')
print(" [ .__ENTER  'spacebar' TO START__. ]")
key = input('                 ')  
if key == ' ':
    scraper()
if scraped == True:
    for line in [
         "                     ",
         "                /\\",
         "               /  \\",  
         "              /    \\",  
         "             /      \\", 
         "            |   ..   |", 
         "            |   ..   |", 
         "            |  /..\\  |", 
         "            |  Type  |", 
         "            |  '^^'  |", 
         "            |  \\../  |", 
         "            |   to   |", 
         "            | unclog |", 
         "            |  PiPe  |", 
         "            |________|" 
    ]:
        print(Fore.GREEN + Style.BRIGHT+(line))
        time.sleep(0.08)
    key = input("                ")
    if key == '^^':
        converter()
    if converted == True:
        for line in [
            "                ##",
            "               ####",
            "              ######",
            "             ########",
            "            ##########",
            "           ############",
        ]:
            print(line)
            time.sleep(0.08)
        print("          #####"+Fore.YELLOW+'DATA'+Fore.GREEN+"#####")
        print("         ####"+Fore.YELLOW+'WAVIFIED'+Fore.GREEN+"####")
        for line in [
         "         ################",
         "          #####"+Fore.YELLOW+'PUSH'+Fore.GREEN+"#####",
         "           ###"+Fore.YELLOW+'ENTER'+Fore.GREEN+"####",
         "             ########",
         "              ######",
         "               ####",
         "                ##"
        ]:
           print(line)
           time.sleep(0.08) 
        key = input()
        if key == '':
            print(text2art("BOOTING SPECTROGRAPHIFIER", font='fancy42'))
            spectrograph()
if spectrographed == True:
    print(Fore.LIGHTMAGENTA_EX+"         ",decor("barcode1")+ text2art("    Your Sounds Have Been   ",font="fancy42")+decor("barcode1",reverse=True))
    tprint('SPECTROGRAPHED', font='cybermedium')
    response = input("TYPE 'EXIT' TO EXIT: ")
    if response == 'EXIT' or response == 'exit':
        sys.exit()