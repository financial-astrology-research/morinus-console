#!/usr/bin/env python

import astrology
import chart
import csv
import graphchart
import houses
import morin
import mtexts
import options
import options
import pickle
import planets
import sys
import time
import transits
import util
import wx
from inspect import getmembers
from pprint import pprint
from printr import printr
from sys import exit

def printPlanetsData(chrt):
    out = []
    out.append("%s\t" % (chrt.name))
    out.append("%d-%d-%d %d:%d\t" % (chrt.time.year, chrt.time.month, chrt.time.day, chrt.time.hour, chrt.time.minute))

    for j in range (planets.Planets.PLANETS_NUM):
        lon = chrt.planets.planets[j].data[planets.Planet.LONG]
        lat = chrt.planets.planets[j].data[planets.Planet.LAT]
        speed = chrt.planets.planets[j].data[planets.Planet.SPLON]
        decl = chrt.planets.planets[j].dataEqu[1]
        #riseset = chrt.riseset.planetRiseSet(j)
        out.append("%.2f\t%.2f\t%.2f\t%.3f\t" % (lon, lat, decl, speed))

    # ASC / MC positions
    ASC = chrt.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON], chrt.houses.ascmc2[houses.Houses.ASC][houses.Houses.LAT], chrt.houses.ascmc2[houses.Houses.ASC][houses.Houses.DECL]
    out.append("%.2f\t%.2f\t%.2f\t%.3f\t" % (ASC[0], ASC[1], ASC[2], 0))
    MC = chrt.houses.ascmc2[houses.Houses.MC][houses.Houses.LON], chrt.houses.ascmc2[houses.Houses.MC][houses.Houses.LAT], chrt.houses.ascmc2[houses.Houses.MC][houses.Houses.DECL]
    out.append("%.2f\t%.2f\t%.2f\t%.3f\t" % (MC[0], MC[1], MC[2], 0))
    # print out
    print ''.join(out)


class Morinus(wx.App):
	def OnInit(self):
		try:
			progPath = os.path.dirname(sys.argv[0])
			os.chdir(progPath)
		except:
			pass

		wx.SetDefaultPyEncoding('utf-8')
		opts = options.Options()
		mtexts.setLang(opts.langid)
		frame = morin.NFrame(None, -1, mtexts.txts['Morinus'], opts)
		#frame.Show(True)
		return True

app = Morinus(0)
opts = options.Options()
opts.def_hsys = opts.hsys = 'B'

# Headers
print "Symbol\tDate\t" \
    "SULON\tSULAT\tSUDEC\tSUSP\t" \
    "MOLON\tMOLAT\tMODEC\tMOSP\t" \
    "MELON\tMELAT\tMEDEC\tMESP\t" \
    "VELON\tVELAT\tVEDEC\tVESP\t" \
    "MALON\tMALAT\tMADEC\tMASP\t" \
    "JULON\tJULAT\tJUDEC\tJUSP\t" \
    "SALON\tSALAT\tSADEC\tSASP\t" \
    "URLON\tURLAT\tURDEC\tURSP\t" \
    "NELON\tNELAT\tNEDEC\tNESP\t" \
    "PLLON\tPLLAT\tPLDEC\tPLSP\t" \
    "NNLON\tNNLAT\tNNDEC\tNNSP\t" \
    "SNLON\tSNLAT\tSNDEC\tSNSP\t" \
    "ASLON\tASLAT\tASDEC\tASSP\t" \
    "MCLON\tMCLAT\tMCDEC\tMCSP\t" \
    "FILE"

# Need to import for each iteration or it brokes
import time
chart_name = sys.argv[1]
bdate = sys.argv[2]
btime = sys.argv[3]
lat = sys.argv[4]
lon = sys.argv[5]
tz = sys.argv[6]
dt = time.strptime(bdate + ' ' + btime, '%Y-%m-%d %H:%M')
north = True
east = True
altitude = 0

#long
idx = lon.find(u'E')#
if idx == -1:
  idx = lon.find(u'W')#
  east = False

if idx == -1:
  print("Invalid lon string provided")
  sys.exit()
else:
  deglon = int(lon[0:idx])
  idx += 1
  degmin = int(lon[idx:])

#lat
idx = lat.find(u'N')#
if idx == -1:
  idx = lat.find(u'S')#
  north = False

if idx == -1:
  print("Invalid lat string provided")
  sys.exit()
else:
  latdeg = int(lat[0:idx])
  idx += 1
  latmin = int(lat[idx:])

# place, time and chart generation
place = chart.Place('Place Name', deglon, degmin, 0, east, latdeg, latmin, 0, north, altitude)
year, month, day, hour, minute, second = dt.tm_year, dt.tm_mon, dt.tm_mday, dt.tm_hour, dt.tm_min, dt.tm_sec
#place.tz
tzh, tzm, tzs = util.decToDeg(float(tz))
if tz[0] == '-':
  tzplus = False
else:
  tzplus = True

time = chart.Time(year, month, day, hour, minute, second, False, astrology.SE_JUL_CAL, chart.Time.ZONE, tzplus, tzh, tzm, False, place)
chrt = chart.Chart(chart_name, False, time, place, opts.hsys, 'notes', opts)
gchart = graphchart.GraphChart(chrt, [800, 800], opts, True)
mybuffer = gchart.drawChart()
fname = "/tmp/chart_" + chart_name + ".jpg"
mybuffer.SaveFile(fname, wx.BITMAP_TYPE_JPEG)
# Print chart positions
printPlanetsData(chrt)
print("\t" + fname)
