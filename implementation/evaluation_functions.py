
MARKER_WORDS = ['in', 'op', 'over', 'bij', 'hoogte', 'richting', 'naar', 'tussen', 'kruising','kruispunt','te', 'splitsing']

import pandas as pd

def import_annotated_results():
    df = pd.read_csv('../data/annotated/annotated_flitsservice_testset.csv', skipinitialspace=True)
    toponyms = df['Toponiemen']
    locations = df['Locaties']
    return toponyms, locations

def annotated_toponyms_as_input(toponyms):
    import re
    toponym_list = []
    for article in toponyms:
        article_list = []
        article = re.split(r',\s*(?![^[\]]*\])', article)
        for toponym in article:
            topo = toponym.strip().split(" ")
            print("topo:", topo)
            if topo[0] in MARKER_WORDS:
                if topo[1][0] == '[':
                    topo[1] = topo[1].strip("[]").split(",")
                    topo[1] = [topo[1][0].replace("_", " "), topo[1][1].replace("_", " ")]
                    print("special topo:", topo[1])
                    article_list.append([[topo[0]], topo[1]])
                else:
                    article_list.append([[topo[0]], [topo[1].replace("_", " ")]])
        toponym_list.append([article_list])
    return toponym_list

def sanitize_locations(toponyms, locations):
    import re
    toponym_list = []
    for article in toponyms:
        tmp_list = []
        article = re.split(r',\s*(?![^[\]]*\])', article)
        for toponym in article:
            topo = toponym.strip().split(" ")
            if topo[0] in MARKER_WORDS:
                if topo[1][0] == '[':
                    topo[1] = topo[1].strip("[]").split(",")
                    tmp_list.extend(topo[1])
                else:
                    tmp_list.append(topo[1])
        toponym_list.append(tmp_list)
    new_article_list = []
    for i, article in enumerate(locations):
        new_article = list(filter(None, article.split(";")))
        return_article = []
        for location in new_article:
            new_location = location.split(",")
            new_location[3] = float(new_location[3])
            if new_location[2].strip() in toponym_list[i]:
                return_article.append(new_location)
        new_article_list.append(return_article)
    return new_article_list

def way_list_accuracy(annotated, way_list):
    x, y, _, radius = annotated
    from geopy.distance import geodesic
    accuracy_list = []
    for location in way_list:
        x_list = []
        y_list = []
        for coord in location[-1]:
            x_list.append(coord[0])
            y_list.append(coord[1])
        x_avg = sum(x_list) / len(x_list)
        y_avg = sum(y_list) / len(y_list)
        distance = geodesic((x,y),(x_avg, y_avg))
        print("distance road:", distance)
        print("radius:", radius)
        if distance < radius/1000:
            accuracy_list.append(1.0)
    if accuracy_list:
        return max(accuracy_list)
    return 0.0

def bbox_list_accuracy(annotated, bbox_list):
    x, y, _, radius = annotated
    from geopy.distance import geodesic
    accuracy_list = []
    for location in bbox_list:
        x_list = []
        y_list = []
        if isinstance(location[-1][0], tuple):
            for el in location[-1]:
                x_list.append(el[0])
                y_list.append(el[1])
        else:
            x_list.extend([float(location[-1][0]), float(location[-1][1])])
            y_list.extend([float(location[-1][2]), float(location[-1][3])])
        x_avg = sum(x_list) / len(x_list)
        y_avg = sum(y_list) / len(y_list)
        distance = geodesic((x,y),(x_avg, y_avg))
        print("distance bbox:", distance)
        print("radius:", radius)
        if distance < radius/1000:
            accuracy_list.append(1.0)
    if accuracy_list:
        return max(accuracy_list)
    return 0.0

def calculate_accuracy(annotated, bbox_list, way_list):
    accuracy_list = []
    for el in annotated:
        result1 = way_list_accuracy(el, way_list)
        result2 = bbox_list_accuracy(el, bbox_list)
        if result1 > 0.0 and result2 > 0.0:
            print("WARNING: bbox and waylist both have a suited result. ways:",result1," Bbox:",result2)
        accuracy_list.append(max(result1, result2))
        print("Accuracy:", max(result1, result2))
    return accuracy_list

def way_list_distance(annotated, way_list):
    x, y, _, radius = annotated
    from geopy.distance import geodesic
    distance_list = []
    dr_ratio_list = []
    for location in way_list:
        x_list = []
        y_list = []
        for coord in location[-1]:
            x_list.append(coord[0])
            y_list.append(coord[1])
        x_avg = sum(x_list) / len(x_list)
        y_avg = sum(y_list) / len(y_list)
        distance = geodesic((x,y),(x_avg, y_avg))
        print("distance road:", distance)
        print("radius:", radius)
        distance_list.append(distance)
        dr_ratio_list.append(distance/radius*1000)
    if distance_list:
        return min(distance_list), min(dr_ratio_list)
    return 1000.0, 10000.0

def bbox_list_distance(annotated, bbox_list):
    x, y, _, radius = annotated
    from geopy.distance import geodesic
    distance_list = []
    dr_ratio_list = []
    for location in bbox_list:
        x_list = []
        y_list = []
        if isinstance(location[-1][0], tuple):
            for el in location[-1]:
                x_list.append(el[0])
                y_list.append(el[1])
        else:
            x_list.extend([float(location[-1][0]), float(location[-1][1])])
            y_list.extend([float(location[-1][2]), float(location[-1][3])])
        x_avg = sum(x_list) / len(x_list)
        y_avg = sum(y_list) / len(y_list)
        distance = geodesic((x,y),(x_avg, y_avg))
        print("distance bbox:", distance)
        print("radius:", radius)
        distance_list.append(distance)
        dr_ratio_list.append(distance/radius*1000)
    if distance_list:
        return min(distance_list), min(dr_ratio_list)
    return 1000.0, 10000.0

def calculate_distance(annotated, bbox_list, way_list):
    distance_list = []
    dr_ratio_list = []
    not_found = 0
    for el in annotated:
        distance1, ratio1 = way_list_distance(el, way_list)
        distance2, ratio2 = bbox_list_distance(el, bbox_list)
        if min(distance1, distance2) == 1000.0:
            not_found = not_found + 1
        else:
            distance_list.append(float(str(min(distance1, distance2)).replace(" km", "")))
            dr_ratio_list.append(float(str(min(ratio1, ratio2)).replace(" km", "")))
    return distance_list, dr_ratio_list, not_found
