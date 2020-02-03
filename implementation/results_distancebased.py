import spacy
from spacy.pipeline import merge_entities
import json
nlp = spacy.load('nl_core_news_sm')

from jsonNER_implementation import import_data_json as import_json
from jsonNER_implementation import mine_location_descriptions_json as mine_json
from jsonNER_implementation import spatial_identifier_extraction as extract
import geomapping
import evaluation_functions as eval

data = import_json.import_data_json('../data/testsets/flitsservice_testset.json', 80)
input_data = mine_json.get_location_descriptions_json(data, nlp)
print(input_data)
articlelist = extract.extractADPLOCCombination(input_data)
article_pred_list = extract.NLtoPredicate(articlelist)
article_pred_list = extract.deleteDuplicateEntries(article_pred_list)

toponyms, annotated = eval.import_annotated_results()
annotated = eval.sanitize_locations(toponyms, annotated)

distance_list = []
dr_ratio_list = []
not_found = 0
for i in range(0,80):
    print("########################################### ARTICLE", i,"#######################################")
    print("Predicates found in article:")
    print(article_pred_list[i])
    bbox, way = geomapping.findLocations(article_pred_list[i])
    tmp_dist, tmp_ratio, tmp_notfound = eval.calculate_distance(annotated[i], bbox, way)
    distance_list.extend(tmp_dist)
    dr_ratio_list.extend(tmp_ratio)
    not_found = not_found + tmp_notfound
    print("Distance list:", distance_list)
    print("Dist/rad ratio:", dr_ratio_list)
    print("Not found count:", not_found)
print("Average distance:", sum(distance_list) / len(distance_list))
print("Average distance/radius ratio:", sum(dr_ratio_list) / len(dr_ratio_list))
print("Number of not found locations:", not_found)
