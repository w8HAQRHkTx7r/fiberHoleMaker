# Contains long f-strings with XML headers and footers for KML and SVG files
# Primarily for the CTA project, but can be adapted easily.  Specific objects
# are supplied between a header and footer.

kml_header = f'''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">
    <Document id="1">
        <open>1</open>
        <LookAt>
           <longitude>-87.6</longitude>
           <latitude>41.9</latitude>
           <altitude>62000</altitude>
           <heading>0</heading>
           <tilt>0</tilt>
           <altitudeMode>relativeToGround</altitudeMode>
           <roll>0</roll>
        </LookAt>
        <Style id="5">
            <IconStyle id="7">
                <colorMode>normal</colorMode>
                <scale>1</scale>
                <heading>0</heading>
                <Icon id="8">
                    <href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>
                </Icon>
            </IconStyle>
            <LabelStyle id="6">
                <color>ff00ffff</color>
                <colorMode>normal</colorMode>
                <scale>1</scale>
            </LabelStyle>
            <LineStyle>
		        <color>ffff00ff</color>
        		<width>5</width>
		    </LineStyle>

            <PolyStyle> <color>33ff00ff</color> <outline>1</outline> </PolyStyle>

        </Style>
        <name>DOCUMENTNAME</name>
'''

kml_footer = f'''    </Document>
</kml>
'''

svg_header = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   width="210mm"
   height="297mm"
   viewBox="0 0 210 297"
   version="1.1"
   id="svg5"
   inkscape:version="1.2.1 (9c6d41e4, 2022-07-14)"
   sodipodi:docname="ctaTrackMap.svg"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <sodipodi:namedview
     id="namedview7"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:showpageshadow="2"
     inkscape:pageopacity="0.0"
     inkscape:pagecheckerboard="0"
     inkscape:deskcolor="#d1d1d1"
     inkscape:document-units="mm"
     showgrid="false"
     inkscape:zoom="1"
     inkscape:cx="475.5"
     inkscape:cy="45.5"
     inkscape:window-width="1280"
     inkscape:window-height="699"
     inkscape:window-x="0"
     inkscape:window-y="25"
     inkscape:window-maximized="0"
     inkscape:current-layer="layer1" />
  <defs
     id="defs2" />
  <g
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     id="layer1">
'''

svg_footer = f'''	</g>
	</svg>
	'''
