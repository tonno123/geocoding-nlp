import spacy
from spacy.pipeline import merge_entities
import json
nlp = spacy.load('nl_core_news_sm')

import sys
sys.path.append('..')


import import_data_json as import_json
import mine_location_descriptions_json as mine_json
import spatial_identifier_extraction as extract
import geocoding
import evaluation_functions_complex as eval

data = import_json.import_data_json('../../data/testsets/flitsservice_testset.json', filepath_complex='../../data/testsets/flitsservice_testset.csv', complex='Y')
input_data = mine_json.get_location_descriptions_json(data, nlp)
articlelist = extract.extractADPLOC(input_data)
article_pred_list = extract.ADPLOCtoPredicate(articlelist)
article_pred_list = extract.deleteDuplicateEntries(article_pred_list)

import pandas as pd
annotated = pd.read_csv('../../data/testsets/flitsservice_testset.csv', skipinitialspace=True)['road'].dropna().values

accuracy_list = []
distance_list = []
ratio_list = []
for i in range(0,50):
    print("########################################### ARTICLE", i,"#######################################")
    print("Spans in article:")
    print(input_data[i])
    print("Predicates found in article:")
    print(article_pred_list[i])
    bbox, way = geocoding.findLocations(article_pred_list[i])
    accuracy_list.append(eval.calc_accuracy(annotated[i].split(","), way))
    distance, ratio = eval.calc_distance(annotated[i].split(","), way)
    distance_list.append(float(str(distance).replace(" km", "")))
    ratio_list.append(float(str(ratio).replace(" km", "")))
    print("Accuracy list:", accuracy_list)
    print("Distance list:", distance_list)
print("Total accuracy:", sum(accuracy_list) / len(accuracy_list))
print("Ratio list:", ratio_list)
