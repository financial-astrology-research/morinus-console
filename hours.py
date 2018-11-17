import astrology
import swisseph
import util
import sys


class PlanetaryHours:
    #From sunrise!! (till next sunrise)
    #Monday: Moon, Saturnus, Jupiter, Mars, Sun, Venus, Mercury, Moon...
    #Sunday: Sun, Venus, Mercury, Moon, Saturnus, Jupiter, Mars, Sun...
    PHs = ((1, 6, 5, 4, 0, 3, 2, 1, 6, 5, 4, 0, 3, 2, 1, 6, 5, 4, 0, 3, 2, 1, 6, 5),
            (4, 0, 3, 2, 1, 6, 5, 4, 0, 3, 2, 1, 6, 5, 4, 0, 3, 2, 1, 6, 5, 4, 0, 3),
            (2, 1, 6, 5, 4, 0, 3, 2, 1, 6, 5, 4, 0, 3, 2, 1, 6, 5, 4, 0, 3, 2, 1, 6),
            (5, 4, 0, 3, 2, 1, 6, 5, 4, 0, 3, 2, 1, 6, 5, 4, 0, 3, 2, 1, 6, 5, 4, 0),
            (3, 2, 1, 6, 5, 4, 0, 3, 2, 1, 6, 5, 4, 0, 3, 2, 1, 6, 5, 4, 0, 3, 2, 1),
            (6, 5, 4, 0, 3, 2, 1, 6, 5, 4, 0, 3, 2, 1, 6, 5, 4, 0, 3, 2, 1, 6, 5, 4),
            (0, 3, 2, 1, 6, 5, 4, 0, 3, 2, 1, 6, 5, 4, 0, 3, 2, 1, 6, 5, 4, 0, 3, 2))


    def __init__(self, lon, lat, altitude, weekday, jd):
        self.risetime = None
        self.settime = None
        self.hrlen = None
        self.daytime = None

        self.weekday = weekday

        #lon, lat, height, atmpress, celsius
        #in GMT, searches after jd!
        ret, risetime = swisseph.rise_trans(jd, astrology.SE_SUN, lon, lat, float(altitude), 0.0, 10.0, astrology.SE_CALC_RISE, astrology.SEFLG_SWIEPH)
        ret, settime = swisseph.rise_trans(jd, astrology.SE_SUN, lon, lat, float(altitude), 0.0, 10.0, astrology.SE_CALC_SET, astrology.SEFLG_SWIEPH)

        #swe_rise_trans calculates only forward!!
        offs = lon*4.0/1440.0
        hr = 0
        HOURSPERHALFDAY = 12.0

        if risetime[0] > settime[0]: # daytime
            self.daytime = True
#           print 'daytime'#
            # Args: float jd_start, int or str body, float lon, float lat, float alt=0.0, float press=0.0, float temp=0.0, int rsmi=0, int flag=FLG_SWIEPH
            ret, result = swisseph.rise_trans(jd-1.0, astrology.SE_SUN, lon, lat, float(altitude), 0.0, 10.0, astrology.SE_CALC_RISE, astrology.SEFLG_SWIEPH)

            #From GMT to Local
            self.risetime = result[0] + offs
            self.settime = settime[0] + offs

#           self.logCalc(settime)#
            self.hrlen = (self.settime-self.risetime)/HOURSPERHALFDAY #hrlen(hour-length) is in days
            for i in range(int(HOURSPERHALFDAY)):
                if jd+offs < self.risetime+self.hrlen*(i+1):
                    hr = i
                    break
        else:# nighttime
            self.daytime = False
#           print 'nightime'#
#           self.logCalc(risetime)#
            ret, result = swisseph.rise_trans(jd-1.0, astrology.SE_SUN, lon, lat, float(altitude), 0.0, 10.0, astrology.SE_CALC_SET, astrology.SEFLG_SWIEPH)
#           self.logCalc(settime)#

            self.risetime = risetime[0] + offs
            self.settime = result[0] + offs

            #Is the local birthtime greater than midnight? If so => decrement day because a planetary day is from sunrise to sunrise
            if jd+offs > int(jd+offs)+0.5:
                self.weekday = util.getPrevDay(self.weekday)

            self.hrlen = (self.risetime-self.settime)/HOURSPERHALFDAY
            for i in range(int(HOURSPERHALFDAY)):
                if jd+offs < self.settime+self.hrlen*(i+1):
                    hr = i+int(HOURSPERHALFDAY)
                    break

        self.planetaryhour = PlanetaryHours.PHs[self.weekday][hr]#planetary day begins from sunrise(not from 0 hour and Planetary hours are not equal!!)


    def revTime(self, tjd):
        jy, jm, jd, jh = swisseph.revjul(tjd, 1)
        d, m, s = util.decToDeg(jh)
        return (d, m, s)


    def logCalc(self, tjd):
        #in GMT!
        jy, jm, jd, jh = swisseph.revjul(tjd, 1)
        d, m, s = util.decToDeg(jh)
        print('GMT: %d.%d.%d %d:%d:%d' % (jy,jm,jd, d, m, s))
