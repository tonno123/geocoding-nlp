import spacy
from spacy.pipeline import merge_entities
import json
nlp = spacy.load('nl_core_news_sm')

from jsonNER_implementation import import_data_json as import_json
from jsonNER_implementation import mine_location_descriptions_json as mine_json
from jsonNER_implementation import spatial_identifier_extraction as extract
import geomapping

data = import_json.import_data_json('../data/flitsservice_trainset_annotated.json', 20)
input_data = mine_json.get_location_descriptions_json(data, nlp)
articlelist = extract.extractADPLOCCombination(input_data)
article_pred_list = extract.NLtoPredicate(articlelist)
article_pred_list = extract.deleteDuplicateEntries(article_pred_list)


bbox_list = []
way_list = []
for i in range(len(input_data)):
    bbox, way = geomapping.findLocations(article_pred_list[i])
    bbox_list.append(bbox)
    way_list.append(way)
print("bbox:", bbox_list)
print("way:", way_list)
