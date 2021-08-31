#!/usr/bin/env python2

# Random placement helpers because I'm tired of using spreadsheets for doing this
#
# Kevin Cuzner

import math
import pcbnew
from pcbnew import *

# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'D:\kicad_python_scripts')

import place_in_circle
sys.path.insert(2, 'D:\kicad_python_scripts')

import place_xy

sys.path.insert(3, 'D:\kicad_python_scripts')

import place_trace_and_via

#Variables --------------------------------------------------------------------
start_x = 43.0
start_y = 12.975

R_off_x = 0.65-0.45
R_off_y = -3

field_size = 74.0

radius_DL = 6.25
radius_DM = 14.5
radius_DF = 24

ang_DL = 45
ang_DM = 0
ang_DF = 45

fields = ['2', '3', '4', '5', '6', '7']
conn_Rs = ['R101', 'R102', 'R103', 'R104', 'R105', 'R106']

arr_DF = ["DF*01", "DF*02", "DF*03", "DF*04", "DF*05", "DF*06", "DF*07", "DF*08", "DF*09", "DF*10", "DF*11", "DF*12"]
arr_DM = ["DM*01", "DM*02", "DM*03", "DM*04", "DM*05", "DM*06", "DM*07", "DM*08"]
arr_DL = ["DL*01", "DL*02", "DL*03", "DL*04"]

arr_RF = ["RF*01", "RF*02", "RF*03", "RF*04", "RF*05", "RF*06", "RF*07", "RF*08", "RF*09", "RF*10", "RF*11", "RF*12"]
arr_RM = ["RM*01", "RM*02", "RM*03", "RM*04", "RM*05", "RM*06", "RM*07", "RM*08"]
arr_RL = ["RL*01", "RL*02", "RL*03", "RL*04"]
#DF r=6, Angle 45
#DM r=14 Angle 0
#DL r=23 Angle 22.5

#End Variables ----------------------------------------------------------------
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Functions --------------------------------------------------------------------

def replaceArr(arr, idx):
	res = []
	for item in arr:
		res.append(item.replace('*',idx))
	
	return res
	
def changeSyntax(center_x, center_y, idx):
	place_in_circle.place_circle(replaceArr(arr_DL, idx), ang_DL, (center_x, center_y), radius_DL)
	place_in_circle.place_circle(replaceArr(arr_DM, idx), ang_DM, (center_x, center_y), radius_DM)
	place_in_circle.place_circle(replaceArr(arr_DF, idx), ang_DF, (center_x, center_y), radius_DF)
	
	place_in_circle.place_circle(replaceArr(arr_RL, idx), ang_DL, (center_x+R_off_x, center_y+R_off_y), radius_DL)
	place_in_circle.place_circle(replaceArr(arr_RM, idx), ang_DM, (center_x+R_off_x, center_y+R_off_y), radius_DM)
	place_in_circle.place_circle(replaceArr(arr_RF, idx), ang_DF, (center_x+R_off_x, center_y+R_off_y), radius_DF)
	
	place_trace_and_via.Place_Tracks_And_Vias(replaceArr(arr_DL, idx));
	place_trace_and_via.Place_Tracks_And_Vias(replaceArr(arr_DM, idx));
	place_trace_and_via.Place_Tracks_And_Vias(replaceArr(arr_DF, idx));

#End Functions ----------------------------------------------------------------
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



#Place diodes and resistors
def place_all():	
	cnt = 0;
	for i in fields:
		#print i
		if cnt < 3:
			changeSyntax(80.0 + (cnt*field_size), 50.0,i)
		else:
			changeSyntax(80.0 + ((cnt-3)*field_size), 50.0 + field_size,i)
		cnt = cnt+1
	
	Refresh()
	

#Resistors which connect GND and VBat planes with the letter field
def place_all_conn_Rs():
	cntRc = 0;
	for iRc in conn_Rs:
		#print iRc
		if cntRc < 3:
			place_xy.Place_xy(iRc, 65.5 + (cntRc*field_size), 75.25)
			
		else:
			place_xy.Place_xy(iRc, 65.5 + ((cntRc-3)*field_size), 74.25 + field_size)
		cntRc = cntRc+1
	

#Cleanup existing tracks ----------------------------------------------------------------

pcb = pcbnew.GetBoard()
tracks = pcb.GetTracks()
for t in tracks:
    if t.GetLayer() == 0:
		#print t.GetNetname()
		pcb.Delete(t)
		
#vias = pcb.GetVias()
#for v in vias:
	#pcb.Delete(v)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


place_all_conn_Rs() #Resistors which connect GND and VBat planes with the letter field
place_all()

Refresh()

#place_xy.Place_xy('R101',65.5,75.25)
#print changeSyntax(80.0, 50.0,'3')
#print changeSyntax(80.0, 50.0,'3')
#print changeSyntax(80.0, 50.0,'3')
