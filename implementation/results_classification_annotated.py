import json

from jsonNER_implementation import spatial_identifier_extraction as extract
import geomapping
import evaluation_functions as eval

toponyms, annotated = eval.import_annotated_results()
annotated = eval.sanitize_locations(toponyms, annotated)

toponyms = eval.annotated_toponyms_as_input(toponyms)
toponym_predicates = extract.NLtoPredicate(toponyms)
toponym_predicates = extract.deleteDuplicateEntries(toponym_predicates)

accuracy_list = []
for i in range(0,80):
    print("########################################### ARTICLE", i,"#######################################")
    print("Predicates found in article:")
    print(toponym_predicates[i])
    bbox, way = geomapping.findLocations(toponym_predicates[i])
    accuracy_list.extend(eval.calculate_accuracy(annotated[i], bbox, way))
    print("Accuracy list:", accuracy_list)
print("Total accuracy:", sum(accuracy_list) / len(accuracy_list))


# accuracy_list = [0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0]
# accuracy_list2 = [1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0]
# accuracy_list.extend(accuracy_list2)
# accuracy = sum(accuracy_list) / len(accuracy_list)
# print("Number of locations:", len(accuracy_list))
# print(accuracy)
