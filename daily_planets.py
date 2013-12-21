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


def dailyPlanets(chrt, start_year, start_month, end_year, end_month):
    for year in range(start_year, end_year):
        for month in range(start_month, end_month+1):
            for day in range(1, 32):
                if util.checkDate(year, month, day):
                    calculateDailyChart(chrt, year, month, day)
                else:
                    break


def calculateDailyChart(chrt, year, month, day):
    hour = 2
    day_time = chart.Time(year, month, day, hour, 0, 0, chrt.time.bc, chrt.time.cal, chrt.time.zt, chrt.time.plus, chrt.time.zh, chrt.time.zm, chrt.time.daylightsaving, chrt.place)
    day_chart = chart.Chart(chrt.name, chrt.male, day_time, chrt.place, chrt.htype, chrt.notes, chrt.options)
    printPlanetsData(day_chart)

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

    for asteroid in chrt.asteroids.asteroids:
        lon = asteroid.data[planets.Planet.LONG]
        lat = asteroid.data[planets.Planet.LAT]
        speed = asteroid.data[planets.Planet.SPLON]
        out.append("%.2f\t%.2f\t%.3f\t" % (lon, lat, speed))

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
astrology.swe_set_ephe_path('/Applications/Morinus.app/Contents/Resources/SWEP/Ephem')
# instance of place, time and chart generation
place = chart.Place(place, deglon, minlon, 0, east, deglat, minlat, seclat, north, altitude)
time = chart.Time(year, month, day, hour, minute, second, bc, cal, zt, plus, zh, zm, daylightsaving, place)
chrt = chart.Chart(name, male, time, place, htype, notes, opts)

print "Date\t" \
    "SULON\tSULAT\tSUSP\tSUASC\tSUMC\tSUDESC\tSUIC\t" \
    "MOLON\tMOLAT\tMOSP\tMOASC\tMOMC\tMODESC\tMOIC\t" \
    "MELON\tMELAT\tMESP\tMEASC\tMEMC\tMEDESC\tMEIC\t" \
    "VELON\tVELAT\tVESP\tVEASC\tVEMC\tVEDESC\tVEIC\t" \
    "MALON\tMALAT\tMASP\tMAASC\tMAMC\tMADESC\tMAIC\t" \
    "JULON\tJULAT\tJUSP\tJUASC\tJUMC\tJUDESC\tJUIC\t" \
    "SALON\tSALAT\tSASP\tSAASC\tSAMC\tSADESC\tSAIC\t" \
    "URLON\tURLAT\tURSP\tURASC\tURMC\tURDESC\tURIC\t" \
    "NELON\tNELAT\tNESP\tNEASC\tNEMC\tNEDESC\tNEIC\t" \
    "PLLON\tPLLAT\tPLSP\tPLASC\tPLMC\tPLDESC\tPLIC\t" \
    "NNLON\tNNLAT\tNNSP\tNNASC\tNNMC\tNNDESC\tNNIC\t" \
    "SNLON\tSNLAT\tSNSP\tSNASC\tSNMC\tSNDESC\tSNIC\t" \
    "CELON\tCELAT\tCESP\t" \
    "CHLON\tCHLAT\tCHSP\t" \
    "JNLON\tJNLAT\tJNSP\t" \
    "PALON\tPALAT\tPASP\t" \
    "PHLON\tPHLAT\tPHSP\t" \
    "VSLON\tVSLAT\tVSSP\t"

dailyPlanets(chrt, 1950, 1, 2030, 12)
