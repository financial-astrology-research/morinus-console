#!/usr/bin/env python

import astrology
import chart
import csv
import houses
import pickle
import planets
import pprint
import options
import transits
import pickle
import util
import time
import transits
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
    "ASCLON\tASCLAT\tASCDEC\tASCSP\t" \
    "MCLON\tMCLAT\tMCDEC\tMCSP\t"

with open('Hors/birthdates.csv', 'rb') as f:
    reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
    for row in reader:
        # Need to import for each iteration or it brokes
        import time
        dt = time.strptime(row['Date'], '%Y-%m-%d %H:%M:%S')
        # place, time and chart generation
        ny_place = chart.Place('New York', 74, 0, 21, False, 40, 42, 51, True, 10)
        year, month, day, hour, minute, second = dt.tm_year, dt.tm_mon, dt.tm_mday, dt.tm_hour, dt.tm_min, dt.tm_sec
        zone_hour, zone_minute, zone_second = util.decToDeg(float(row['ZH']))
        symbol = row['Symbol']
        time = chart.Time(year, month, day, hour, minute, second, False, astrology.SE_JUL_CAL, chart.Time.ZONE, False, zone_hour, 0, False, ny_place)
        chrt = chart.Chart(symbol, False, time, ny_place, opts.hsys, 'notes', opts)
        # Print chart positions
        printPlanetsData(chrt)
