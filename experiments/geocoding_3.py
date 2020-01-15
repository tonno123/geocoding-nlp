import overpy
import time

api = overpy.Overpass()
r3 = api.query("""
area["name"="Breda"]->.boundaryarea;
(
nwr(area.boundaryarea)[name="Nieuwe Kadijk"];
);
out center;
""")
print(r3)
nodeCoordList = []
for way in r3.ways:
    print(", ".join(str(e) for e in way._node_ids))
    r4 = api.query("""
    node(id: %s);
    out center;
    """ % (", ".join(str(e) for e in way._node_ids) ) )
    time.sleep(1)
    for node in r4.nodes:
        nodeCoordList.append((node.lat, node.lon))
print(nodeCoordList)
