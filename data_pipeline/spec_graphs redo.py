import os

spec_graphs = '../spec_graphs'
parent = os.listdir(spec_graphs)
categories= []
for filename in parent:
    if filename[0] == '.':
        continue
    categories.append(filename)
print(categories)