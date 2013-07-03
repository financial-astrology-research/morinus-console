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
    out.append("%d-%d-%d\t" % (chrt.time.year, chrt.time.month, chrt.time.day))

    for j in range (planets.Planets.PLANETS_NUM):
        lon = chrt.planets.planets[j].data[planets.Planet.LONG]
        lat = chrt.planets.planets[j].data[planets.Planet.LAT]
        speed = chrt.planets.planets[j].data[planets.Planet.SPLON]
        name = chrt.planets.planets[j].name
        riseset = chrt.riseset.planetRiseSet(j)
        out.append("%.2f\t%.2f\t%.3f\t%s\t%s\t%s\t%s\t" % (lon, lat, speed, riseset[0], riseset[1], riseset[2], riseset[3]))

    print ''.join(out)

fpath = "/Users/pablocc/Hors/EUR born.hor"
chrt = None

try:
    f = open(fpath, 'rb')
    name = pickle.load(f)
    male = pickle.load(f)
    htype = pickle.load(f)
    bc = pickle.load(f)
    year = pickle.load(f)
    month = pickle.load(f)
    day = pickle.load(f)
    hour = pickle.load(f)
    minute = pickle.load(f)
    second = pickle.load(f)
    cal = pickle.load(f)
    zt = pickle.load(f)
    plus = pickle.load(f)
    zh = pickle.load(f)
    zm = pickle.load(f)
    daylightsaving = pickle.load(f)
    place = pickle.load(f)
    deglon = pickle.load(f)
    minlon = pickle.load(f)
    seclon = pickle.load(f)
    east = pickle.load(f)
    deglat = pickle.load(f)
    minlat = pickle.load(f)
    seclat = pickle.load(f)
    north = pickle.load(f)
    altitude = pickle.load(f)
    notes = pickle.load(f)
    f.close()

except IOError:
    print "error loading the chart"

opts = options.Options()
# instance of place, time and chart generation
place = chart.Place(place, deglon, minlon, 0, east, deglat, minlat, seclat, north, altitude)
time = chart.Time(year, month, day, hour, minute, second, bc, cal, zt, plus, zh, zm, daylightsaving, place)
chrt = chart.Chart(name, male, time, place, htype, notes, opts)

print "Date\t" \
    "SULON\tSULAT\tSUSP\t" \
    "MOLON\tMOLAT\tMOSP\t" \
    "MELON\tMELAT\tMESP\t" \
    "VELON\tVELAT\tVESP\t" \
    "MALON\tMALAT\tMASP\t" \
    "JULON\tJULAT\tJUSP\t" \
    "SALON\tSALAT\tSASP\t" \
    "URLON\tURLAT\tURSP\t" \
    "NELON\tNELAT\tNESP\t" \
    "PLLON\tPLLAT\tPLSP\t" \
    "NNLON\tNNLAT\tNNSP\t" \
    "SNLON\tSNLAT\tSNSP\t"

printPlanetsData(chrt)
