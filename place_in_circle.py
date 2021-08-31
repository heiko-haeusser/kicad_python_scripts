#!/usr/bin/env python2

# Random placement helpers because I'm tired of using spreadsheets for doing this
#
# Kevin Cuzner

import math
from pcbnew import *

	
def place_circle(refdes, start_angle, center, radius, component_offset=0, hide_ref=True, lock=False):
	"""
	Places components in a circle
	refdes: List of component references
	start_angle: Starting angle
	center: Tuple of (x, y) mm of circle center
	radius: Radius of the circle in mm
	component_offset: Offset in degrees for each component to add to angle
	hide_ref: Hides the reference if true, leaves it be if None
	lock: Locks the footprint if true
	"""
	
	pcb = GetBoard()
	#print "Refdes=", refdes
	#print "enumerate Refdes=", enumerate(refdes)
	deg_per_idx = 360 / len(refdes)
	idx = 0;
	for rd in refdes:
		part = pcb.FindModuleByReference(refdes[idx])
		angle = (deg_per_idx * idx + start_angle) % 360;
		print "Cpm: ", part.GetReference(), "angle", angle
		x_mm = center[0] + math.cos(math.radians(angle)) * radius
		y_mm = center[1] + math.sin(math.radians(angle)) * radius

		#print("center_x", center[0], "x=", x_mm)
		#print("center_x", center[1], "y=", y_mm)

		#newPos = mm_to_pos(part.setPosition(), x_mm, y_mm) 
		part.SetPosition(wxPointMM(x_mm, y_mm))
		part.SetOrientation(0)
		#if hide_ref is not None:
		#part.Reference().SetVisible(not hide_ref)
		idx=idx+1
	#print "Placement finished. Press F11 to refresh."
