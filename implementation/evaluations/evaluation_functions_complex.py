

def calc_accuracy(annotated, way_list):
    x, y, radius = annotated
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
        if distance < float(radius)/1000:
            accuracy_list.append(1.0)
    if accuracy_list:
        return max(accuracy_list)
    return 0.0

def calc_distance(annotated, way_list):
    x, y, radius = annotated
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
        dr_ratio_list.append(distance/float(radius)*1000)
    if distance_list:
        return min(distance_list), min(dr_ratio_list)
    return 1000.0, 10000.0
