import os
import re

cd = './'
os.chdir('./')
parent = os.listdir()
folders = []

parent_dir = False # Change this if u want 0-0

def clean():
    path = f
    for filename in folders:
        for filename in os.listdir(f):
            special_chars = re.findall(r'[^A-Za-z0-9._-]', filename)
            if special_chars:
                newname = re.sub(r'[^A-Za-z0-9._-]','',filename)
                os.rename(os.path.join(path, filename), os.path.join(path, newname))
            if ".wav" in filename:
                newname = filename.replace('.wav','')
            os.rename(os.path.join(path, filename), os.path.join(path, newname))

if parent_dir == True:
    for fol in parent:
        if fol[0] == '.':
            continue
        folders.append(fol)
        for f in folders:
            clean()
else:
    folders = parent
    f = cd 
    clean()

print('[DONE]')   

