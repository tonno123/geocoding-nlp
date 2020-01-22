# - import results
# - create function so "uit" results are removed
# - create function to compare each annotated result to each application result
#      - for application result streets: get point closest to annotated point, check if smaller than distance value in annotated data
#      - for application bounding boxes: check if annotated point in bounding box.
#

import pandas as pd

def import_annotated_results():
    df = pd.read_csv('../data/annotated/annotated_flitsservice_testset.csv', skipinitialspace=True)
    toponyms = df['Toponiemen']
    locations = df['Locaties']
    return toponyms, locations

# change this so that it removes all locations that have a preposition that is not supported, not just "uit"
def remove_uit_results(toponyms, locations):
    new_locations_list = []
    for i, article in enumerate(toponyms):
        toponym_list = article.split(",")
        new_location = list(filter(None, locations[i].split(";")))
        for el in toponym_list:
            el = el.strip()
            if el[:3] == 'uit':
                uit_toponym = el.split(" ")[-1]
                for location in new_location:
                    if uit_toponym == location.split(",")[2]:
                        new_location.pop(new_location.index(location))
        new_locations_list.append(new_location)
    return new_locations_list

toponyms, locations = import_annotated_results()
locations = remove_uit_results(toponyms, locations)
print(locations)

def way_list_accuracy(lat1, lon1, max_dist, coord_list):
    for location in coord_list:
        correct_counter = 0
        for [lat2,lon2] in location[-1]:
            distance = geodesic((lat1,lon1),(lat2,lon2))
            if distance < max_dist:
                correct_counter = correct_counter + 1
        


def bbox_list_accuracy()

def calculate_accuracy(annotated, bbox_list, way_list):
    from geopy.distance import geodesic
