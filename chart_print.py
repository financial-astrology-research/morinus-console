#!/usr/bin/env python

import astrology
import chart
import pickle
import planets
import pprint
import options
import transits
import pickle
import util
import transits
from inspect import getmembers
from pprint import pprint
from printr import printr

def printPlanetsData(chrt):
    out = []
    out.append("%d-%d-%d %d:%d\t" % (chrt.time.year, chrt.time.month, chrt.time.day, chrt.time.hour, chrt.time.minute))

    for j in range (planets.Planets.PLANETS_NUM):
        lon = chrt.planets.planets[j].data[planets.Planet.LONG]
        lat = chrt.planets.planets[j].data[planets.Planet.LAT]
        speed = chrt.planets.planets[j].data[planets.Planet.SPLON]
        decl = chrt.planets.planets[j].dataEqu[1]
        #riseset = chrt.riseset.planetRiseSet(j)
        out.append("%.2f\t%.2f\t%.2f\t%.3f\t" % (lon, lat, decl, speed))

    print ''.join(out)

opts = options.Options()
opts.def_hsys = opts.hsys = 'B'
# place, time and chart generation
ny_place = chart.Place('New York', 74, 0, 21, False, 40, 42, 51, True, 10)
year, month, day, hour, minute, second = 2014, 5, 29, 11, 0, 0
zone_hour, zone_minute = 5, 0
symbol = 'Today'
time = chart.Time(year, month, day, hour, minute, second, False, astrology.SE_JUL_CAL, chart.Time.ZONE, False, zone_hour, 0, False, ny_place)
chrt = chart.Chart(symbol, False, time, ny_place, opts.hsys, 'notes', opts)

print "Date\t" \
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
    "SNLON\tSNLAT\tSNDEC\tSNSP\t"

printPlanetsData(chrt)
