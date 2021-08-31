#!/usr/bin/env python2

# Random placement helpers because I'm tired of using spreadsheets for doing this
#
# Kevin Cuzner

import math
from pcbnew import *

	
def Place_xy(refdes, x, y):
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
	
	part = pcb.FindModuleByReference(refdes)
	
		#newPos = mm_to_pos(part.setPosition(), x_mm, y_mm) 
	part.SetPosition(wxPointMM(x, y))
		#part.SetOrientation(angle * -10)
		#if hide_ref is not None:
		#part.Reference().SetVisible(not hide_ref)


