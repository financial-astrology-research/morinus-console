import astrology
import chart
import math
import mtexts
import planets
import swisseph
import sys
import util


class RiseSet:
    """Computes Rise/Set times (for the birthday)"""

    RISE, MC, SET, IC = range(0, 4)

    Angles = [astrology.SE_CALC_RISE, astrology.SE_CALC_MTRANSIT , astrology.SE_CALC_SET,  astrology.SE_CALC_ITRANSIT]

    def __init__(self, jd, cal, lon, lat, alt, pls):
        self.jd = jd
        self.cal = cal
        self.lon = lon
        self.lat = lat
        self.alt = alt

        self.calflag = astrology.SE_GREG_CAL
        if self.cal == chart.Time.JULIAN:
            self.calflag = astrology.SE_JUL_CAL

#       self.offs = lon*4.0/1440.0
        self.times = []
        self.calcTimes()
#       self.printRiseSet(pls)


    def calcTimes(self):
        #the date we get from julianday is the same as year, month day in Time-class but we didn't pass it to the init function.
        oyear, omonth, oday, otim = swisseph.revjul(self.jd, self.calflag)

        numangles = len(RiseSet.Angles)
        for i in range(planets.Planets.PLANETS_NUM):#Nodes are excluded
            ar = []

            #Rise
            # TODO: ret, risetime = swisseph.rise_trans(jd, astrology.SE_SUN, lon, lat, float(altitude), 0.0, 10.0, astrology.SE_CALC_RISE, astrology.SEFLG_SWIEPH)
            ret, JDRise = swisseph.rise_trans(self.jd, i, self.lon, self.lat, self.alt, 0.0, 10.0, RiseSet.Angles[RiseSet.RISE], astrology.SEFLG_SWIEPH)
            tyear, tmonth, tday, ttim = swisseph.revjul(JDRise[0], self.calflag)
            if oyear != tyear or omonth != tmonth or oday != tday:
                ret, JDRise = swisseph.rise_trans(self.jd-1.0, i, self.lon, self.lat, self.alt, 0.0, 10.0, RiseSet.Angles[RiseSet.RISE], astrology.SEFLG_SWIEPH)

            #MC
            ret, JDMC = swisseph.rise_trans(self.jd, i, self.lon, self.lat, self.alt, 0.0, 10.0, RiseSet.Angles[RiseSet.MC], astrology.SEFLG_SWIEPH)
            tyear, tmonth, tday, ttim = swisseph.revjul(JDMC[0], self.calflag)
            if oyear != tyear or omonth != tmonth or oday != tday:
                ret, JDMC = swisseph.rise_trans(self.jd-1.0, i, self.lon, self.lat, self.alt, 0.0, 10.0, RiseSet.Angles[RiseSet.MC], astrology.SEFLG_SWIEPH)

            #Set
            ret, JDSet = swisseph.rise_trans(self.jd, i, self.lon, self.lat, self.alt, 0.0, 10.0, RiseSet.Angles[RiseSet.SET], astrology.SEFLG_SWIEPH)
            tyear, tmonth, tday, ttim = swisseph.revjul(JDSet[0], self.calflag)
            if oyear != tyear or omonth != tmonth or oday != tday:
                ret, JDSet = swisseph.rise_trans(self.jd-1.0, i, self.lon, self.lat, self.alt, 0.0, 10.0, RiseSet.Angles[RiseSet.SET], astrology.SEFLG_SWIEPH)

            #IC
            ret, JDIC = swisseph.rise_trans(self.jd, i, self.lon, self.lat, self.alt, 0.0, 10.0, RiseSet.Angles[RiseSet.IC], astrology.SEFLG_SWIEPH)
            tyear, tmonth, tday, ttim = swisseph.revjul(JDIC[0], self.calflag)
            if oyear != tyear or omonth != tmonth or oday != tday:
                ret, JDIC = swisseph.rise_trans(self.jd-1.0, i, self.lon, self.lat, self.alt, 0.0, 10.0, RiseSet.Angles[RiseSet.IC], astrology.SEFLG_SWIEPH)

            #From GMT to Local
#           JDRise += self.offs
            year, month, day, hr = swisseph.revjul(JDRise[0], self.calflag)
            ar.append(hr)

#           JDMC += self.offs
            year, month, day, hr = swisseph.revjul(JDMC[0], self.calflag)
            ar.append(hr)

#           JDSet += self.offs
            year, month, day, hr = swisseph.revjul(JDSet[0], self.calflag)
            ar.append(hr)

#           JDIC += self.offs
            year, month, day, hr = swisseph.revjul(JDIC[0], self.calflag)
            ar.append(hr)

            self.times.append(ar)


    def printRiseSet(self, pls):
        numangles = len(RiseSet.Angles)
        txt = [mtexts.txtsriseset['Rise'], mtexts.txtsriseset['MC'], mtexts.txtsriseset['Set'], mtexts.txtsriseset['IC']]
        print('')
        print('Rise/Set times:')
        for i in range(planets.Planets.PLANETS_NUM):#Nodes are excluded
            for angle in range(numangles):
                h,m,s = util.decToDeg(self.times[i][angle])
                print("%s: %s: %02d:%02d:%02d" % (pls.planets[i].name, txt[angle], h, m, s))
