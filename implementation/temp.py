import spacy
from spacy.pipeline import merge_entities
import json
nlp = spacy.load('nl_core_news_sm')

from jsonNER_implementation import import_data_json as import_json
from jsonNER_implementation import mine_location_descriptions_json as mine_json

data = import_json.import_data_json('../data/flitsservice_trainset_annotated.json', 80)
input_data = mine_json.get_location_descriptions_json(data, nlp)

for i in range(40):
    print(data[i])
    print(input_data[i])
    print("############################################################################")
