import os
import re

os.chdir('./spec_graphs')
parent = os.listdir()
folders = []
for fol in parent:
    if fol[0] == '.':
        continue
    folders.append(fol)
for f in folders:
    path = f
    for filename in os.listdir(f):
        special_chars = re.findall(r'[^A-Za-z0-9._-]', filename)
        if special_chars:
            newname = re.sub(r'[^A-Za-z0-9._-]','',filename)
            os.rename(os.path.join(path, filename), os.path.join(path, newname))
        if ".wav" in filename:
            newname = filename.replace('.wav','')
            os.rename(os.path.join(path, filename), os.path.join(path, newname))
print('[DONE]')   

