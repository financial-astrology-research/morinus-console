#!/usr/bin/env python

from datetime import datetime
from inspect import getmembers
from optparse import OptionParser
from pprint import pprint
from printr import printr
import astrology
import chart
import options
import pickle
import placedb
import transits
import util

def printTransits(ls, fh, aspecting_planet = -1, aspected_planet = -1):
    planets = ('SU', 'MO', 'ME', 'VE', 'MA', 'JU', 'SA', 'UR', 'NE', 'PL')
    # used to map aspect position to aspect name
    aspects_keys = ['a0', 'a3', 'a4', 'a6', 'a7', 'a9', 'a12', 'a13', 'a14', 'a15', 'a18']
    signs = ['AR', 'TA', 'GE', 'CN', 'LE', 'VI', 'LI', 'SC', 'SA', 'CA', 'AQ', 'PI']
    ascmc = ['Asc', 'MC']

    header = "Date\tHour\tPT\tAS\tPR\tHR\tHT\tSI\tLON\tLAT\tSP\tPRLON\tS\t" \
            "SU\tSUR\tSULO\tSULA\tSUSP\tSUD\tSURD\tSUS\tSUT\t" \
            "MO\tMOR\tMOLO\tMOLA\tMOSP\tMOD\tMORD\tMOS\tMOT\t" \
            "ME\tMER\tMELO\tMELA\tMESP\tMED\tMERD\tMES\tMET\t" \
            "VE\tVER\tVELO\tVELA\tVESP\tVED\tVERD\tVES\tVET\t" \
            "MA\tMAR\tMALO\tMALA\tMASP\tMAD\tMARD\tMAS\tMAT\t" \
            "JU\tJUR\tJULO\tJULA\tJUSP\tJUD\tJURD\tJUS\tJUT\t" \
            "SA\tSAR\tSALO\tSALA\tSASP\tSAD\tSARD\tSAS\tSAT\t" \
            "UR\tURR\tURLO\tURLA\tURSP\tURD\tURRD\tURS\tURT\t" \
            "NE\tNER\tNELO\tNELA\tNESP\tNED\tNERD\tNES\tNET\t" \
            "PL\tPLR\tPLLO\tPLLA\tPLSP\tPLD\tPLRD\tPLS\tPLT"
    fh.write(header + '\n')

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

        out.append('%s\t%d:%02d:%02d\t%s\t%s\t%s\tH%d\tH%d\t%s\t%d\t%d\t%.2f\t%d\t%d' % (tr.date, d, m, s, planets[tr.plt], aspects_keys[tr.aspect], obj_keys[tr.obj], tr.house+1, tr.house2+1, signs[tr.sign], tr.lon, tr.lat, tr.sp, tr.prlon, tr.score))
        # add the riseset times

        for planet in planets:
            #if isinstance(tr.aspects[planet]['sig'], int):
                #sign = signs[tr.aspects[planet]['sig']]
            #else:
                #sign = ''
            out.append('\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (tr.aspects[planet]['n'], tr.aspects[planet]['prt'], tr.aspects[planet]['lon'], tr.aspects[planet]['lat'], tr.aspects[planet]['sp'], tr.aspects[planet]['d'], tr.aspects[planet]['prd'], tr.aspects[planet]['s'], tr.aspects[planet]['t']))

        fh.write(''.join(out) + '\n')


# track the execution time
startTime = datetime.now()
print "Init process at: "
print(startTime)

# get params
parser = OptionParser()
(args_options, args) = parser.parse_args()

if args and args[0]:
    file_name = args[0]
else:
    print("Provide a transits file name.")
    exit()

try:
   fh = open(file_name, 'w+')
except IOError:
   print "Error: can\'t find file %s" % (file_name)
   exit()

# open the file to save the transits

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
# The orbs of aspects and planets
opts.orbis = [
 [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
 [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
 [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
 [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
 [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
 [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
 [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
 [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
 [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
 [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
 [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
]

opts.riseset = False

# instance of place, time and chart generation
place = chart.Place(place, deglon, minlon, 0, east, deglat, minlat, seclat, north, altitude)
time = chart.Time(year, month, day, hour, minute, second, bc, cal, zt, plus, zh, zm, daylightsaving, place, False)
chrt = chart.Chart(name, male, time, place, htype, notes, opts, False)

# calculate astrodinas
# chrt.astrodinas()
#chrt.printAspMatrix();
trans = transits.Transits()
# read places DB to get NY place
#pdb = placedb.PlaceDB()
#pdb.read()
#pdb.searchPlace('New York, USA')
#trans.extraPlace(pdb.search_result)

for year in range(1997, 2014):
    for month in range(1, 13):
        trans.month(year, month, chrt)

printTransits(trans.transits, fh)

print(datetime.now()-startTime)
