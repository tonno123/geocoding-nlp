from geopy.geocoders import Nominatim
import overpy
import time
import math
from geopy.exc import GeocoderTimedOut
from geopy.exc import GeocoderUnavailable

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from geopy.distance import geodesic
import copy


nom = Nominatim(user_agent="geocoding_thesis")
api = overpy.Overpass()

NominatimResultList = []
OverpassResultList = []

def isHighway(roadname):
    if roadname[:1] is 'A' or roadname[:1] is 'N':
        if roadname[1:2].isdigit():
            return True
    return False

def getADPs(sent):
    ADP_list = []
    for location in sent:
        ADP_list.append(location[0])
    return ADP_list

def orderSent(sentence):
    for i in range(len(sentence)-1):
        if sentence[i][0] is 'INTERSECT':
            sentence.append(sentence.pop(i))
    return sentence

def OverpassSearch(query, waittime=3):
    from overpy.exception import OverpassTooManyRequests
    from overpy.exception import OverpassGatewayTimeout
    try:
        query_result = api.query(query)
        result =  query_result
    except OverpassTooManyRequests:
        print("Overpass receives too many requests, waiting", waittime, "seconds.")
        time.sleep(waittime)
        result = OverpassSearch(query,waittime*2)
    except OverpassGatewayTimeout:
        print("Overpass gateway overload, waiting", waittime, "seconds.")
        time.sleep(waittime)
        result = OverpassSearch(query,waittime*2)
    return result

def OverpassQuery(roadname, area="Nederland"):
    for element in OverpassResultList:
        if element[0] == roadname:
            return element[1]
    if isinstance(roadname, list):
        [road1, road2] = roadname
        if isHighway(road1):
            road1_type = "ref"
        else:
            road1_type = "name"
        if isHighway(road2):
            road2_type = "ref"
        else:
            road2_type = "name"
        query = """
        area["name"="Nederland"]->.boundaryarea;
        (
        nwr[%s="%s"];node(w)->.n1;
        nwr[%s="%s"];node(w)->.n2;
        );
        node.n1.n2;
        out center;
        """ % (road1_type, road1, road2_type, road2)
    else:
        if isHighway(roadname):
            road_type = "ref"
        else:
            road_type = "name"
        query = """
        area["name"="%s"]->.boundaryarea;
        (
        nwr(area.boundaryarea)[%s="%s"];
        );
        out center;
        """ % (area, road_type, roadname)
    result = OverpassSearch(query)
    OverpassResultList.append([roadname, result])
    return result

def NominatimSearch(location, waittime=3):
    for element in NominatimResultList:
        if element[0] == location:
            return element[1]
    try:
        result = nom.geocode(location, country_codes='nl', exactly_one=False,limit=100)
        time.sleep(1.1)
    except GeocoderTimedOut or GeocoderUnavailable:
        print("Nominatim timed out, waiting", waittime, "seconds.")
        time.sleep(waittime)
        result = NominatimSearch(location, waittime*2)
    NominatimResultList.append([location, result])
    return result

def CoordsInBoundingbox(coordinate_list, boundingbox):
    result_list = []
    if not isinstance(boundingbox[0], tuple):
        for coord in coordinate_list:
            if coord[0] > float(boundingbox[0]) and coord[0] < float(boundingbox[1]):
                if coord[1] > float(boundingbox[2]) and coord[1] < float(boundingbox[3]):
                    result_list.append(coord)
    else:
        polygon = Polygon(boundingbox)
        for coord in coordinate_list:
            if polygon.contains(Point(coord[0],coord[1])):
                result_list.append(coord)
    return result_list

def intersect(roads, boundingbox_list_sent, way_list_sent):
    if len(roads) < 2:
        way_list_sent.append(['intersect',roads])
        return boundingbox_list_sent, way_list_sent

    query_result = OverpassQuery([roads[0], roads[1]])
    if query_result:
        result_list = []
        for node in query_result.nodes:
            result_list.append([float(node.lat), float(node.lon)])
        if result_list:
            way_list_sent.append(['crossroads', result_list])
    return boundingbox_list_sent,way_list_sent

def getBestBetweenLocation(search_result):
    for i in range(len(search_result)):
        if i > 3:
            break
        if search_result[i].raw.get('class') == 'place':
            return (float(search_result[i].raw.get('lat')), float(search_result[i].raw.get('lon')))
    return (float(search_result[0].raw.get('lat')), float(search_result[0].raw.get('lon')))

