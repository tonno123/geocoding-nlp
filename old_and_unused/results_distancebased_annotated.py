import json
from jsonNER_implementation import spatial_identifier_extraction as extract
import geomapping
import evaluation_functions as eval

toponyms, annotated = eval.import_annotated_results()
annotated = eval.sanitize_locations(toponyms, annotated)

toponyms = eval.annotated_toponyms_as_input(toponyms)
toponym_predicates = extract.NLtoPredicate(toponyms)
toponym_predicates = extract.deleteDuplicateEntries(toponym_predicates)

distance_list = []
dr_ratio_list = []
not_found = 0
for i in range(44,80):
    print("########################################### ARTICLE", i,"#######################################")
    print("Predicates found in article:")
    print(toponym_predicates[i])
    bbox, way = geomapping.findLocations(toponym_predicates[i])
    tmp_dist, tmp_ratio, tmp_notfound = eval.calculate_distance(annotated[i], bbox, way)
    distance_list.extend(tmp_dist)
    dr_ratio_list.extend(tmp_ratio)
    not_found = not_found + tmp_notfound
    print("Distance list:", distance_list)
    print("Dist/rad ratio:", dr_ratio_list)
print("Average distance:", sum(distance_list) / len(distance_list))
print("Average distance/radius ratio:", sum(dr_ratio_list) / len(dr_ratio_list))
print("Number of not found locations:", not_found)
