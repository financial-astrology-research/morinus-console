#!/usr/bin/env python

import astrology
import chart
import options
import pickle
import placedb
import transits
import util
from inspect import getmembers
from pprint import pprint
from printr import printr

def printTransits(ls, aspecting_planet = -1, aspected_planet = -1):
    planets = ('SU', 'MO', 'ME', 'VE', 'MA', 'JU', 'SA', 'UR', 'NE', 'PL')
    # used to map aspect position to aspect name
    aspects_keys = ['a0', 'a3', 'a4', 'a6', 'a7', 'a9', 'a12', 'a13', 'a14', 'a15', 'a18']
    signs = ['AR', 'TA', 'GE', 'CN', 'LE', 'VI', 'LI', 'SC', 'SA', 'CA', 'AQ', 'PI']
    ascmc = ['Asc', 'MC']

    print "Date\tHour\tPT\tAS\tPR\tHR\tHT\tSI\tLON\tLAT\tSP\tPRLON\t" \
        "ASC1\tMC1\tDES1\tASC2\tMC2\tDES2\tS\t" \
        "SU\tSULO\tSULA\tSUSP\tSUD\tSUS\tSUT\t" \
        "MO\tMOLO\tMOLA\tMOSP\tMOD\tMOS\tMOT\t" \
        "ME\tMELO\tMELA\tMESP\tMED\tMES\tMET\t" \
        "VE\tVELO\tVELA\tVESP\tVED\tVES\tVET\t" \
        "MA\tMALO\tMALA\tMASP\tMAD\tMAS\tMAT\t" \
        "JU\tJULO\tJULA\tJUSP\tJUD\tJUS\tJUT\t" \
        "SA\tSALO\tSALA\tSASP\tSAD\tSAS\tSAT\t" \
        "UR\tURLO\tURLA\tURSP\tURD\tURS\tURT\t" \
        "NE\tNELO\tNELA\tNESP\tNED\tNES\tNET\t" \
        "PL\tPLLO\tPLLA\tPLSP\tPLD\tPLS\tPLT"

    for tr in ls:
        out = []
        if aspecting_planet != -1 and tr.plt != aspecting_planet:
            continue

        d, m, s = util.decToDeg(tr.time)
        if tr.objtype == transits.Transit.PLANET:
            obj_keys = planets
        elif tr.objtype == transits.Transit.ASCMC:
            obj_keys = ascmc
        else:
            continue

        out.append('%s\t%d:%02d:%02d\t%s\t%s\t%s\tH%d\tH%d\t%s\t%d\t%d\t%.2f\t%d\t' % (tr.date, d, m, s, planets[tr.plt], aspects_keys[tr.aspect], obj_keys[tr.obj], tr.house+1, tr.house2+1, signs[tr.sign], tr.lon, tr.lat, tr.sp, tr.prlon))
        # add the riseset times
        out.append('%s\t%s\t%s\t%s\t%s\t%s\t%d' % (tr.riseset1[0], tr.riseset1[1], tr.riseset1[2], tr.riseset2[0], tr.riseset2[1], tr.riseset2[2], tr.score));

        for planet in planets:
            #if isinstance(tr.aspects[planet]['sig'], int):
                #sign = signs[tr.aspects[planet]['sig']]
            #else:
                #sign = ''
            out.append('\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (tr.aspects[planet]['n'], tr.aspects[planet]['lon'], tr.aspects[planet]['lat'], tr.aspects[planet]['sp'], tr.aspects[planet]['d'], tr.aspects[planet]['s'], tr.aspects[planet]['t']))

        print ''.join(out)

fpath = "/Users/pablocc/Hors/USA Born.hor"

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
# The orbs of aspects and planets
opts.orbis = [
 [8.0, 2.0, 2.0, 3.0, 2.0, 4.0, 4.0, 3.0, 2.0, 3.0, 8.0],
 [8.0, 2.0, 2.0, 3.0, 2.0, 4.0, 4.0, 3.0, 2.0, 3.0, 8.0],
 [8.0, 2.0, 2.0, 3.0, 2.0, 4.0, 4.0, 3.0, 2.0, 3.0, 8.0],
 [8.0, 2.0, 2.0, 3.0, 2.0, 4.0, 4.0, 3.0, 2.0, 3.0, 8.0],
 [8.0, 2.0, 2.0, 3.0, 2.0, 4.0, 4.0, 3.0, 2.0, 3.0, 8.0],
 [8.0, 2.0, 2.0, 3.0, 2.0, 4.0, 4.0, 3.0, 2.0, 3.0, 8.0],
 [8.0, 2.0, 2.0, 3.0, 2.0, 4.0, 4.0, 3.0, 2.0, 3.0, 8.0],
 [8.0, 2.0, 2.0, 3.0, 2.0, 4.0, 4.0, 3.0, 2.0, 3.0, 8.0],
 [8.0, 2.0, 2.0, 3.0, 2.0, 4.0, 4.0, 3.0, 2.0, 3.0, 8.0],
 [8.0, 2.0, 2.0, 3.0, 2.0, 4.0, 4.0, 3.0, 2.0, 3.0, 8.0],
 [8.0, 2.0, 2.0, 3.0, 2.0, 4.0, 4.0, 3.0, 2.0, 3.0, 8.0],
]

# instance of place, time and chart generation
place = chart.Place(place, deglon, minlon, 0, east, deglat, minlat, seclat, north, altitude)
time = chart.Time(year, month, day, hour, minute, second, bc, cal, zt, plus, zh, zm, daylightsaving, place)
chrt = chart.Chart(name, male, time, place, htype, notes, opts)

# calculate astrodinas
# chrt.astrodinas()
#chrt.printAspMatrix();
trans = transits.Transits()
# read places DB to get NY place
pdb = placedb.PlaceDB()
pdb.read()
pdb.searchPlace('New York, USA')
trans.extraPlace(pdb.search_result)


for year in range(1990, 2016):
    for month in range(1,13):
        trans.month(year, month, chrt)

printTransits(trans.transits)
