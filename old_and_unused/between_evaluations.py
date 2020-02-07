import gmplot

import sys
sys.path.append('..')

import spacy
from spacy.pipeline import merge_entities
import json
nlp = spacy.load('nl_core_news_sm')

import import_data_json as import_json
import mine_location_descriptions_json as mine_json
import spatial_identifier_extraction as extract
import geocoding
import evaluation_functions as eval

def containsBetween(article):
    for sentence in article:
        for pred_topo in sentence:
            if pred_topo[0] == 'BETWEEN':
                return True
    return False

data = import_json.import_data_json('../../data/flitsservice_trainset.json', 100)
input_data = mine_json.get_location_descriptions_json(data, nlp)
articlelist = extract.extractADPLOC(input_data)
article_pred_list = extract.ADPLOCtoPredicate(articlelist)
article_pred_list = extract.deleteDuplicateEntries(article_pred_list)



bbox_list = []
way_list = []
for i in range(0,1500):
    if not containsBetween(article_pred_list[i]):
        continue
    print("########################################### ARTICLE", i,"#######################################")
    print(data[i])
    print(input_data[i])
    print("Predicates found in article:")
    print(articlelist[i])
    print(article_pred_list[i])
    bbox, way = geocoding.findLocations(article_pred_list[i])
    print("Found bounding boxes:", bbox)
    print("Found roads:", way)




gmap = gmplot.GoogleMapPlotter(52.428, 4, 13)
gmap.draw("BETWEEN", i, ".html")
