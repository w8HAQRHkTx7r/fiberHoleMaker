# This program reads the CTA station/stop API (or a cached version) and creates
# both a KML and an SVG file that shows the locations and names of the CTA train
# stations.  There's an option to filter for combinations of lines.

import requests
import sys
import json
from kmlsvg import kml_header, kml_footer, svg_header, svg_footer
from pprint import pprint

# creates a bit mask for filtering CTA lines to print
def bitLines(stationData):
	bitPattern = 0
	if stationData['red']:
		bitPattern += 1
	if stationData['blue']:
		bitPattern += 2
	if stationData['g']:
		bitPattern += 4
	if stationData['brn']:
		bitPattern += 8
	if stationData['p']:
		bitPattern += 16
	if stationData['pexp']:
		bitPattern += 32
	if stationData['y']:
		bitPattern += 64
	if stationData['pnk']:
		bitPattern += 128
	if stationData['o']:
		bitPattern += 256
	return bitPattern
		
	
# Creates a function to map lat/long to a paper size
def make_interpolater(left_min, left_max, right_min, right_max): 
    # Figure out how 'wide' each range is  
    leftSpan = left_max - left_min  
    rightSpan = right_max - right_min  

    # Compute the scale factor between left and right values 
    scaleFactor = float(rightSpan) / float(leftSpan) 

    # create interpolation function using pre-calculated scaleFactor
    def interp_fn(value):
        return right_min + (value-left_min)*scaleFactor

    return interp_fn

KML_FILE = "ctaStations.kml"
SVG_FILE = "ctaTrackMap.svg"

# Bit Values Constants
RED =    1
BLUE =   2
G =      4
BRN =    8
P =     16
PEXP =  32
Y =     64
PNK =  128
O =    256

# Constants used in SVG_FILE
intercircle_offset =  6.88    # Measured on the larger 144/m strip

intercircle_offset =  6.6727  # Measured on the smaller 75/  strip
strip_width        =  7.00
SVG_FILE = f"ctaEqualSpaced{intercircle_offset}.svg"
print(f'{KML_FILE=} {SVG_FILE=}')

# Dimensions of the SVG track map
width =      11
height =     20

# Distance from the circle to its label
stationCircleRadius  =   1.25
stationFontSize      = 3.0
stationLabelXOffset  = stationCircleRadius * 3
stationLabelYOffset  = stationFontSize / 2.0
stationLabelRotation = -180.0

loop_Stations        = [40680,40380,40430,41160,40490,40330,40850,41490,40070,40560,41660,41340,40160,40460,41090,40790,40040,41400,40260,40370,41700,40730,]
red_or_purple_Stations = [40900,41190,40100,41300,40760,40880,41380,40340,41200,40770,40540,40080,41420,41320,41210,40530,41220,40650,40630,41450,40330,41660,41090,40560,41490,41400,41000,40190,41230,41170,40910,40990,40240,41430,40450]

# Run this section once to download the CTA data
# url = 'https://data.cityofchicago.org/resource/8pix-ypme.json'
# response = requests.get(url)
# data = response.json()
# json.dump(data, open("ctaAPIStations.json", "w"))

# The comment out the above section
# and run this instead
data = json.load(open("ctaAPIStations.json"))

minLat =  361
maxLat =   -1
minLon =  361
maxLon =  -361

