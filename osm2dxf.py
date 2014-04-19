from dxfwrite import DXFEngine as dxf
import libxml2
import sys
import operator
from math import pi, tan, log

def generate_dxf(filename, tags):
    lat2y = lambda lat: (180/pi * log(tan(pi/4+lat*(pi/180)/2)))
    
    drawing = dxf.drawing(filename + ".dxf")
    xml = libxml2.parseFile(filename)
    context = xml.xpathNewContext()

    for tag in tags:
        layer_name = tag.upper()
        paths = context.xpathEval("/*/way[tag/@k = '%s']" %(tag))
        
        drawing.add_layer(layer_name)
        
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
        
        print "found %d nodes for %s, cached them" %(len(lat), layer_name)
        print "found %d paths" %(len(paths))
        
        for path in paths:
            # check if path has elevation information
            ele = path.xpathEval("tag[@k = 'ele']")
            if len(ele) == 0:
                elevation = 0.0
            else:
                elevation = float(ele[0].prop('v'))

            # find all nodes in path
            nodes = path.xpathEval("nd")
        
            points = []
            closed_path = False

            for node in nodes:
                if lon.has_key(node.prop('ref')) and lat.has_key(node.prop('ref')):
                    points.append( (long2coord(lon[node.prop('ref')]), lat2coord(lat[node.prop('ref')]), float(elevation)/15.0) )
                else:
                    print("Key %s not found in lat or long dict! Skipping...")

            polyline = dxf.polyline(points, layer=layer_name)
            
            if nodes[-1].prop('ref') == nodes[0].prop('ref'):
                closed_path = True
                polyline.close(status=True)
        
            print "Writing %s path for layer %s with elevation=%dm, %d nodes" %("closed" if closed_path else "", layer_name, elevation, len(nodes))
            drawing.add(polyline)
        
    print "Saving file..."
    drawing.save()
    print "Done."

def main(argv):
    filename = argv[1]
    tags = argv[2].split(",")
    
    print("generating %s from %s with tags %s..." %(filename + ".dxf", filename, str(tags)))
    generate_dxf(filename ,tags)

if __name__ == "__main__":
    main(sys.argv)
