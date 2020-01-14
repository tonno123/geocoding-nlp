import overpy

api = overpy.Overpass()
# #
# r3 = api.query("""
# area["name"="Nederland"]->.boundaryarea;
# (
# nwr[name="Kerkstraat"];node(w)->.n1;
# nwr[name="Molenweg"];node(w)->.n2;
# );
# node.n1.n2;
# out center;
# """)
# for way in r3.ways:
#     print(way.center_lat, way.center_lon)
# for node in r3.nodes:
#     print(node.lat,node.lon)
# for relations in r3.relations:
#     print(relations.members)

#################################################################################

# import geopy# import geopy
# from geopy.geocoders import Nominatim
# from geopy.distance import geodesic
# nom = Nominatim(user_agent="geocoding_thesis")
# import math
#
# location3 = nom.geocode("Tilburg", country_codes='nl', exactly_one=False,limit=100)
# lat1 = float(location3[0].raw.get('lat'))
# lon1 = float(location3[0].raw.get('lon'))
# print(lat1,lon1)
# location4 = nom.geocode("Breda", country_codes='nl', exactly_one=False,limit=100)
# lat2 = float(location4[0].raw.get('lat'))
# lon2 = float(location4[0].raw.get('lon'))
# print(lat2,lon2)
# angle = math.atan2(lon2-lon1,lat2-lat1)
# print(angle)
# #distance = float(str(geodesic((lat1,lon1),(lat2,lon2))/math.sqrt(2))[:-3])
# distance = geodesic((lat1,lon1),(lat2,lon2))/math.sqrt(2)
#
# print(math.degrees(angle))
#
# #s = geodesic(kilometers=distance)
# dest_point = distance.destination(point=[lat1,lon1], bearing=math.degrees(angle)+45)
# dest_point2 = distance.destination(point=[lat1, lon1], bearing=math.degrees(angle)-45)
# (test1,test2,_) = dest_point
# result = (test1,test2)
# print(result)
#
#
# lat,lon,_ = dest_point
# lat2,lon2,_ = dest_point2
# print(lat,lon)
# print(lat2,lon2)
# from geopy.geocoders import Nominatim
# from geopy.distance import geodesic
# nom = Nominatim(user_agent="geocoding_thesis")
# import math
#
# location3 = nom.geocode("Tilburg", country_codes='nl', exactly_one=False,limit=100)
# lat1 = float(location3[0].raw.get('lat'))
# lon1 = float(location3[0].raw.get('lon'))
# print(lat1,lon1)
# location4 = nom.geocode("Breda", country_codes='nl', exactly_one=False,limit=100)
# lat2 = float(location4[0].raw.get('lat'))
# lon2 = float(location4[0].raw.get('lon'))
# print(lat2,lon2)
# angle = math.atan2(lon2-lon1,lat2-lat1)
# print(angle)
# #distance = float(str(geodesic((lat1,lon1),(lat2,lon2))/math.sqrt(2))[:-3])
# distance = geodesic((lat1,lon1),(lat2,lon2))/math.sqrt(2)
#
# print(math.degrees(angle))
#
# #s = geodesic(kilometers=distance)
# dest_point = distance.destination(point=[lat1,lon1], bearing=math.degrees(angle)+45)
# dest_point2 = distance.destination(point=[lat1, lon1], bearing=math.degrees(angle)-45)
# (test1,test2,_) = dest_point
# result = (test1,test2)
# print(result)
#
#
# lat,lon,_ = dest_point
# lat2,lon2,_ = dest_point2
# print(lat,lon)
# print(lat2,lon2)
#print(help(type(dest_point)))
# print("lon distance:",lon_distance)
# print("lat distance:",lat_distance)
# for location in location3:
#     print(location.raw)

r3 = api.query("""
area["name"="Nederland"]->.boundaryarea;
(
nwr(area.boundaryarea)[name="Langebosschedijk"];
);
out center;
""")
print(r3)
for way in r3.ways:
    print(way.center_lat, way.center_lon)



article = [['a'], ['b'],['d','e'], ['b','c'], ['b'], ['c'], ['a'],['d']]
# list[:1] + list[2:]
# list[:1] + [list[1]] + list[2:]

print(len(article[0]))
for i in range(len(article)):
    print('NEW ROUND')
    if len(article[i]) == 1:
        article_copy = article[:i] + article[(i+1):]
        match_sent = article[i][0]
        print(match_sent)
        if article[i] in article_copy:
            print("Deleting double")
            article = article[:i] + article[(i+1):]
print(article)

        # for sentence in article_copy:
        #     for location in sentence:
        #         print(location)
        #         if match_sent == location:
        #             article = article[:i] + article[(i+1):]
        #             print(article)

print(article)




new_list = []
for sentence in list:
    print(sentence)
    new_list.append(sentence)
    list.remove(sentence)
    try:
        list.remove(sentence)
        list.remove(sentence)
        list.remove(sentence)
    except ValueError:
        print("no more")
print(new_list)





def removeDuplicateLocations(article):
    for i in range(len(article)):
        if len(article[i]) is 1:
            for ii in range(len(article))


def removeDuplicateLocations(article):
    for sentence in article:
        if len(sentence) is 1:
            article_copy = deepcopy(article)
            article_copy.remove(sentence)
            for sent in article_copy


article = [['a'], ['b'],['a','d','e'], ['b','c','e'], ['b'], ['c'], ['a'],['d'],['f']]
article[-1:]
def matchSentence(match, article):
    for sentence in article:
        for location in sentence:
            if match == location:
                return True
    return False

i = 0
while i < len(article):
    if len(article[i]) == 1:
        article_copy = article[:i] + article[(i+1):]
        print("article_copy:", article_copy)
        if matchSentence(article[i][0], article_copy):
            article = article_copy
        else:
            i = i+1
    else:
        i = i+1
print(article)




way_list = [['crossroads', [[51.5441104, 5.0943147], [51.5441947, 5.0942256], [51.5443332, 5.0941176], [51.544174, 5.0944913], [51.5444218, 5.0943134], [51.5442711, 5.0944122]]], ['crossroads', [[51.543256, 5.082651], [51.5435424, 5.0829808], [51.5432559, 5.082651]]], ['crossroads', [[51.5441104, 5.0943147], [51.5441947, 5.0942256], [51.5443332, 5.0941176], [51.544174, 5.0944913], [51.5444218, 5.0943134], [51.5442711, 5.0944122]]]]
for location in way_list:
    print(location[-1])
    for coord in location[-1]:
        print(coord[0],coord[1])