# Create a dictionary of unique stations and their lat/lon coordinates
station_dict = {}
with open("ctaStations.kml","w") as kmlfile:
	print(kml_header, file=kmlfile)
	i = 0
	for row in data:
		stop = row['stop_id']
		staNm = row['station_name']
		staId = row['map_id']
		coords = (row['location']['longitude'], row['location']['latitude'])
		
		# Filter specific lines
		# Plot all stations
		interestingLine = True

		# Plot only selected Lines
		stationLines = bitLines(row)
		interestingLine = stationLines & (RED)
		# 
		# Plot only the Loop (or NOT loop)
		#interestingLine = (int(staId) in loop_Stations)
		interestingLine = (int(staId) in red_or_purple_Stations)
 

		if not interestingLine:
			continue

		# Because multiple lines share a station (which comprises multiple stops), the
		# station name and lat/lon appear multiple times. If we've seen a station and
		# coordinates before, don't add the dup.
		if coords in station_dict:
			next
		else:
			station_dict[coords] = (staNm, staId)

	for coords, (stationName, stationID) in station_dict.items():
		# Create a KML placemark
		station = f'''    <Placemark id="{row['map_id']}">
				<name>{stationName} {stationID}</name>
				<styleUrl>#5</styleUrl>
				<Point id="0">
					<coordinates>{coords[0]},{coords[1]},0</coordinates>
				</Point>
			</Placemark>'''
		print(station, file=kmlfile)

		minLon = min(minLon, float(coords[0]))
		maxLon = max(maxLon, float(coords[0]))
		minLat = min(minLat, float(coords[1]))
		maxLat = max(maxLat, float(coords[1]))

	print(kml_footer, file=kmlfile)

# Bounding Box Override
# minLon = 87.90422307
# maxLon = 87.605857
# minLat = 41.722377
# maxLat = 42.073153

print("Bounding box", file=sys.stderr)
print(f'W {minLon:=} E {maxLon:=} S {minLat:=} N {maxLat:=}', file=sys.stderr)

width_mm  = width  * 25.4  # mm / inch
height_mm = height * 25.4

width_scaler  = make_interpolater( minLon+1,  maxLon, 0, width_mm)
height_scaler = make_interpolater( maxLat+1,  minLat , 0, height_mm)

with open(SVG_FILE,"w") as svgfile:
	print(svg_header, file=svgfile)
	stationCount = 0
	for coords, (stationName, stationID) in sorted(station_dict.items(), key=lambda item: item[0][1], reverse = True):
		print(f'{coords}:{stationID}:{stationName}')
		cx = width_scaler(float(coords[0]))
		cy = height_scaler(float(coords[1]))
		cx = 10
		cy = stationCount * intercircle_offset * 2.0

		inbound_circle =  f'''    <circle style="fill:none	;stroke:#ff0000;stroke-width:0.244187" id="path{stationCount}" cx="{cx}" cy="{cy}" r="{stationCircleRadius}"  />'''
		outbound_circle = f'''    <circle style="fill:none	;stroke:#ff0000;stroke-width:0.244187" id="path{stationCount}" cx="{cx+strip_width}" cy="{cy}" r="{stationCircleRadius}"  />'''
		stationLabel = f'''    <text
		   xml:space="preserve" 
		   style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:{stationFontSize}px;line-height:1.25;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';fill:none;fill-opacity:1;stroke:#0000ff;stroke-width:0.264588"   
		   x="{cx + stationLabelXOffset}"   
		   y="{cy + stationLabelYOffset}" 
		   id="staId{stationID}"
		   transform="rotate({stationLabelRotation},{cx},{cy})"><tspan
			 sodipodi:role="line"
			 id="tspan{stationCount}"
			 style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:{stationFontSize}px;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';stroke-width:0.264588"
			 x="{cx + stationLabelXOffset}"
			 y="{cy + stationLabelYOffset}">{stationName}</tspan></text>'''

		inbound_tween = f'''    <circle style="fill:none	;stroke:#ff0000;stroke-width:0.244187" id="path{stationCount}" cx="{cx}" cy="{cy + intercircle_offset}" r="{stationCircleRadius}"  />		'''
		outbound_tween = f'''    <circle style="fill:none	;stroke:#ff0000;stroke-width:0.244187" id="path{stationCount}" cx="{cx+strip_width}" cy="{cy + intercircle_offset}" r="{stationCircleRadius}"  />		'''

		print(stationLabel, file=svgfile)
		print(inbound_circle, file=svgfile)
		print(outbound_circle, file=svgfile)
		print(inbound_tween, file=svgfile)
		print(outbound_tween, file=svgfile)
		stationCount += 1

	print(svg_footer, file=svgfile)
