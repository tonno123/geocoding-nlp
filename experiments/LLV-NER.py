import sys
sys.path.insert(1, '/home/toon/Documents/Afstudeerproject/geocoding-thesis/implementation/model')

import model_location_detection as chris
filedir = '/home/toon/Documents/Afstudeerproject/geocoding-nlp/data/transport-online.csv'

with open(filedir,'r') as f:
    data = json.load(f)

print(data)

#chris.get_string_toponyms
