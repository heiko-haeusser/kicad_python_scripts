#!/usr/bin/env python2

# Random placement helpers because I'm tired of using spreadsheets for doing this
# place_trace_and_via.py
# Kevin Cuzner

import math
#from pcbnew import *
import pcbnew

printMsgs = 0

pcb = pcbnew.GetBoard()

def parse_layers(pcb):
	p_cnt = 0
	top_cu = 0
	bot_cu = 0
	top_silk = 0
	bot_silk = 0
	print "layer names --------------------------------------------------------------\n"

	while p_cnt < 99:
		if "BAD INDEX!" in pcb.GetLayerName(p_cnt):
			break
		#print "layer name: ", pcb.GetLayerName(p_cnt)
		if "B.Cu" in pcb.GetLayerName(p_cnt):
			print "Bottom copper layer is number ", p_cnt
			bot_cu = p_cnt
		if "F.Cu" in pcb.GetLayerName(p_cnt):
			print "Top copper layer is number ", p_cnt
			top_cu = p_cnt
		if "B.SilkS" in pcb.GetLayerName(p_cnt):
			print "Bottom silk layer is number ", p_cnt
			bot_silk = p_cnt
		if "F.SilkS" in pcb.GetLayerName(p_cnt):
			print "Top silk layer is number ", p_cnt
			top_silk = p_cnt
		p_cnt = p_cnt+1
	
	print "###########################################################################\n"

	return [top_cu, bot_cu, top_silk, bot_silk]

layers = parse_layers(pcb)

def mm_to_nm(mm):
	return mm*1000000.0

def nm_to_mm(mm):
	return mm/1000000.0
	
def place_Track(xy_start, xy_end, net, layer):
	if printMsgs == 1:
		print "place track with net_name: ", net.GetNetname(), " on layer: ", pcb.GetLayerName(layer)
		print "x_start: ", xy_start[0]
		print "x_end: ", xy_end[0]
		print " " 
		print "y_start: ", xy_start[1]
		print "y_end: ", xy_end[1]
		print " " 
	t = pcbnew.TRACK(pcb)
	pcb.Add(t)
	t.SetStart(pcbnew.wxPointMM(xy_start[0], xy_start[1]))
	t.SetEnd(pcbnew.wxPointMM(xy_end[0], xy_end[1]))
	t.SetLayer(0)
	t.SetNet(net)
	t.SetWidth(int(mm_to_nm(0.7)))
	if "GND" in net.GetNetname():
		if printMsgs == 1:
			print "place via with net_name: ", net.GetNetname(), " x= ", xy_end[0], " y= ", xy_end[1]
		v = pcbnew.VIA(pcb)
		pcb.Add(v)
		v.SetPosition(pcbnew.wxPointMM(xy_end[0], xy_end[1]))
		v.SetLayerPair(layers[0], layers[1])
		v.SetNet(net)
		v.SetDrill(int(mm_to_nm(0.4)))
		v.SetWidth(int(mm_to_nm(0.8)))

def get_Pad_Position(pad):
	x = nm_to_mm(pad.GetPosition().x)
	y = nm_to_mm(pad.GetPosition().y)
	return [x, y]

def get_xy_for_R(refdes):
	pcb = pcbnew.GetBoard()
	part = pcb.FindModuleByReference(refdes)
	a_pads = part.Pads()
	x = 0
	y = 0
	for pad in a_pads:
		a_netName = pad.GetNet().GetNetname()
		if "V" not in a_netName:
			xy = get_Pad_Position(pad)
			if printMsgs == 1:
				print "Resistor x= ", xy[0] , " y= ", xy[1]
			
		#else:
			#Connection to R here
	return xy

def Place_Tracks_And_Vias_Diode(part):
	a_pads = part.Pads()
	for pad in a_pads:
		a_netName = pad.GetNet().GetNetname()
		xy = get_Pad_Position(pad)
		if "GND" in a_netName:
			#GND connection with via here
			if printMsgs == 1:
				print "GND connection for Diode --------------------------------------------------\n"
				print "place GND connection with via on ", part.GetReference()
				print "Diode GND x= ", xy[0] , " y= ", xy[1]
			place_Track(xy, [xy[0], xy[1]+2], pad.GetNet(), layers[0])
			if printMsgs == 1:
				print "###########################################################################\n"
		else:
			if printMsgs == 1:
				print "place connection between R and D ------------------------------------------\n"
				print "place connection between R and D: ", part.GetReference()
				print "Diode    x= ", xy[0] , " y= ", xy[1]
			xy_R = get_xy_for_R(part.GetReference().replace('D', 'R'))#Connection to R here
			place_Track(xy, xy_R, pad.GetNet(), layers[0])
			if printMsgs == 1:
				print "###########################################################################\n"



def Place_Tracks_And_Vias(refdes):
	for ref in refdes:
		part = pcb.FindModuleByReference(ref)
		
		if part.GetReference().startswith('D'):
			Place_Tracks_And_Vias_Diode(part)



#Place_Tracks_And_Vias(['DF201'])
#Place_Tracks_And_Vias(['RF201'])
#pcbnew.Refresh()