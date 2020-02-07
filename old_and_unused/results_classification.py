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
articlelist = extract.extractADPLOCCombination(input_data)
article_pred_list = extract.NLtoPredicate(articlelist)
article_pred_list = extract.deleteDuplicateEntries(article_pred_list)

toponyms, annotated = eval.import_annotated_results()
annotated = eval.sanitize_locations(toponyms, annotated)
accuracy_list = []
for i in range(0,80):
    print("########################################### ARTICLE", i,"#######################################")
    print("Predicates found in article:")
    print(article_pred_list[i])
    bbox, way = geomapping.findLocations(article_pred_list[i])
    accuracy_list.extend(eval.calculate_accuracy(annotated[i], bbox, way))
    print("Accuracy list:", accuracy_list)
print("Total accuracy:", sum(accuracy_list) / len(accuracy_list))


# accuracy_list = [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0]
# accuracy = sum(accuracy_list) / len(accuracy_list)
# print("Number of locations:", len(accuracy_list))
# print("Accuracy:", accuracy)
