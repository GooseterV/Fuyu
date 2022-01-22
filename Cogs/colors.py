import colorsys
import math

import cv2
import numpy as np
import pyspectrum
from colormath.color_conversions import RGB_to_XYZ, convert_color
from colormath.color_objects import LabColor, LuvColor, XYZColor, sRGBColor

rgb_scale = 255
cmyk_scale = 100

def rgb_to_cmyk(r,g,b):
	if (r == 0) and (g == 0) and (b == 0):
		# black
		return 0, 0, 0, cmyk_scale

	# rgb [0,255] -> cmy [0,1]
	c = 1 - r / float(rgb_scale)
	m = 1 - g / float(rgb_scale)
	y = 1 - b / float(rgb_scale)

	# extract out k [0,1]
	min_cmy = min(c, m, y)
	c = (c - min_cmy) 
	m = (m - min_cmy) 
	y = (y - min_cmy) 
	k = min_cmy

	# rescale to the range [0,cmyk_scale]
	return (round(c*cmyk_scale), round(m*cmyk_scale), round(y*cmyk_scale), round(k*cmyk_scale))

def cmyk_to_rgb(c,m,y,k):
	r = round(rgb_scale*(1.0-(c+k)/float(cmyk_scale)))
	g = round(rgb_scale*(1.0-(m+k)/float(cmyk_scale)))
	b = round(rgb_scale*(1.0-(y+k)/float(cmyk_scale)))
	return (r,g,b)

def hex_to_rgb(hex):
	return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r,g,b):
	return "{:02x}{:02x}{:02x}".format(r, g, b)

def hex_to_decimal(hex_string):
	return int(hex_string, 16)

def decimal_to_hex(decimal):
	return hex(decimal).replace("0x", "")


def rgb_to_ycc(r, g, b): 
    y = .299*r + .587*g + .114*b
    cb = 128 -.168736*r -.331364*g + .5*b
    cr = 128 +.5*r - .418688*g - .081312*b
    return round(y), round(cb), round(cr)
def rgb_to_xyz(r, g, b):
	rgb = sRGBColor(rgb_r=r, rgb_g=g, rgb_b=b, is_upscaled=True)
	return RGB_to_XYZ(rgb, target_illuminant="d55").get_value_tuple()
def rgb_to_lab(r, g, b):
	rgb = sRGBColor(rgb_r=r, rgb_g=g, rgb_b=b, is_upscaled=True)
	return convert_color(rgb, LabColor, observer='2', illuminant='d50').get_value_tuple()
def rgb_to_luv(r, g, b):
	rgb = sRGBColor(rgb_r=r, rgb_g=g, rgb_b=b, is_upscaled=True)
	return convert_color(rgb, LuvColor).get_value_tuple()
def testColors():
	print(decimal_to_hex(3468132))
	print(hex_to_decimal("34eb64"))
	print(hex_to_rgb("34eb64"))
	print(rgb_to_hex(52, 235, 100))
	print(rgb_to_cmyk(52, 235, 100))
	print(cmyk_to_rgb(73, 0, 53, 8))
	print(rgb_to_lab(255, 0, 0))
	print(rgb_to_xyz(255, 0, 0))
	print(rgb_to_luv(255, 0, 0))


c = pyspectrum.Colors()
to_mix = [
	c.RGB(52, 152, 219),
	c.RGB(32, 102, 148)
]
mixed = c.mix_colors(to_mix)

#print(mixed.to_hex().to_string())