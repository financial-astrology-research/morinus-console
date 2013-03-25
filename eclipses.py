#!/usr/bin/env python

import astrology
import chart
import pickle
import options
import transits
import util
from inspect import getmembers
from pprint import pprint
from printr import printr

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
# override orb for exact aspects to 3.0
opts.exact = 3.0

# instance of place, time and chart generation
place = chart.Place(place, deglon, minlon, 0, east, deglat, minlat, seclat, north, altitude)
ny_place = chart.Place('New York', 74, 0, 0, False, 40, 42, 0, True, 43)
time = chart.Time(2005, 10, 3, 10, 0, 0, bc, cal, zt, plus, zh, zm, daylightsaving, place)
chrt = chart.Chart(name, male, time, place, htype, notes, opts)

astrology.swe_set_ephe_path('/Applications/Morinus.app/Contents/Resources/SWEP/Ephem')
calflag = astrology.SE_JUL_CAL
hour = 10
minute = 10
second = 0
time1 = hour+minute/60.0+second/3600.0
tjd = astrology.swe_julday(2013, 3, 1, time1, calflag)
retflag = astrology.swe_sol_eclipse_when_loc(tjd, astrology.SEFLG_SWIEPH, ny_place.lon, ny_place.lat, astrology.SE_ECL_ALLTYPES_SOLAR, False);
#retflag = astrology.swe_sol_eclipse_when_glob(tjd, astrology.SEFLG_SWIEPH, astrology.SE_ECL_ALLTYPES_SOLAR, False);
jd = retflag[1][0]
eclflag = retflag[0][0]
print eclflag
year, month, day, time = astrology.swe_revjul(jd, 1)
print "%d %d %d" % (year, month, day)


if ((eclflag & astrology.SE_ECL_TOTAL)):
    print "total\n"

if ((eclflag & astrology.SE_ECL_ANNULAR)):
    print "annular\n"

if ((eclflag & astrology.SE_ECL_ANNULAR_TOTAL)):
    print "ann-tot\n"

if ((eclflag & astrology.SE_ECL_PARTIAL)):
    print "partial\n"
