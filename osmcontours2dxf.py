from dxfwrite import DXFEngine as dxf
import libxml2
import sys
import operator
from math import pi, tan, log

lat2y = lambda lat: (180/pi * log(tan(pi/4+lat*(pi/180)/2)))

drawing = dxf.drawing("contours.dxf")
xml = libxml2.parseFile(sys.argv[1])
context = xml.xpathNewContext()
contour_ways = context.xpathEval("/*/way[tag/@k = 'contour']")

drawing.add_layer("CONTOURS")

n = context.xpathEval("/*/node")
lat = {}
lon = {}

for node in n:
    lat[node.prop('id')] = float(node.prop('lat'))
    lon[node.prop('id')] = float(node.prop('lon'))

xmax = max(lon.iteritems(), key=operator.itemgetter(1))[1]
xmin = min(lon.iteritems(), key=operator.itemgetter(1))[1]
ymax = max(lat.iteritems(), key=operator.itemgetter(1))[1]
ymin = min(lat.iteritems(), key=operator.itemgetter(1))[1]

print("Rectangle: [%f, %f], [%f, %f]" % (xmin, xmax, ymin, ymax))

masterscale = 500/(xmax-xmin)
baselong = xmin
basey = lat2y(ymin)

lat2coord = lambda lat: (lat2y(lat)-basey)*masterscale
long2coord = lambda lon: (lon-baselong)*masterscale

print "found " + str(len(lat)) + " nodes, cached them"
print "found " + str(len(contour_ways)) + " contours"

for contour in contour_ways:
    elevation = str(contour.xpathEval("tag[@k = 'ele']")[0].prop('v'))
    nodes = contour.xpathEval("nd")

    points = []
    for node in nodes:
        points.append( (long2coord(lon[node.prop('ref')]), lat2coord(lat[node.prop('ref')]), float(elevation)) )

    print "Writing contour with elevation=" + elevation + "m, " + str(len(nodes)) + " nodes"
    drawing.add(dxf.polyline(points, layer='CONTOURS'))

print "Saving file..."
drawing.save()
print "Done."
