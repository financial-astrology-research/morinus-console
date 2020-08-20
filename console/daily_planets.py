#!/usr/bin/env python3

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append('/usr/local/lib/python3.7/site-packages')

from inspect import getmembers
from pprint import pprint
from sys import exit
import astrology
import chart
import options
import pickle
import planets
import swisseph
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
                    for current_hour in range(hour, 24):
                        day_chart = calculateDailyChart(chrt, year, month, day, current_hour)
                        printPlanetsData(day_chart)
                        # calculateNearestEclipse('sun', chrt, year, month, day, current_hour)
                        # calculateNearestEclipse('moon', chrt, year, month, day, current_hour)
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
        day_time = chart.event.DateTime(eyear, emonth, eday, ehour, eminute, esecond, False, 0, 0, False, 0, 0, 0, chrt.place)
        day_chart = chart.Chart(chrt.name, chrt.male, day_time, chrt.place, chrt.htype, chrt.notes, chrt.options)
        lon = day_chart.planets.planets[planet_id].data[planets.Planet.LONG]
        eclipses_cache[ecldate] = lon

    # add to out buffer
    out.append("%.2f\t%s\t" % (lon, ecltype))
    # send out
    sys.stdout.write(''.join(out))

def calculateDailyChart(chrt, year, month, day, hour):
    day_time = chart.event.DateTime(year, month, day, hour, 0, 0, chrt.time.bc, chrt.time.cal, chrt.time.zt, chrt.time.plus, chrt.time.zh, chrt.time.zm, chrt.time.daylightsaving, chrt.place)
    return chart.Chart(chrt.name, chrt.male, day_time, chrt.place, chrt.htype, chrt.notes, chrt.options)

def printPlanetsData(chrt):
    out = []
    out.append("%d-%d-%d\t%d\t" % (chrt.time.year, chrt.time.month, chrt.time.day, chrt.time.hour))

    for j in range (planets.Planets.PLANETS_NUM):
        lon = chrt.planets.planets[j].data[planets.Planet.LONG]
        lat = chrt.planets.planets[j].data[planets.Planet.LAT]
        speed = chrt.planets.planets[j].data[planets.Planet.SPLON]
        decl = chrt.planets.planets[j].dataEqu[1]
        #name = chrt.planets.planets[j].name
        #riseset = chrt.riseset.planetRiseSet(j)
        out.append("%.2f\t%.2f\t%.3f\t%.2f\t" % (lon, lat, decl, speed))

    # for asteroid in chrt.asteroids.asteroids:
    #     lon = asteroid.data[planets.Planet.LONG]
    #     lat = asteroid.data[planets.Planet.LAT]
    #     speed = asteroid.data[planets.Planet.SPLON]
    #     decl = asteroid.dataEqu[1]
    #     out.append("%.2f\t%.2f\t%.3f\t%.2f\t" % (lon, lat, decl, speed))

    sys.stdout.write(''.join(out))

opts = options.Options()
swisseph.set_ephe_path('../SWEP/Ephem')
# instance of place, time and chart generation
# Based on Greenwich place and UTC time.
place = chart.Place(None, 51, 29, 24, True, 0, 0, 0, True, 0)
time = chart.event.DateTime(2020, 8, 20, 0, 0, 0, False, 0, 0, True, 0, 0, False, place)
chrt = chart.Chart("Daily Chart", False, time, place, 0, "", opts)

print("Date\tHour\t" \
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
    "VSLON\tVSLAT\tVSDEC\tVSSP\t")

dailyPlanets(chrt, 1980, 1, 2030, 12, 0)