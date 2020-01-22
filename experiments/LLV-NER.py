import sys
sys.path.insert(1, '/home/toon/Documents/Afstudeerproject/geocoding-thesis/implementation/model')

import model_location_detection as chris

import json
filedir = '/home/toon/Documents/Afstudeerproject/geocoding-nlp/data/v4_hetongeluk.json'

with open(filedir,'r') as f:
    data = json.load(f)

data = data[1]
print(data)
chris.get_string_toponyms(data)
print(data)
print(type(data))

for i in data:
    print(type(i))
    #chris.get_string_toponyms(i)

#print(data)

#chris.get_string_toponyms
