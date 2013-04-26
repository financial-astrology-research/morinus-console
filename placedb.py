import chart
import re
import os
import pickle
from printr import printr

class PlaceDB:

    class Record:
        NAME = 0
        LON = 1
        LAT = 2
        TZ = 3
        ALT = 4
        MAX_NUM = ALT

        DELIMITER = '\t'
        DELIMITER_NUM = MAX_NUM

        def __init__(self, name, lon, lat, tz, alt):
            self.name = name
            self.lon = lon
            self.lat = lat
            self.tz = tz
            self.alt = alt
        

    FILENAME = os.path.join('Res', 'placedb.dat')

    def __init__(self):
        self.placedb = []
        self.search_result = {'place' : '', 'tz' : ''}


    def add(self, name, lon, lat, tz, alt):
        self.placedb.append(PlaceDB.Record(name, lon, lat, tz, alt))


    def read(self):
        lines = []
        try:
            f = open(PlaceDB.FILENAME, 'rb')
            try:
                while(True):
                    lines.append(pickle.load(f))
                f.close()

            except EOFError:
                for ln in lines:
                    #remove newline
                    ln = ln.rstrip('\n')
                    if not self.isValid(ln):
                        continue

                    line = ln.split(PlaceDB.Record.DELIMITER)
                    self.placedb.append(PlaceDB.Record(line[PlaceDB.Record.NAME], line[PlaceDB.Record.LON], line[PlaceDB.Record.LAT], line[PlaceDB.Record.TZ], line[PlaceDB.Record.ALT]))

        except IOError:
            pass


    def write(self):
        try:
            f = open(PlaceDB.FILENAME, 'wb')
            for rec in self.placedb:
                txt = rec.name+PlaceDB.Record.DELIMITER+rec.lon+PlaceDB.Record.DELIMITER+rec.lat+PlaceDB.Record.DELIMITER+rec.tz+PlaceDB.Record.DELIMITER+rec.alt+'\n'
                pickle.dump(txt, f)

            f.close()

        except IOError:
            dlg = wx.MessageDialog(self, mtexts.txts['DBFileError'], mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
        

    def sort(self):
        self.placedb = self.qsort(self.placedb)

#       num = len(self.placedb)

#       for j in range(num):
#           for i in range(num-1):
#               if (self.placedb[i].name > self.placedb[i+1].name):
#                   tmp = self.placedb[i]
#                   self.placedb[i] = self.placedb[i+1]
#                   self.placedb[i+1] = tmp


    def qsort(self, L):
        if L == []: return []
        return self.qsort([x for x in L[1:] if x.name < L[0].name]) + L[0:1] + self.qsort([x for x in L[1:] if x.name >= L[0].name])



    def isValid(self, ln):
        valid = True
        if ln == '':
            valid = False
        else:
            if ln.count(PlaceDB.Record.DELIMITER) != PlaceDB.Record.DELIMITER_NUM:
                valid = False
            #else #here can be more checking...

        return valid

    def searchPlace(self, name):
        for place in self.placedb:
            if re.search(name, place.name, re.IGNORECASE):
                self.buildPlaceObjects(place)

    def buildPlaceObjects(self, place):
        north = True
        east = True

        #long
        idx = place.lon.find(u'E')#
        if idx == -1:
            idx = place.lon.find(u'W')#
            east = False

        deglon = int(place.lon[0:idx])
        idx += 1
        degmin = int(place.lon[idx:])

        #lat
        idx = place.lat.find(u'N')#
        if idx == -1:
            idx = place.lat.find(u'S')#
            north = False

        latdeg = int(place.lat[0:idx])
        idx += 1
        latmin = int(place.lat[idx:])

        #place.tz
        zsign = place.tz[0]
        place.tz = place.tz[1:]
        idx = place.tz.find(':')
        zhour = int(place.tz[0:idx])
        idx += 1
        zminute = int(place.tz[idx:])

        altitude = int(place.alt)

        self.search_result['place'] = chart.Place(place.name, deglon, degmin, 0, east, latdeg, latmin, 0, north, altitude)
        self.search_result['tz'] = {'sign' : zsign, 'hour' : zhour, 'minute' : zminute}
