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