def between(location, bbox_list_sent, way_list_sent):
    if len(location) < 2:
        return bbox_list_sent,way_list_sent
    searchresult1 = NominatimSearch(location[0])
    time.sleep(1.1)
    searchresult2 = NominatimSearch(location[1])
    if searchresult1 and searchresult2:
        lat1,lon1 = getBestBetweenLocation(searchresult1)
        lat2,lon2 = getBestBetweenLocation(searchresult2)

        angle = math.atan2(lon2-lon1,lat2-lat1)
        distance = geodesic((lat1,lon1),(lat2,lon2))/math.sqrt(2)
        point1_x,point1_y,_ = distance.destination(point=[lat1,lon1], bearing=math.degrees(angle)+45)
        point2_x,point2_y,_ = distance.destination(point=[lat1, lon1], bearing=math.degrees(angle)-45)
        bbox_list_sent.append(['between',[(point1_x,point1_y),(lat1,lon1),(point2_x,point2_y),(lat2,lon2)]])
    return bbox_list_sent, way_list_sent

def in_loc(location, boundingbox_list_sent, way_list_sent):
    place = []
    result_list = NominatimSearch(location)
    if result_list:
        for result in result_list:
            if result.raw.get('class') == 'boundary':
                boundingbox_list_sent.append(['in', result.raw.get('boundingbox')])
                return boundingbox_list_sent, way_list_sent
            elif result.raw.get('class') == 'place' and not place:
                place = result.raw.get('boundingbox')
        if place:
            boundingbox_list_sent.append(['in', place])
        else:
            boundingbox_list_sent.append(['in', result_list[0].raw.get('boundingbox')])
    return boundingbox_list_sent, way_list_sent

def heading(roadname,bbox_list_sent,way_list_sent):
    return bbox_list_sent,way_list_sent

def on(roadname, boundingbox_list_sent, way_list_sent):
    query_result = OverpassQuery(roadname[0])
    if query_result:
        result = []
        for way in query_result.ways:
            result.append([float(way.center_lat), float(way.center_lon)])
        if result:
            if isHighway(roadname[0]):
                way_list_sent.append(["highway", roadname[0],result])
            else:
                way_list_sent.append(["street", roadname[0], result])
    return boundingbox_list_sent, way_list_sent

def at(location, boundingbox_list_sent, way_list_sent):
    place = []
    result_list = NominatimSearch(location)
    if result_list:
        for result in result_list:
            if result.raw.get('class') == 'boundary':
                boundingbox_list_sent.append(['at', result.raw.get('boundingbox')])
                return boundingbox_list_sent, way_list_sent
            elif result.raw.get('class') == 'place' and not place:
                place = result.raw.get('boundingbox')
        if place:
            boundingbox_list_sent.append(['at', place])
    return boundingbox_list_sent, way_list_sent

def mergeLists(bbox_list, way_list):
    way_list_new = []
    for way in way_list:

        if way[0] is 'street' or way[0] is 'crossroads':
            for bbox in bbox_list:
                result = CoordsInBoundingbox(way[-1], bbox[1])
                if result:
                    way[-1] = result
                    bbox_list.pop(bbox_list.index(bbox))

        elif way[0] is 'highway':
            for bbox in bbox_list:
                if bbox[0] is not 'in':
                    result = CoordsInBoundingbox(way[2], bbox[1])
                    if result:
                        way[2] = result
                        bbox_list.pop(bbox_list.index(bbox))

        elif way[0] is 'intersect':
            for road in way_list:
                if road[0] != 'crossroads' and road[1] != way[1][0]:
                    way_list_old = copy.deepcopy(way_list)
                    bbox_list, way_list = intersect([way[1][0],road[1]], bbox_list, way_list)
                    if way_list_old != way_list:
                        way_list.pop(way_list.index(road))
                        way_list.pop(way_list.index(way))
                        break

    return bbox_list, way_list

def printResults(bbox_list,way_list):
    for location in bbox_list:
        print("Bounding box:", location[-1])
    for location in way_list:
        print("Road coordinates:",location[-2], "***********")

def sanitizeResults(bbox_list, way_list):
    for element in way_list:
        if element[0] == 'intersect':
            way_list.pop(way_list.index(element))
    for element in bbox_list:
        print("boundingbox 2:", bbox_list)
        if element[0] == 'between':
            bbox_list.pop(bbox_list.index(element))
    return bbox_list, way_list

def findLocations(article):
    boundingbox_list = []
    way_list = []
    for sent in article:
        boundingbox_list_sent = []
        way_list_sent = []
        sent = orderSent(sent)
        ADP_list = getADPs(sent)
        for i in range(len(ADP_list)):
            boundingbox_list_sent, way_list_sent = eval(ADP_list[i].lower())(sent[i][1], boundingbox_list_sent, way_list_sent)
        boundingbox_list_sent, way_list_sent = mergeLists(boundingbox_list_sent, way_list_sent)
        boundingbox_list.extend(boundingbox_list_sent)
        way_list.extend(way_list_sent)
    boundingbox_list, way_list = mergeLists(boundingbox_list, way_list)
    boundingbox_list, way_list = sanitizeResults(boundingbox_list, way_list)
    printResults(boundingbox_list,way_list)
    return boundingbox_list, way_list
