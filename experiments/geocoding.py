from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geocaching_thesis")


location3 = geolocator.geocode("Kanaal-Noord", exactly_one=False)
print(location3[1].raw)



location = geolocator.geocode("A1 Hengelo", exactly_one=False)
print(location)
print(len(location))
print(location[0].address)
print(location[0].raw)
print(location[0].raw.get('boundingbox'))
print(location[4].raw)
print(location[4].raw.get('boundingbox'))
print(location[3].raw.get('boundingbox'))
print(location[2].raw.get('boundingbox'))
print(location[5].raw.get('boundingbox'))
print(location[6].raw.get('boundingbox'))
print(location[6].raw.get('lat'))
print(location[6].raw.get('lon'))
print(location[7].raw.get('boundingbox'))
print(location[8].raw.get('boundingbox'))

# print(location.address)
# print(location.latitude, location.longitude)
# print(location.raw.get('type'))
# print(location.raw)


location2 = geolocator.geocode("Hoolstraat, Teteringen", exactly_one=False)
print(location2.address)
print(location.latitude, location.longitude)
print(location.raw.get('type'))
print(location2[0].raw)
print(location2[1].raw)

location = geolocator.geocode("Maarn")
print(location.address)
print(location.latitude, location.longitude)
print(location.raw.get('type'))
print(location.raw)

for i in range(-1):
    print("test")
