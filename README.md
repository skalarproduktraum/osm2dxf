osm2dxf - Convert OpenStreetMap data to AutoCAD DXF
===================================================

osm2dxf is a simple XPath-based converter to translate from OpenStreetMap files
to AutoCAD DXF. Call it via

```bash
python ./osm2dxf.py filename.osm building,waterway,contour
```

This will create a new file, `filename.osm.dxf`, with separate layers for the
building, waterway and contour tags. If SRTM height data is available in the
OSM file, it'll be added with the corresponding height in Z.

A full list of possible tags is available in the OpenStreetMap wiki page on 
[Map features](https://wiki.openstreetmap.org/wiki/Map_features).

The value of `masterscale` within the file `osm2dxf.py` might need to be 
adjusted from the default of 500 for your needs. For example, when opening DXF
files in [LibreCAD](https://librecad.org/) to create maps, a value of 0.96 
multiplied by the scale of the map you require appears to produce dimensions 
consistent with the OpenStreetMap web interface. So, if your map is to be 
printed at 1:5000 scale, a value of 4800 for `masterscale` seems to work. 
Dimensions can be checked with the _Distance Point to Point_ tool in LibreCAD.

## Requirements

osm2dxf requires dxfwrite and libxml2 modules to be installed.
