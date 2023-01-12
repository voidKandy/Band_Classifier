import subprocess
from colorama import init, Fore, Style, Back
import time
import io
from art import *
import sys

global scraped
scraped = True
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

def spectrograph():
    process = subprocess.Popen(['python', 'spectrographifier.py'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while process.poll() is None:
        print(Fore.GREEN+ text2art("[][][][][]", font='invita'))
        # Read all of the output from the subprocess
        output = process.stdout.read(2048)
        # Split the output on the newline character
        lines = output.decode('utf-8').strip().split('\n')
    print(Fore.LIGHTMAGENTA_EX+"                      ",decor("barcode1")+ text2art("    Your Sounds Have Been   ",font="fancy42")+decor("barcode1",reverse=True))
    tprint('    SPECTROGRAPHED', font='cybermedium')
    print(Fore.GREEN)
    response = input("TYPE 'EXIT' TO EXIT: ")
    if response == 'EXIT' or response == 'exit':
        sys.exit()
            

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
            "                ##",
            "               ####",
            "              ######",
            "             ########",
            "            ##########",
            "           ############",
        ]:
            print(line)
            time.sleep(0.08)
        print("          #####"+Fore.YELLOW+'DATA'+Fore.CYAN+"#####")
        print("         ####"+Fore.YELLOW+'WAVIFIED'+Fore.CYAN+"####")
        for line in [
         Fore.CYAN+"         ################",
         "          ####"+Fore.YELLOW+'RETURN'+Fore.CYAN+"####",
         "           #####"+Fore.YELLOW+'TO'+Fore.CYAN+"#####",
         "             ##"+Fore.YELLOW+'EXIT'+Fore.CYAN+"##",
         "              ######",
         "               ####",
         "                ##" + Fore.LIGHTBLACK_EX
        ]:
           print(line)
           time.sleep(0.08) 
        key = input()
        if key == '':
            sys.exit()
        if key == 'spec':
            print(Fore.MAGENTA)
            print(text2art("                          BOOTING SPECTROGRAPHIFIER", font='manga'))
            spectrograph()
