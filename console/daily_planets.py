#!/usr/bin/env python

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from inspect import getmembers
from pprint import pprint
from printr import printr
from sys import exit
import astrology
import chart
import options
import pickle
import pickle
import planets
import pprint
import sys
import transits
import transits
import util

eclipses_cache = {}

def dailyPlanets(chrt, start_year, start_month, end_year, end_month, hour):
    for year in range(start_year, end_year):
        for month in range(start_month, end_month+1):
            for day in range(1, 32):
                if util.checkDate(year, month, day):
                    day_chart = calculateDailyChart(chrt, year, month, day, hour)
                    printPlanetsData(day_chart)
                    calculateNearestEclipse('sun', chrt, year, month, day, hour)
                    calculateNearestEclipse('moon', chrt, year, month, day, hour)
                    sys.stdout.write('\n')
                else:
                    break

def calculateNearestEclipse(ecplanet, chrt, year, month, day, hour, minute = 0, second = 0):
    out = []
    time = hour + minute / 60.0 + second / 3600.0
    tjd = swisseph.julday(year, month, day, time, astrology.SE_GREG_CAL)

    # Calculate the global eclipse nearest to the specified date
    if ecplanet == 'sun':
        retflag = swisseph.sol_eclipse_when_glob(tjd, astrology.SEFLG_SWIEPH, astrology.SE_ECL_ALLTYPES_SOLAR, True);
        planet_id = astrology.SE_SUN
    elif ecplanet == 'moon':
        retflag = swisseph.lun_eclipse_when(tjd, astrology.SEFLG_SWIEPH, astrology.SE_ECL_ALLTYPES_LUNAR, True);
        planet_id = astrology.SE_MOON
    else:
        print('No valid eclipse ecplanet input at calculateNearestEclipse\n')
        exit(1)

    # Get date and eclipse type
    ejd = retflag[1][0]
    eclflag = retflag[0][0]
    # Convert julian to gregorian date
    eyear, emonth, eday, ejtime = swisseph.revjul(ejd, astrology.SE_GREG_CAL)
    ehour, eminute, esecond = util.decToDeg(ejtime)

    if (eclflag & astrology.SE_ECL_TOTAL):
        ecltype = 'total'
    elif (eclflag & astrology.SE_ECL_ANNULAR):
        ecltype = 'annular'
    elif (eclflag & astrology.SE_ECL_ANNULAR_TOTAL):
        ecltype = 'anntotal'
    elif (eclflag & astrology.SE_ECL_PARTIAL):
        ecltype = 'partial'
    elif (eclflag & astrology.SE_ECL_PENUMBRAL):
        ecltype = 'penumbral'
    else:
        ecltype = '';

    ecldate = 'GMT: %s - %s - %d-%d-%d %d:%d:%d' % (ecplanet, ecltype, eyear, emonth, eday, ehour, eminute, esecond)

    # Calculate the sun position for GMT
    if eclipses_cache.has_key(ecldate):
        lon = eclipses_cache[ecldate]
    else:
        day_time = chart.Time(eyear, emonth, eday, ehour, eminute, esecond, False, 0, 0, False, 0, 0, 0, chrt.place)
        day_chart = chart.Chart(chrt.name, chrt.male, day_time, chrt.place, chrt.htype, chrt.notes, chrt.options)
        lon = day_chart.planets.planets[planet_id].data[planets.Planet.LONG]
        eclipses_cache[ecldate] = lon

    # add to out buffer
    out.append("%.2f\t%s\t" % (lon, ecltype))
    # send out
    sys.stdout.write(''.join(out))

def calculateDailyChart(chrt, year, month, day, hour):
    day_time = chart.Time(year, month, day, hour, 0, 0, chrt.time.bc, chrt.time.cal, chrt.time.zt, chrt.time.plus, chrt.time.zh, chrt.time.zm, chrt.time.daylightsaving, chrt.place)
    return chart.Chart(chrt.name, chrt.male, day_time, chrt.place, chrt.htype, chrt.notes, chrt.options)

def printPlanetsData(chrt):
    out = []
    out.append("%d-%d-%d\t" % (chrt.time.year, chrt.time.month, chrt.time.day))

    for j in range (planets.Planets.PLANETS_NUM):
        lon = chrt.planets.planets[j].data[planets.Planet.LONG]
        lat = chrt.planets.planets[j].data[planets.Planet.LAT]
        speed = chrt.planets.planets[j].data[planets.Planet.SPLON]
        decl = chrt.planets.planets[j].dataEqu[1]
        #name = chrt.planets.planets[j].name
        #riseset = chrt.riseset.planetRiseSet(j)
        out.append("%.2f\t%.2f\t%.3f\t%.2f\t" % (lon, lat, decl, speed))

    for asteroid in chrt.asteroids.asteroids:
        lon = asteroid.data[planets.Planet.LONG]
        lat = asteroid.data[planets.Planet.LAT]
        speed = asteroid.data[planets.Planet.SPLON]
        decl = asteroid.dataEqu[1]
        out.append("%.2f\t%.2f\t%.3f\t%.2f\t" % (lon, lat, decl, speed))

    sys.stdout.write(''.join(out))

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
    print("error loading the chart")

opts = options.Options()
swisseph.set_ephe_path('./SWEP/Ephem')
# instance of place, time and chart generation
place = chart.Place(place, deglon, minlon, 0, east, deglat, minlat, seclat, north, altitude)
time = chart.Time(year, month, day, hour, minute, second, bc, cal, zt, plus, zh, zm, daylightsaving, place)
chrt = chart.Chart(name, male, time, place, htype, notes, opts)

print("Date\t" \
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
    "CELON\tCELAT\tCEDEC\tCESP\t" \
    "CHLON\tCHLAT\tCHDEC\tCHSP\t" \
    "JNLON\tJNLAT\tJNDEC\tJNSP\t" \
    "PALON\tPALAT\tPADEC\tPASP\t" \
    "PHLON\tPHLAT\tPHDEC\tPHSP\t" \
    "VSLON\tVSLAT\tVSDEC\tVSSP\t" \
    "ESULON\tESUT\tEMOLON\tEMOT\t")

dailyPlanets(chrt, 1930, 1, 2030, 12, 2)
