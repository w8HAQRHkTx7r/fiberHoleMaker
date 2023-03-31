# Purpose: creates SVG file to burn holes into a plate to align fiber cables with LED matrix or strip

import requests
import sys
import json
from kmlsvg import svg_header, svg_footer
from pprint import pprint

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

SVG_FILE = "fiberMask.svg"

# Constants used in SVG_FILE
intercircle_offset =  10    # 16x16 matrix spacing

SVG_FILE = f"fiberMask_{intercircle_offset}.svg"
print(f'{SVG_FILE=}')

# Dimensions of the SVG track map
width =      11
height =     20

# Distance from the circle to its label
fiberCircleRadius  =   0.75

cx = 0
cy = 10

with open(SVG_FILE,"w") as svgfile:
	print(svg_header, file=svgfile)
	for holeCount in range(3):
		print(f'Hole: {holeCount}')
		cx += 10
		cy = 10

		inbound_circle =  f'''    <circle style="fill:none	;stroke:#ff0000;stroke-width:0.244187" id="hole{holeCount}" cx="{cx}" cy="{cy}" r="{fiberCircleRadius}"  />'''
		print(inbound_circle, file=svgfile)
		holeCount += 1

	print(svg_footer, file=svgfile)
