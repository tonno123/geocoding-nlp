
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
    return 1000.0, None

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
    return 1000.0, None

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
            distance_list.append(min(distance1, distance2))
            dr_ratio_list.append(min(ratio1, ratio2))
    return distance_list, dr_ratio_list, not_found
