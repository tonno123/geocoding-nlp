import overpy

api = overpy.Overpass()
r = api.query("""
area["name"="Nederland"]->.boundaryarea;
(
nwr(area.boundaryarea)[name="Breda"];
);
out center;
""")
print(r)





for way in r.ways:
    print(float(way.center_lat),",", float(way.center_lon))
    print(way)
    print("======================================")
r.get_way(741000339)._node_ids[1].

way = r.ways[0]
r2 = api.query("""
node(id:6919917003, 45736074, 989303374, 45727345, 45725196, 989303587, 45721681, 989303457, 45716798, 45715162, 45713306);
out center;
""")
print(r2)
print(r2.nodes[0].lat)

for node in r2.nodes:
    print(node.lat,",", node.lon)

coords  = []
coords += [(float(node.lon), float(node.lat))
           for node in r.nodes]
coords += [(float(way.center_lat), float(way.center_lon))
           for way in r.ways]
coords += [(float(rel.center_lon), float(rel.center_lat))
           for rel in r.relations]

print(coords)

r3 = api.query("""
area["name"="Nederland"]->.boundaryarea;
(
nwr(area.boundaryarea)[name="Vredebestlaan"];
);
out center;
""")
print(r3)
for way in r3.ways:
    print(way.center_lat, way.center_lon)
