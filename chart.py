# -*- coding: utf-8 -*-

import almutens
import antiscia
import antzodpars
import arabicparts
import astrology
import copy
import customerpd
import datetime
import fixstars
import fortune
import hours
import houses
import math
import midpoints
import mtexts
import munfortune
import options
import planets
import riseset
import syzygy
import util
import zodpars
from printr import printr

# if long is 'E' or/and lat is 'S' -> negate value

class Time:
    """Time of Birth"""

    #calendars
    GREGORIAN = 0
    JULIAN = 1

    #times
    ZONE = 0
    GREENWICH = 1
    LOCALMEAN = 2
    LOCALAPPARENT = 3
    
    HOURSPERDAY = 24.0

    def __init__(self, year, month, day, hour, minute, second, bc, cal, zt, plus, zh, zm, daylightsaving, place, full = True): #zt is zonetime, zh is zonehour, zm is zoneminute, full means to calculate everything e.g. FixedStars, MidPoints, ...
        self.year = year
        self.month = month
        self.day = day
        self.origyear = year
        self.origmonth = month
        self.origday = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.bc = bc
        self.cal = cal
        self.zt = zt
        self.plus = plus
        self.zh = zh
        self.zm = zm
        self.daylightsaving = daylightsaving

        self.time = hour+minute/60.0+second/3600.0

        self.dyear, self.dmonth, self.dday, self.dhour, self.dmin, self.dsec = year, month, day, hour, minute, second
        if self.daylightsaving:
            self.time -= 1.0
            self.dhour -= 1
        #check daylightsaving underflow
        if self.time < 0.0:
            self.time += Time.HOURSPERDAY
            self.year, self.month, self.day = util.decrDay(self.year, self.month, self.day)
            self.dhour += int(Time.HOURSPERDAY)
            self.dyear, self.dmonth, self.dday = self.year, self.month, self.day
            
        if zt == Time.ZONE:#ZONE
            ztime = zh+zm/60.0
            if self.plus:
                self.time-=ztime
            else:
                self.time+=ztime
        elif zt == Time.LOCALMEAN:#LMT
            t = (place.deglon+place.minlon/60.0)*4.0 #long * 4min
            if place.east:
                self.time-=t/60.0
            else:
                self.time+=t/60.0   

        if bc:
            self.year = 1-self.year

        #check over/underflow
        if self.time >= Time.HOURSPERDAY:
            self.time -= Time.HOURSPERDAY
            self.year, self.month, self.day = util.incrDay(self.year, self.month, self.day)
        elif self.time < 0.0:
            self.time += Time.HOURSPERDAY
            self.year, self.month, self.day = util.decrDay(self.year, self.month, self.day)

        calflag = astrology.SE_GREG_CAL
        if self.cal == Time.JULIAN:
            calflag = astrology.SE_JUL_CAL
        self.jd = astrology.swe_julday(self.year, self.month, self.day, self.time, calflag)

        if zt == Time.LOCALAPPARENT:#LAT
            ret, te, serr = astrology.swe_time_equ(self.jd)
            self.jd += te #LMT
            #Back to h,m,s(self.time) from julianday fromat
            self.year, self.month, self.day, self.time = astrology.swe_revjul(self.jd, calflag)
            #To GMT
            t = (place.deglon+place.minlon/60.0)*4.0 #long * 4min
            if place.east:
                self.time-=t/60.0
            else:
                self.time+=t/60.0   

            #check over/underflow
            if self.time >= Time.HOURSPERDAY:
                self.time -= Time.HOURSPERDAY
                self.year, self.month, self.day = util.incrDay(self.year, self.month, self.day)
            elif self.time < 0.0:
                self.time += Time.HOURSPERDAY
                self.year, self.month, self.day = util.decrDay(self.year, self.month, self.day)

            #GMT in JD (julianday)
            self.jd = astrology.swe_julday(self.year, self.month, self.day, self.time, calflag)

        self.sidTime = astrology.swe_sidtime(self.jd) #GMT

        self.ph = None
        if full:
            self.calcPHs(place)

        self.profy = None
        self.profm = None
        self.profd = None
        self.profho = None
        self.profmi = None
        self.profse = None


    def calcPHs(self, place):
        #Planetary day/hour calculation
        self.weekday = datetime.datetime(self.dyear, self.dmonth, self.dday, self.dhour, self.dmin, self.dsec).weekday()#only daylightsaving was subtracted
        lon = place.deglon+place.minlon/60.0
        if not place.east:
            lon *= -1
        lat = place.deglat+place.minlat/60.0
        if not place.north:
            lat *= -1
            
        self.ph = hours.PlanetaryHours(lon, lat, place.altitude, self.weekday, self.jd)

        
class Place:
    """Place of Birth"""

    def __init__(self, place, deglon, minlon, seclon, east, deglat, minlat, seclat, north, altitude):
        self.place = place  

        self.deglon = deglon
        self.minlon = minlon
        self.seclon = seclon
        self.east = east    

        self.deglat = deglat
        self.minlat = minlat
        self.seclat = seclat
        self.north = north

        self.altitude = altitude

        self.lon = deglon+minlon/60.0+seclon/3600.0
        self.lat = deglat+minlat/60.0+seclat/3600.0

        if not self.north:
            self.lat *= -1.0

        if not self.east:
            self.lon *= -1.0


class Asp:

    aspect_astrodinas = [
        10, # a0
        2, # a30
        2, # a45
        3, # a60
        2, # a70
        6, # a90
        4, # a120
        2, # a130
        2, # a140
        2, # a150
        10, # a180
        2, #a18
        2, #a40
        2, #a51
        2, #a80
        2, #a103
        2, #a108
        2, #a154
        2, #a160
    ]

    def __init__(self):
        self.typ = Chart.NONE
        self.dif = 0.0
        self.aspdif = 0.0
        self.sinister = False
        self.appl = False
        self.parallel = Chart.NONE
        self.exact = False

class PlanetAspects:
    def __init__(self):
        self.aspects = []

class Chart:
    """Represents a horoscope"""

    #types
    RADIX = 0
    SOLAR = 1
    LUNAR = 2
    REVOLUTION = 3
    TRANSIT = 4
    HORARY = 5
    PROFECTION = 6
    PDINCHART = 7

    SIGN_NUM = 12
    SIGN_DEG = 30

    ARIES = 0
    TAURUS = 1
    GEMINI = 2
    CANCER = 3
    LEO = 4
    VIRGO = 5
    LIBRA = 6
    SCORPIO = 7
    SAGITTARIUS = 8
    CAPRICORNUS = 9
    AQUARIUS = 10
    PISCES = 11

    NONE = -1
    CONJUNCTIO = 0
    SEMISEXTIL = 1
    SEMIQUADRAT = 2
    SEXTIL = 3
    QUINTILE = 4
    QUADRAT = 5
    TRIGON = 6
    SESQUIQUADRAT = 7
    BIQUINTILE = 8
    QUINQUNX = 9
    OPPOSITIO = 10
    PARALLEL = 11
    CONTRAPARALLEL = 12

    RAPTPAR = 13
    RAPTCONTRAPAR = 14
    MIDPOINT = 15

    DOMICIL = 0
    EXAL = 1
    PEREGRIN = 2
    CASUS = 3
    EXIL = 4

    Aspects = [0.0, 30.0, 45.0, 60.0, 72.0, 90.0, 120.0, 135.0, 144.0, 150.0, 180.0, 18, 40, 52, 80, 104, 108, 155, 160]
    ASPECT_NUM = 19

    TRANSURANUS = 0
    TRANSNEPTUNE = 1
    TRANSPLUTO = 2

    #Speculums
    PLACIDIAN = 0
    REGIOMONTAN = 1

    #Lot of Fortune
    LFMOONSUN = 0
    LFDSUNMOON = 1
    LFDMOONSUN = 2
    
    def_fixstarsorb = 1.5   

    #Profections
    YEAR, MONTH, DAY = range(0, 3)

    def __init__(self, name, male, time, place, htype, notes, options, full = True, proftype = 0, nolat=False):
        self.name = name
        self.male = male
        self.time = time
        self.place = place
        self.htype = htype
        self.notes = notes
        self.options = options
        self.full = full
        self.proftype = proftype
        self.nolat = nolat

        d = astrology.swe_deltat(time.jd)
        rflag, self.obl, serr = astrology.swe_calc(time.jd+d, astrology.SE_ECL_NUT, 0)
        #true obliquity of the ecliptic
        #mean
        #nutation in long
        #nutation in obl

        astrology.swe_set_topo(place.lon, place.lat, place.altitude)

        self.create()


    def create(self):
        hflag = 0
        fsflag = 0
        pflag = astrology.SEFLG_SWIEPH+astrology.SEFLG_SPEED
        astflag = astrology.SEFLG_SWIEPH
        self.ayanamsha = 0.0
        if self.options.ayanamsha != 0:
            astrology.swe_set_sid_mode(self.options.ayanamsha-1, 0, 0)
            self.ayanamsha = astrology.swe_get_ayanamsa_ut(self.time.jd)

        if self.options.topocentric:
            pflag += astrology.SEFLG_TOPOCTR

        self.houses = houses.Houses(self.time.jd, hflag, self.place.lat, self.place.lon, self.options.hsys, self.obl[0], self.options.ayanamsha, self.ayanamsha)

        self.raequasc, declequasc, dist = astrology.swe_cotrans(self.houses.ascmc[houses.Houses.EQUASC], 0.0, 1.0, -self.obl[0])
        self.planets = planets.Planets(self.time.jd, self.options.meannode, pflag, self.place.lat, self.houses.ascmc2, self.raequasc, self.nolat, self.obl[0])

        self.abovehorizonwithorb = self.isAboveHorizonWithOrb()

        abovehor = self.planets.planets[astrology.SE_SUN].abovehorizon
        if self.options.usedaynightorb:
            abovehor = self.abovehorizonwithorb

        self.fortune = fortune.Fortune(self.options.lotoffortune, self.houses.ascmc2, self.raequasc, self.planets, self.obl[0], self.place.lat, abovehor)

        self.munfortune = None
        self.parts = None
        self.fixstars = None
        self.midpoints = None
        self.riseset = None
        self.zodpars = None
        self.antiscia = None
        self.antzodpars = None
        self.cpd = None
        self.cpd2 = None
        self.syzygy = None
        self.almutens = None
        mdsun = self.planets.planets[astrology.SE_SUN].speculums[0][planets.Planet.MD]
        sasun = self.planets.planets[astrology.SE_SUN].speculums[0][planets.Planet.SA]
        self.antiscia = antiscia.Antiscia(self.planets.planets, self.houses.ascmc, self.fortune.fortune, self.obl[0], self.options.ayanamsha, self.ayanamsha)
        if self.full:
            self.munfortune = munfortune.MundaneFortune(self.houses.ascmc2, self.planets, self.obl[0], self.place.lat)
            self.syzygy = syzygy.Syzygy(self)
            self.parts = arabicparts.ArabicParts(self.options.arabicparts, self.houses.ascmc, self.planets, self.houses, self.houses.cusps, self.fortune, self.syzygy, self.options)
            self.fixstars = fixstars.FixStars(self.time.jd, fsflag, self.options.fixstars, self.obl[0])
            self.midpoints = midpoints.MidPoints(self.planets)
            self.riseset = riseset.RiseSet(self.time.jd, self.time.cal, self.time.zh, self.place.lon, self.place.lat, self.place.altitude, self.planets)
            self.zodpars = zodpars.ZodPars(self.planets, self.obl[0])
            self.antzodpars = antzodpars.AntZodPars(self.antiscia.plantiscia, self.antiscia.plcontraant, self.obl[0])
            self.almutens = almutens.Almutens(self)
            if self.options.pdcustomer:
                self.cpd = customerpd.CustomerPD(self.options.pdcustomerlon[0], self.options.pdcustomerlon[1], self.options.pdcustomerlon[2], self.options.pdcustomerlat[0], self.options.pdcustomerlat[1], self.options.pdcustomerlat[2], self.options.pdcustomersouthern, self.place.lat, self.houses.ascmc2, self.obl[0], self.raequasc)
            if self.options.pdcustomer2:
                self.cpd2 = customerpd.CustomerPD(self.options.pdcustomer2lon[0], self.options.pdcustomer2lon[1], self.options.pdcustomer2lon[2], self.options.pdcustomer2lat[0], self.options.pdcustomer2lat[1], self.options.pdcustomer2lat[2], self.options.pdcustomer2southern, self.place.lat, self.houses.ascmc2, self.obl[0], self.raequasc)

        astrology.swe_close()

        self.calcAspMatrix()

        if self.fixstars != None:
            self.calcFixStarAspMatrix()

        #self.calculateAstrodinas()

    def rebuildFixStars(self):
        if self.full:
            del self.fixstars
            fsflag = 0
            self.fixstars = fixstars.FixStars(self.time.jd, fsflag, self.options.fixstars, self.obl[0])


    def setHouseSystem(self):
        hflag = 0
        self.houses = houses.Houses(self.time.jd, hflag, self.place.lat, self.place.lon, self.options.hsys, self.obl[0], self.options.ayanamsha, self.ayanamsha)


    def setNodes(self):
        pflag = astrology.SEFLG_SWIEPH+astrology.SEFLG_SPEED
        self.planets = planets.Planets(self.time.jd, self.options.meannode, pflag, self.place.lat, self.houses.ascmc2, self.raequasc, self.obl[0])


    def calcFortune(self):
        del self.fortune
        self.abovehorizonwithorb = self.isAboveHorizonWithOrb()

        abovehor = self.planets.planets[astrology.SE_SUN].abovehorizon
        if self.options.usedaynightorb:
            abovehor = self.abovehorizonwithorb

        self.fortune = fortune.Fortune(self.options.lotoffortune, self.houses.ascmc2, self.raequasc, self.planets, self.obl[0], self.place.lat, abovehor)
        self.calcPointAspMatrix(self.fortune.fortune[fortune.Fortune.LON], 0)


    def isAboveHorizonWithOrb(self):
        mdsun = self.planets.planets[astrology.SE_SUN].speculums[0][planets.Planet.MD]
        sasun = self.planets.planets[astrology.SE_SUN].speculums[0][planets.Planet.SA]
        abovehorizon = self.planets.planets[astrology.SE_SUN].abovehorizon
#       mdsun = self.planets.planets[planets.Planets.SUN].speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.MD]
#       sasun = self.planets.planets[planets.Planets.SUN].speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.SA]
#       abovehorizon = self.planets.planets[planets.Planets.SUN].speculums[planets.Planet.PLACIDIAN].abovehorizon

        if not abovehorizon:
            if mdsun < 0.0:
                mdsun += 180.0
            if sasun < 0.0:
                sasun += 180.0

            orb = self.options.daynightorbdeg+self.options.daynightorbmin/60.0
            if mdsun-orb < sasun:
                abovehorizon = True         

        return abovehorizon


    def calcSyzygy(self):
        if self.full:
            del self.syzygy
            self.syzygy = syzygy.Syzygy(self)


    def calcArabicParts(self):
        if self.full:
            del self.parts
            self.parts = arabicparts.ArabicParts(self.options.arabicparts, self.houses.ascmc, self.planets, self.houses, self.houses.cusps, self.fortune, self.syzygy, self.options)


    def calcAntiscia(self):
        if self.antiscia != None:
            del self.antiscia
            self.antiscia = antiscia.Antiscia(self.planets.planets, self.houses.ascmc, self.fortune.fortune, self.obl[0], self.options.ayanamsha, self.ayanamsha)


    def calcAspMatrix(self):    
        self.calcSpeeds()

        self.aspmatrix = [[Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp()], 
                    [Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp()], 
                    [Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp()], 
                    [Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp()], 
                    [Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp()], 
                    [Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp()], 
                    [Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp()], 
                    [Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp()], 
                    [Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp()], 
                    [Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp()], 
                    [Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp()]]

        for i in range(self.planets.PLANETS_NUM-1):
            for j in range(self.planets.PLANETS_NUM-1):
                if i != j:
                    k = i
                    l = j
                    if j > i:
                        k = j
                        l = i

                    #Check parallel-contraparallel  
                    self.aspmatrix[k][l].parallel = Chart.NONE 
                    decl1 = self.planets.planets[i].dataEqu[1]                          
                    decl2 = self.planets.planets[j].dataEqu[1]                          
                    if (decl1 > 0.0 and decl2 > 0.0) or (decl1 < 0.0 and decl2 < 0.0):
                        if ((decl1 > 0.0 and (decl1+self.options.orbisplanetspar[i][0]+self.options.orbisplanetspar[j][0] > decl2) and (decl1-(self.options.orbisplanetspar[i][0]+self.options.orbisplanetspar[j][0]) < decl2)) or (decl1 < 0.0 and (decl1+self.options.orbisplanetspar[i][0]+self.options.orbisplanetspar[j][0] > decl2) and (decl1-(self.options.orbisplanetspar[i][0]+self.options.orbisplanetspar[j][0]) < decl2))):
                            self.aspmatrix[k][l].parallel = Chart.PARALLEL
                    else:
                        if decl1 < 0.0:
                            decl1 *= -1.0
                        if decl2 < 0.0:
                            decl2 *= -1.0
                        if (decl1+self.options.orbisplanetspar[i][1]+self.options.orbisplanetspar[j][1] > decl2) and (decl1-(self.options.orbisplanetspar[i][1]+self.options.orbisplanetspar[j][1]) < decl2):
                            self.aspmatrix[k][l].parallel = Chart.CONTRAPARALLEL

                    for a in range(Chart.ASPECT_NUM):
                        #Check aspects

                        val1 = self.planets.planets[j].data[0]+self.options.orbis[j][a]+self.options.orbis[i][a]
                        val2 = self.planets.planets[j].data[0]-(self.options.orbis[j][a]+self.options.orbis[i][a])

                        if (self.inorbsinister(val1, val2, self.planets.planets[i].data[0], a)):
                            tmp = util.normalize(self.planets.planets[i].data[0]+Chart.Aspects[a])
                            dif = math.fabs(tmp-self.planets.planets[j].data[0])
                            if self.aspmatrix[k][l].typ == Chart.NONE or (self.aspmatrix[k][l].typ != Chart.NONE and self.aspmatrix[k][l].dif > dif):
                                self.aspmatrix[k][l].typ = a
                                self.aspmatrix[k][l].aspdif = dif
                                self.aspmatrix[k][l].sinister = True
                                self.aspmatrix[k][l].appl = self.isApplPlanets(tmp, i, j) 

                                #Check Exact
                                val1 = self.planets.planets[j].data[0]+self.options.exact
                                val2 = self.planets.planets[j].data[0]-self.options.exact

                                if (self.inorbsinister(val1, val2, self.planets.planets[i].data[0], a)):
                                    self.aspmatrix[k][l].exact = True 
                                else:   
                                    self.aspmatrix[k][l].exact = False
                        dif = self.planets.planets[i].data[0]-self.planets.planets[j].data[0]
                        if self.planets.planets[j].data[0] > self.planets.planets[i].data[0]:
                            dif = self.planets.planets[j].data[0]-self.planets.planets[i].data[0]

                        if dif > 180.0:
                            dif = 360.0-dif

                        self.aspmatrix[k][l].dif = dif

        NODES = 2
        # AscMC
        self.aspmatrixAscMC = [[Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(), Asp()], 
                            [Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(), Asp()]]

        ascmc = [self.houses.ascmc2[houses.Houses.ASC][houses.Houses.DECL], self.houses.ascmc2[houses.Houses.MC][houses.Houses.DECL]]
        for i in range(self.planets.PLANETS_NUM-1):
            for j in range(2):
                #Check parallel-contraparallel
                self.aspmatrixAscMC[j][i].parallel = Chart.NONE 
                decl1 = self.planets.planets[i].dataEqu[1]
                decl2 = ascmc[j]
                if (decl1 > 0.0 and decl2 > 0.0) or (decl1 < 0.0 and decl2 < 0.0):
                    if ((decl1 > 0.0 and (decl1+self.options.orbisparAscMC[0]+self.options.orbisplanetspar[i][0] > decl2) and (decl1-(self.options.orbisparAscMC[0]+self.options.orbisplanetspar[i][0]) < decl2)) or (decl1 < 0.0 and (decl1+self.options.orbisparAscMC[0]+self.options.orbisplanetspar[i][0] > decl2) and (decl1-(self.options.orbisparAscMC[0]+self.options.orbisplanetspar[i][0]) < decl2))):
                        self.aspmatrixAscMC[j][i].parallel = Chart.PARALLEL
                else:
                    if decl1 < 0.0:
                        decl1 *= -1.0
                    if decl2 < 0.0:
                        decl2 *= -1.0
                    if (decl1+self.options.orbisparAscMC[1]+self.options.orbisplanetspar[i][1] > decl2) and (decl1-(self.options.orbisparAscMC[1]+self.options.orbisplanetspar[i][1]) < decl2):
                        self.aspmatrixAscMC[j][i].parallel = Chart.CONTRAPARALLEL

                for a in range(Chart.ASPECT_NUM):
                    if i == self.planets.PLANETS_NUM-NODES and a > 0:#exclude the aspects of the nodes
                        break

                    #Check aspects
                    val1 = self.houses.ascmc[j]+self.options.orbisAscMC[a]+self.options.orbis[i][a]
                    val2 = self.houses.ascmc[j]-(self.options.orbisAscMC[a]+self.options.orbis[i][a])

                    if (self.inorbsinister(val1, val2, self.planets.planets[i].data[0], a)):
                        tmp = util.normalize(self.planets.planets[i].data[0]+Chart.Aspects[a])
                        dif = math.fabs(tmp-self.houses.ascmc[j])
                        if self.aspmatrixAscMC[j][i].typ == Chart.NONE or (self.aspmatrixAscMC[j][i].typ != Chart.NONE and self.aspmatrixAscMC[j][i].dif > dif):
                            self.aspmatrixAscMC[j][i].typ = a
                            self.aspmatrixAscMC[j][i].aspdif = dif
                            self.aspmatrixAscMC[j][i].sinister = True
                            self.aspmatrixAscMC[j][i].appl = tmp > self.houses.ascmc[j] 

                            #Exact
                            val1 = self.houses.ascmc[j]+self.options.exact
                            val2 = self.houses.ascmc[j]-self.options.exact

                            if (self.inorbsinister(val1, val2, self.planets.planets[i].data[0], a)):
                                self.aspmatrixAscMC[j][i].exact = True 
                            else:   
                                self.aspmatrixAscMC[j][i].exact = False
                    else:#negativ
                        if (self.inorbdexter(val1, val2, self.planets.planets[i].data[0], a)):
                            tmp = util.normalize(self.planets.planets[i].data[0]-Chart.Aspects[a])
                            dif = math.fabs(tmp-self.houses.ascmc[j])
                            if self.aspmatrixAscMC[j][i].typ == Chart.NONE or (self.aspmatrixAscMC[j][i].typ != Chart.NONE and self.aspmatrixAscMC[j][i].dif > dif):
                                self.aspmatrixAscMC[j][i].typ = a
                                self.aspmatrixAscMC[j][i].aspdif = dif
                                self.aspmatrixAscMC[j][i].appl = tmp > self.houses.ascmc[j] 

                                #Exact
                                val1 = self.houses.ascmc[j]+self.options.exact
                                val2 = self.houses.ascmc[j]-self.options.exact

                                if (self.inorbdexter(val1, val2, self.planets.planets[i].data[0], a)):
                                    self.aspmatrixAscMC[j][i].exact = True 
                                else:   
                                    self.aspmatrixAscMC[j][i].exact = False

                    dif = self.planets.planets[i].data[0]-self.houses.ascmc[j]
                    if self.houses.ascmc[j] > self.planets.planets[i].data[0]:
                        dif = self.houses.ascmc[j]-self.planets.planets[i].data[0]

                    if dif > 180.0:
                        dif = 360.0-dif

                    self.aspmatrixAscMC[j][i].dif = dif

        # Houses
        hidx = (1, 2, 3, 10, 11, 12)

        self.aspmatrixH = [[Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(), Asp()], 
                            [Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(), Asp()], 
                            [Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(), Asp()], 
                            [Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(), Asp()], 
                            [Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(), Asp()], 
                            [Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(),Asp(), Asp()]] 

        for i in range(self.planets.PLANETS_NUM-1):
            for j in range(len(hidx)):
                #Check parallel-contraparallel
                self.aspmatrixH[j][i].parallel = Chart.NONE 
                decl1 = self.planets.planets[i].dataEqu[1]
                decl2 = self.houses.cusps2[hidx[j]-1][1]    
                if (decl1 > 0.0 and decl2 > 0.0) or (decl1 < 0.0 and decl2 < 0.0):
                    if ((decl1 > 0.0 and (decl1+self.options.orbisparH[0]+self.options.orbisplanetspar[i][0] > decl2) and (decl1-(self.options.orbisparH[0]+self.options.orbisplanetspar[i][0]) < decl2)) or (decl1 < 0.0 and (decl1+self.options.orbisparH[0]+self.options.orbisplanetspar[i][0] > decl2) and (decl1-(self.options.orbisparH[0]+self.options.orbisplanetspar[i][0]) < decl2))):
                        self.aspmatrixH[j][i].parallel = Chart.PARALLEL
                else:
                    if decl1 < 0.0:
                        decl1 *= -1.0
                    if decl2 < 0.0:
                        decl2 *= -1.0
                    if (decl1+self.options.orbisparH[1]+self.options.orbisplanetspar[i][1] > decl2) and (decl1-(self.options.orbisparH[1]+self.options.orbisplanetspar[i][1]) < decl2):
                        self.aspmatrixH[j][i].parallel = Chart.CONTRAPARALLEL

                for a in range(Chart.ASPECT_NUM):
                    if i == self.planets.PLANETS_NUM-NODES and a > 0:#exclude the aspects of the nodes
                        break

                    #Check aspects
                    orbH = self.options.orbisH[a]
                    val1 = self.houses.cusps[hidx[j]]+orbH+self.options.orbis[i][a]
                    val2 = self.houses.cusps[hidx[j]]-(orbH+self.options.orbis[i][a])

                    if (j == 0 or j == 3) and (self.houses.hsys == 'P' or self.houses.hsys == 'K' or self.houses.hsys == 'O' or self.houses.hsys == 'R' or self.houses.hsys == 'C' or self.houses.hsys == 'E' or self.houses.hsys == 'T' or self.houses.hsys == 'B'):
                        orbH = self.options.orbisAscMC[a]

                    pllon = self.planets.planets[i].data[0]
                    if self.options.ayanamsha != 0 and self.houses.hsys == 'W':
                        pllon = util.normalize(pllon-self.ayanamsha)
                    if (self.inorbsinister(val1, val2, pllon, a)):
                        tmp = util.normalize(pllon+Chart.Aspects[a])
                        dif = math.fabs(tmp-self.houses.cusps[hidx[j]])
                        if self.aspmatrixH[j][i].typ == Chart.NONE or (self.aspmatrixH[j][i].typ != Chart.NONE and self.aspmatrixH[j][i].dif > dif):
                            self.aspmatrixH[j][i].typ = a
                            self.aspmatrixH[j][i].aspdif = dif
                            self.aspmatrixH[j][i].sinister = True
                            self.aspmatrixH[j][i].appl = tmp > self.houses.cusps[hidx[j]] 

                            #Exact
                            val1 = self.houses.cusps[hidx[j]]+self.options.exact
                            val2 = self.houses.cusps[hidx[j]]-self.options.exact

                            if (self.inorbsinister(val1, val2, pllon, a)):
                                self.aspmatrixH[j][i].exact = True 
                            else:   
                                self.aspmatrixH[j][i].exact = False
                    else:#negativ
                        if (j == 0 or j == 3) and (self.houses.hsys == 'P' or self.houses.hsys == 'K' or self.houses.hsys == 'O' or self.houses.hsys == 'R' or self.houses.hsys == 'C' or self.houses.hsys == 'E' or self.houses.hsys == 'T' or self.houses.hsys == 'B'):
                            orbH = self.options.orbisAscMC[a]

                        if (self.inorbdexter(val1, val2, pllon, a)):
                            tmp = util.normalize(pllon-Chart.Aspects[a])
                            dif = math.fabs(tmp-self.houses.cusps[hidx[j]])
                            if self.aspmatrixH[j][i].typ == Chart.NONE or (self.aspmatrixH[j][i].typ != Chart.NONE and self.aspmatrixH[j][i].dif > dif):
                                self.aspmatrixH[j][i].typ = a
                                self.aspmatrixH[j][i].aspdif = dif
                                self.aspmatrixH[j][i].appl = tmp > self.houses.cusps[hidx[j]] 

                                #exact
                                val1 = self.houses.cusps[hidx[j]]+self.options.exact
                                val2 = self.houses.cusps[hidx[j]]-self.options.exact

                                if (self.inorbdexter(val1, val2, pllon, a)):
                                    self.aspmatrixH[j][i].exact = True 
                                else:   
                                    self.aspmatrixH[j][i].exact = False

                    dif = pllon-self.houses.cusps[hidx[j]]
                    if self.houses.cusps[hidx[j]] > pllon:
                        dif = self.houses.cusps[hidx[j]]-pllon

                    if dif > 180.0:
                        dif = 360.0-dif

                    self.aspmatrixH[j][i].dif = dif


        self.calcPointAspMatrix(self.fortune.fortune[fortune.Fortune.LON], 0)


    def calcPointAspMatrix(self, point_lon, matrix_pos):
        NODES = 2
        # we have up to 10 rows in the matrix for custom points
        self.aspMatrixPoints = [
            [Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
            [Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
            [Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
            [Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
            [Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
            [Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
            [Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
            [Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
            [Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
            [Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
        ]

        for i in range(self.planets.PLANETS_NUM):#Both nodes (conjunctio only)
            #We don't check parallel-contraparallel now
            self.aspMatrixPoints[matrix_pos][i].parallel = Chart.NONE 

            for a in range(Chart.ASPECT_NUM):
                #only conjunctio in case of the nodes
                if i >= self.planets.PLANETS_NUM-NODES and a > 0:
                    break

                #Check aspects
                orb = 0.0
                if i < self.planets.PLANETS_NUM-1:
                    orb = self.options.orbis[i][a]
                else:
                    orb = self.options.orbis[i-1][a]

                val1 = point_lon+orb
                val2 = point_lon-orb

                if (self.inorbsinister(val1, val2, self.planets.planets[i].data[0], a)):
                    tmp = util.normalize(self.planets.planets[i].data[0]+Chart.Aspects[a])
                    dif = math.fabs(tmp-point_lon)
                    if self.aspMatrixPoints[matrix_pos][i].typ == Chart.NONE or (self.aspMatrixPoints[matrix_pos][i].typ != Chart.NONE and self.aspMatrixPoints[matrix_pos][i].dif > dif):
                        self.aspMatrixPoints[matrix_pos][i].typ = a
                        self.aspMatrixPoints[matrix_pos][i].aspdif = dif
                        self.aspMatrixPoints[matrix_pos][i].sinister = True
                        self.aspMatrixPoints[matrix_pos][i].appl = tmp > point_lon #LoF's speed is like that of the Moon but if Sun-Moon then it goes backwards in the signs

                        #Exact
                        val1 = point_lon+self.options.exact
                        val2 = point_lon-self.options.exact

                        if (self.inorbsinister(val1, val2, self.planets.planets[i].data[0], a)):
                            self.aspMatrixPoints[matrix_pos][i].exact = True 
                        else:   
                            self.aspMatrixPoints[matrix_pos][i].exact = False
                else:#negativ
                    if (self.inorbdexter(val1, val2, self.planets.planets[i].data[0], a)):
                        tmp = util.normalize(self.planets.planets[i].data[0]-Chart.Aspects[a])
                        dif = math.fabs(tmp-point_lon)
                        if self.aspMatrixPoints[matrix_pos][i].typ == Chart.NONE or (self.aspMatrixPoints[matrix_pos][i].typ != Chart.NONE and self.aspMatrixPoints[matrix_pos][i].dif > dif):
                            self.aspMatrixPoints[matrix_pos][i].typ = a
                            self.aspMatrixPoints[matrix_pos][i].aspdif = dif
                            self.aspMatrixPoints[matrix_pos][i].appl = tmp > point_lon #LoF's spped is like that of the Moon but if Sun-Moon then it goes backwards in the signs

                            #exact
                            val1 = point_lon+self.options.exact
                            val2 = point_lon-self.options.exact

                            if (self.inorbdexter(val1, val2, self.planets.planets[i].data[0], a)):
                                self.aspMatrixPoints[matrix_pos][i].exact = True 
                            else:   
                                self.aspMatrixPoints[matrix_pos][i].exact = False

                dif = self.planets.planets[i].data[0]-point_lon
                if point_lon > self.planets.planets[i].data[0]:
                    dif = point_lon-self.planets.planets[i].data[0]

                if dif > 180.0:
                    dif = 360.0-dif

                self.aspMatrixPoints[matrix_pos][i].dif = dif

#        for i in range(len(self.aspMatrixPoints[matrix_pos])):
            #if self.aspMatrixPoints[matrix_pos][i].typ > -1:
                #printr(self.aspMatrixPoints[matrix_pos][i])



    def isApplPlanets(self, tmp, pl1, pl2):
        pl1speed = 0
        pl2speed = 0
        for i in range(self.planets.PLANETS_NUM-1):
            if self.speeds[i] == pl1:
                pl1speed = i
            if self.speeds[i] == pl2:
                pl2speed = i

        pl1ret = self.planets.planets[pl1].data[3] < 0.0
        pl2ret = self.planets.planets[pl2].data[3] < 0.0

        #Aspects are checked only forward => pl1 is always before pl2!
        if tmp < self.planets.planets[pl2].data[0]:
            if pl1speed > pl2speed:
                return not pl1ret
            else:
                return pl2ret
        else:
            if pl1speed > pl2speed:
                return pl1ret
            else:
                return not pl2ret       


    def calcSpeeds(self):
        self.speeds = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        planetspds = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for i in range(self.planets.PLANETS_NUM-1):
            planetspds[i] = self.planets.planets[i].data[3]
            if planetspds[i] < 0.0:
                planetspds[i] *= -1.0

        for j in range(self.planets.PLANETS_NUM-1):
            for i in range(self.planets.PLANETS_NUM-2):
                if (planetspds[i] > planetspds[i+1]):
                    tmp = planetspds[i]
                    planetspds[i] = planetspds[i+1]
                    planetspds[i+1] = tmp
                    a = self.speeds[i]
                    self.speeds[i] = self.speeds[i+1]
                    self.speeds[i+1] = a


    def dignity(self, pid):
        lona = self.planets.planets[pid].data[0]
        if self.options.ayanamsha != 0:
            lona -= self.ayanamsha
            lona = util.normalize(lona)
        sign = int(lona/Chart.SIGN_DEG)
        val = Chart.PEREGRIN

        if pid < astrology.SE_PLUTO+1:
            isdom = self.options.dignities[pid][0][sign]
            isexal = self.options.dignities[pid][1][sign]

            oppsign = sign+Chart.SIGN_NUM/2
            if oppsign >= Chart.SIGN_NUM:
                oppsign -= Chart.SIGN_NUM

            isexil = self.options.dignities[pid][0][oppsign]
            iscasus = self.options.dignities[pid][1][oppsign]

            if isdom:
                val = Chart.DOMICIL
            elif isexil:
                val = Chart.EXIL
            elif isexal:
                val = Chart.EXAL
            elif iscasus:
                val = Chart.CASUS   

        return val

    def calculateAstrodinas(self):
        # calculate the planets signs
        self.calcPlanetSign()
        # init a planets score array
        self.astrodinas = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for pid in range(astrology.SE_PLUTO+1):

            ###########################################
            # calculate domicile & exaltation
            ###########################################
            if self.isInDomicile(pid):
                # score 5 for domicile
                self.astrodinas[pid] += 5

            if self.isInExaltation(pid):
                # score 4 for exaltation
                self.astrodinas[pid] += 4

            ####################################
            # calculates if it's in a triplicity
            ####################################

            if self.isInTriplicity(pid):
                # score +2 for triplicity
                self.astrodinas[pid] += 2

            ##############################
            # calculate the decans dignity
            ##############################

            # position of a planet relative to the sign
            lona = self.planets.planets[pid].data[0]
            pos_sign = lona % self.SIGN_DEG
            # number of decan where the relative position belogns
            dec = int(pos_sign / 10)
            sign = self.planets.planets[pid].sign

            if self.options.decans[self.options.seldecan][sign][dec] == pid:
                # score +1 for decan
                self.astrodinas[pid] += 1

            ##############
            # ruler of day
            ##############
            #day_ruler = (1, 4, 2, 5, 3, 6, 0)
            #if day_ruler[self.time.ph.weekday] == pid:
                # score +1 for day ruler
                #self.astrodinas[day_ruler[self.time.ph.weekday]] += 1

            ########################################################
            # dispositor of other planets by domicile and exaltation
            ########################################################

            # extract from the domicile matrix the signs that belongs to current planet
            planet_doms = [i for i in range(len(self.options.dignities[pid][0])) if self.options.dignities[pid][0][i] == True]
            # for each planet domicile sign look for how many planets is dispositor
            #for domsign in planet_doms:
                # score +2 for each disposed planet by domicile
                # self.astrodinas[pid] += self.signs_planets[domsign] * 2

            planet_exals = [i for i in range(len(self.options.dignities[pid][1])) if self.options.dignities[pid][1][i] == True]
            #for exalsign in planet_exals:
                # score +1 for each disposed planet by exaltation
                # self.astrodinas[pid] += self.signs_planets[exalsign] * 1

            ##############################
            # Mutual reception by domicile
            ##############################
            in_reception = self.isInMutualReception(pid)
            if in_reception > 0:
                # score +3 for each reception
                self.astrodinas[pid] += in_reception * 2

            # TODO: implement combust
            # TODO: implement cazimi
            # TODO: implement almugea
            # TODO: fixed stars conjunctions
            # TODO: implement dignity by term
            # TODO: implement mutual reception by exaltation
            # TODO: implement status of the lord and aspect to current planet

            #################################
            # Aspects from it's dignities
            #################################
            self.astrodinas[pid] += self.calcAspectsFromDignity(pid)

            #############
            # In it's joy
            #############
            if self.isInJoy(pid):
                # score +1 for joy
                self.astrodinas[pid] += 1

            ######################
            # above of the horizon
            ######################
            if self.planets.planets[pid].abovehorizon:
                # score +1 if planet is above horizon
                self.astrodinas[pid] += 1

            ##########################################
            # debilitations that decrease planet power
            ##########################################
            decrease_factor = self.calcPlanetDebility(pid)
            self.astrodinas[pid] = round(self.astrodinas[pid] * decrease_factor, 1)

    def calcAspectsFromDignity(self, pid):
        '''Calculate receiving aspects from it's own dignities'''

        given_astrodinas = 0
        planet_aspects = self.getPlanetAspects(pid)
        planet_doms = [i for i in range(len(self.options.dignities[pid][0])) if self.options.dignities[pid][0][i] == True]
        planet_exals = [i for i in range(len(self.options.dignities[pid][1])) if self.options.dignities[pid][1][i] == True]
        planet_dignities = planet_doms + planet_exals

        for aspect in planet_aspects.aspects:
            aspect_sign = self.planets.planets[aspect.pid].sign
            if aspect_sign in planet_dignities:
                given_astrodinas += self.calcAspectAstrodinas(aspect)

        return given_astrodinas

    def calcPlanetSign(self):
        '''Calculates the sign position of the chart planets'''

        # counter of number of planets that are in specific sign
        self.signs_planets = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for pid in range(astrology.SE_MEAN_NODE+1):
            lona = self.planets.planets[pid].data[0]
            sign = int(lona/Chart.SIGN_DEG)
            self.planets.planets[pid].sign = sign
            self.signs_planets[sign] += 1

    def calcPlanetDebility(self, pid):
        '''Calculates planet debility and affect it's astrodinas accordingly'''

        decrease_factor = 1

        # decrease astrodinas powerful
        if self.isInExile(pid):
            # 30 percent
            decrease_factor -= 0.30

        if self.isInFall(pid):
            # 30 percent
            decrease_factor -= 0.30

        if self.isRetrograde(pid):
            # 20 percent
            decrease_factor -= 0.20

        return decrease_factor

    def isRetrograde(self, pid):
        '''Check if a planet is retrograde'''
        if self.planets.planets[pid].data[planets.Planet.SPLON] < 0.0:
            return True
        return False

    def isInJoy(self, spid):
        '''Check if a planet is in it's joy (house natural to it's significations)'''
        planet_joys = [9, 3, 1, 5, 6, 11, 12, -1, -1, -1]

        # get longitude of the planet and the house where is located
        lon = self.planets.planets[spid].data[planets.Planet.LONG]
        planet_house = self.houses.getHousePos(lon, self.options)

        if planet_joys[spid] != -1 and planet_joys[spid] == planet_house:
            return True

        return False

    def isInMutualReception(self, spid):
        '''Check if a planet is in mutual reception by domicile with other.'''

        planet_doms = [i for i in range(len(self.options.dignities[spid][0])) if self.options.dignities[spid][0][i] == True]
        mutual_receptors = []
        for pid in range(astrology.SE_PLUTO+1):
            # don't look for itself and check mutual reception if the iterated planet
            # is located in the dignity of looked planet (pid)
            if spid != pid and self.planets.planets[pid].sign in planet_doms:
                candidate_doms = [i for i in range(len(self.options.dignities[pid][0])) if self.options.dignities[pid][0][i] == True]
                if self.planets.planets[spid].sign in candidate_doms:
                    mutual_receptors.append(pid)

        return len(mutual_receptors)

    def isInTriplicity(self, spid):
        '''Calculates if a planet is in its triplicity'''

        # define the mapping of signs with elemental triplicity
        tripls = [0, 3, 1, 2, 0, 3, 1, 2, 0, 3, 1, 2]
        sign_element = tripls[self.planets.planets[spid].sign]

        # iterate over the three triplicity rules according Morin
        for k in range(3):
            # the key 2 represents the triplicities based on Morin
            # key 2 is based on Dorothean
            tripid = self.options.trips[2][sign_element][k]

            if tripid != -1 and tripid == spid:
                return True

        return False

    def isInDomicile(self, pid):
        '''Check if a planet is in it's domicile'''
        sign = self.planets.planets[pid].sign
        if self.options.dignities[pid][0][sign]:
            return True
        return False

    def isInExile(self, pid):
        '''Check if a planet is in it's exile'''
        sign = self.planets.planets[pid].sign
        oppsign = sign+Chart.SIGN_NUM/2
        if oppsign >= Chart.SIGN_NUM:
            oppsign -= Chart.SIGN_NUM

        if self.options.dignities[pid][0][oppsign]:
            return True
        return False

    def isInExaltation( self, pid ):
        '''Check if a planet is in it's exaltation'''
        sign = self.planets.planets[pid].sign
        if self.options.dignities[pid][1][sign]:
            return True
        return False
 
    def isInFall(self, pid):
        '''Check if a planet is in it's fall'''
        sign = self.planets.planets[pid].sign
        oppsign = sign+Chart.SIGN_NUM/2
        if oppsign >= Chart.SIGN_NUM:
            oppsign -= Chart.SIGN_NUM

        if self.options.dignities[pid][1][oppsign]:
            return True
        return False

    def calcFixStarAspMatrix(self):
        '''Calculates conjunctions of fixstars(planets and AscMC)'''

        self.fsaspmatrix = []
        self.fsaspmatrixangles = []
        self.fsaspmatrixhcs = []
        self.fsaspmatrixlof = []

        num = len(self.fixstars.data)
        for i in range(num):
            ar = []

            val1 = self.fixstars.data[i][fixstars.FixStars.LON]+self.options.fixstars[self.fixstars.data[i][fixstars.FixStars.NOMNAME]]
            val2 = self.fixstars.data[i][fixstars.FixStars.LON]-self.options.fixstars[self.fixstars.data[i][fixstars.FixStars.NOMNAME]]

            for j in range(self.planets.PLANETS_NUM):
                if (self.inorbsinister(val1, val2, self.planets.planets[j].data[planets.Planet.LONG], Chart.CONJUNCTIO)):
                    ar.append(j)

            if len(ar) != 0:
                fsar = (i, ar)
                self.fsaspmatrix.append(fsar)

        # AscDescMCIC
        ASC = self.houses.ascmc[houses.Houses.ASC]
        DESC = util.normalize(self.houses.ascmc[houses.Houses.ASC]+180.0)
        MC = self.houses.ascmc[houses.Houses.MC]
        IC = util.normalize(self.houses.ascmc[houses.Houses.MC]+180.0)
        ascmc = [ASC, DESC, MC, IC]

        for i in range(num):
            ar = []

            val1 = self.fixstars.data[i][fixstars.FixStars.LON]+self.options.fixstars[self.fixstars.data[i][fixstars.FixStars.NOMNAME]]
            val2 = self.fixstars.data[i][fixstars.FixStars.LON]-self.options.fixstars[self.fixstars.data[i][fixstars.FixStars.NOMNAME]]

            for j in range(len(ascmc)):
                if (self.inorbsinister(val1, val2, ascmc[j], Chart.CONJUNCTIO)):
                    ar.append(j)

            if len(ar) != 0:
                fsar = (i, ar)
                self.fsaspmatrixangles.append(fsar)

        # Housecusps
        for i in range(num):
            ar = []

            val1 = self.fixstars.data[i][fixstars.FixStars.LON]+self.options.fixstars[self.fixstars.data[i][fixstars.FixStars.NOMNAME]]
            val2 = self.fixstars.data[i][fixstars.FixStars.LON]-self.options.fixstars[self.fixstars.data[i][fixstars.FixStars.NOMNAME]]

            for j in range(houses.Houses.HOUSE_NUM):
                if (j == 0 or j == 3 or j == 6 or j == 9) and (self.houses.hsys == 'P' or self.houses.hsys == 'K' or self.houses.hsys == 'O' or self.houses.hsys == 'R' or self.houses.hsys == 'C' or self.houses.hsys == 'E' or self.houses.hsys == 'T' or self.houses.hsys == 'B'):
                    continue

                if (self.inorbsinister(val1, val2, self.houses.cusps[j+1], Chart.CONJUNCTIO)):
                    ar.append(j)

            if len(ar) != 0:
                fsar = (i, ar)
                self.fsaspmatrixhcs.append(fsar)

        #LoF
        lonlof = self.fortune.fortune[fortune.Fortune.LON]
        for i in range(num):
            val1 = self.fixstars.data[i][fixstars.FixStars.LON]+self.options.fixstars[self.fixstars.data[i][fixstars.FixStars.NOMNAME]]
            val2 = self.fixstars.data[i][fixstars.FixStars.LON]-self.options.fixstars[self.fixstars.data[i][fixstars.FixStars.NOMNAME]]

            if (self.inorbsinister(val1, val2, lonlof, Chart.CONJUNCTIO)):
                self.fsaspmatrixlof.append(i)


    def recalc(self):
        del self.houses
        del self.planets

        del self.fortune
        del self.fixstars
        del self.midpoints
        del self.riseset
        del self.zodpars
        del self.antiscia
        del self.antzodpars
        del self.syzygy
        del self.almutens
        del self.parts
        del self.cpd
        del self.cpd2

        self.create()


    def recalcAlmutens(self):
        del self.almutens
        self.almutens = almutens.Almutens(self)


    def setCustomer(self, cpd):
        if self.cpd != None:
            del self.cpd

        self.cpd = cpd


    def setCustomer2(self, cpd2):
        if self.cpd2 != None:
            del self.cpd2

        self.cpd2 = cpd2


    def inorbsinister(self, val1, val2, pos, asp):
        '''Checks if inside orb (Pisces-Aries transition also!), val1 is leftorbboundary, val2 is rightorb boundary'''

        asppoint = pos+Chart.Aspects[asp]

        if (val1 >= 360.0 and val2 < 360.0) or (val1 > 0 and val2 < 0):#left is in Aries, right is in Pisces
            if (val1 >= 0 and val2 < 0):
                val1 += 360.0
                val2 += 360.0
            if asp == Chart.CONJUNCTIO and pos < 20.0: # 20.0 is arbitrary, just to see if the planet is close to the Pisces-Aries transition
                asppoint += 360.0
        else:
            val1 = util.normalize(val1)
            val2 = util.normalize(val2)
            asppoint = util.normalize(asppoint)

        if val1 > asppoint and val2 < asppoint:
            return True

        return False 


    def inorbdexter(self, val1, val2, pos, asp):
        '''Checks if inside orb (Pisces-Aries transition also!), val1 is leftorbboundary, val2 is rightorb boundary'''

        asppoint = pos-Chart.Aspects[asp]
        asppoint = util.normalize(asppoint)

        if (val1 >= 360.0 and val2 < 360.0) or (val1 > 0 and val2 < 0):#left is in Aries, right is in Pisces
            asppoint += 360.0
            if (val1 >= 0 and val2 < 0):
                val1 += 360.0
                val2 += 360.0
            if asppoint < 20.0: # 20.0 is arbitrary, just to see if the planet is close to the Pisces-Aries transition
                asppoint += 360.0
        else:
            val1 = util.normalize(val1)
            val2 = util.normalize(val2)

        if val1 > asppoint and val2 < asppoint:
            return True

        return False 


    def calcProfPos(self, prof):
        self.planets.calcProfPos(prof)
        self.houses.calcProfPos(prof)
        self.fortune.calcProfPos(prof)


    def printAspMatrix(self):
        planets = ('Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Node')        
        partxt = ('none', 'parallel', 'contrap')

        for i in range(self.planets.PLANETS_NUM-1):
            for j in range(self.planets.PLANETS_NUM-1):
                if j > i:
                    if self.aspmatrix[j][i].typ != Chart.NONE:
                        plel = 0
                        if self.aspmatrix[j][i].parallel == Chart.PARALLEL:
                            plel = 1
                        if self.aspmatrix[j][i].parallel == Chart.CONTRAPARALLEL:
                            plel = 2
                        extxt = ''
                        if self.aspmatrix[j][i].exact:
                            extxt = 'exact'
                        appltxt = 'sepa'
                        if self.aspmatrix[j][i].appl:
                            appltxt = 'appl'
                        print '%s - %s: type=%d diff=%f %s par=%s %s\n' % (planets[i], planets[j], self.aspmatrix[j][i].typ, self.aspmatrix[j][i].dif, appltxt, partxt[plel], extxt)

        print '\n'

        hname = ('Asc', '2', '3', 'X', '11', '12')
        hnum = 6
        for i in range(self.planets.PLANETS_NUM-2):
            for j in range(hnum):
                if self.aspmatrixH[j][i].typ != Chart.NONE:
                    extxt = ''
                    if self.aspmatrixH[j][i].exact:
                        extxt = 'exact'
                    appltxt = 'sepa'
                    if self.aspmatrixH[j][i].appl:
                        appltxt = 'appl'
                    print '%s - %s: type=%d %s diff=%f  %s\n' % (planets[i], hname[j], self.aspmatrixH[j][i].typ, appltxt, self.aspmatrixH[j][i].dif, extxt)


    def strongAspects(self, pid, pr_lon):
        planets_names = ('SU', 'MO', 'ME', 'VE', 'MA', 'JU', 'SA', 'UR', 'NE', 'PL', 'NN', 'NS')
        partxt = ('none', 'parallel', 'contrap')
        aspects_keys = self.options.aspects_keys
        strong_aspect = {
            'SU' : {'n' : '', 't' : '', 'd' : 0, 's' : 0, 'lon' : 0, 'lat' : 0, 'sp' : 0, 'prt' : '', 'prd' : 0},
            'MO' : {'n' : '', 't' : '', 'd' : 0, 's' : 0, 'lon' : 0, 'lat' : 0, 'sp' : 0, 'prt' : '', 'prd' : 0},
            'ME' : {'n' : '', 't' : '', 'd' : 0, 's' : 0, 'lon' : 0, 'lat' : 0, 'sp' : 0, 'prt' : '', 'prd' : 0},
            'VE' : {'n' : '', 't' : '', 'd' : 0, 's' : 0, 'lon' : 0, 'lat' : 0, 'sp' : 0, 'prt' : '', 'prd' : 0},
            'MA' : {'n' : '', 't' : '', 'd' : 0, 's' : 0, 'lon' : 0, 'lat' : 0, 'sp' : 0, 'prt' : '', 'prd' : 0},
            'JU' : {'n' : '', 't' : '', 'd' : 0, 's' : 0, 'lon' : 0, 'lat' : 0, 'sp' : 0, 'prt' : '', 'prd' : 0},
            'SA' : {'n' : '', 't' : '', 'd' : 0, 's' : 0, 'lon' : 0, 'lat' : 0, 'sp' : 0, 'prt' : '', 'prd' : 0},
            'UR' : {'n' : '', 't' : '', 'd' : 0, 's' : 0, 'lon' : 0, 'lat' : 0, 'sp' : 0, 'prt' : '', 'prd' : 0},
            'NE' : {'n' : '', 't' : '', 'd' : 0, 's' : 0, 'lon' : 0, 'lat' : 0, 'sp' : 0, 'prt' : '', 'prd' : 0},
            'PL' : {'n' : '', 't' : '', 'd' : 0, 's' : 0, 'lon' : 0, 'lat' : 0, 'sp' : 0, 'prt' : '', 'prd' : 0},
            'NN' : {'n' : '', 't' : '', 'd' : 0, 's' : 0, 'lon' : 0, 'lat' : 0, 'sp' : 0, 'prt' : '', 'prd' : 0},
            'NS' : {'n' : '', 't' : '', 'd' : 0, 's' : 0, 'lon' : 0, 'lat' : 0, 'sp' : 0, 'prt' : '', 'prd' : 0},
        }

        # get the aspects of our planet
        planet_aspects = self.getPlanetAspects(pid)

        # build the strong_aspect array
        for aspect in planet_aspects.aspects:
            # planet lon, lat and speed
            lon = int(self.planets.planets[aspect.pid].data[planets.Planet.LONG])
            lat = round(self.planets.planets[aspect.pid].data[planets.Planet.LAT], 1)
            speed = round(self.planets.planets[aspect.pid].data[planets.Planet.SPLON], 2)
            planet_name = planets_names[aspect.pid]
            strong_aspect[planet_name]['n'] = aspects_keys[aspect.typ]
            strong_aspect[planet_name]['aid'] = aspect.typ
            strong_aspect[planet_name]['t'] = aspect.appltxt + aspect.extxt
            strong_aspect[planet_name]['dex'] = aspect.dexter
            strong_aspect[planet_name]['ad'] = self.astrodinas[aspect.pid]
            strong_aspect[planet_name]['d'] = round(aspect.aspdif, 1)
            strong_aspect[planet_name]['s'] = self.calcAspectAstrodinas(aspect, self.astrodinas[aspect.pid])
            strong_aspect[planet_name]['lon'] = lon
            strong_aspect[planet_name]['lat'] = lat
            strong_aspect[planet_name]['sp'] = speed
            #print '%s - %s: type=%d diff=%f %s par=%s %s\n' % (planets[i], planets[asplanet_id], self.aspmatrix[j][i].typ, dif, appltxt, partxt[plel], extxt)

        # calculate aspect matrix to the radical point
        matrix_pos = 1
        self.calcPointAspMatrix(pr_lon, matrix_pos)
        for i in range(self.planets.PLANETS_NUM):
            # ignore the transit planets aspects due are alredy
            # as the main aspect
            if i == pid:
                continue
            if self.aspMatrixPoints[matrix_pos][i].typ != Chart.NONE:
                aspect = self.aspMatrixPoints[matrix_pos][i]
                if self.aspMatrixPoints[matrix_pos][i].aspdif > 180:
                    aspect.aspdif = 360.0 - self.aspMatrixPoints[matrix_pos][i].aspdif
                else:
                    aspect.aspdif = self.aspMatrixPoints[matrix_pos][i].aspdif

                # we are interested in the aspect that forms with radical point and the distance
                # of the aspect
                planet_name = planets_names[i]
                strong_aspect[planet_name]['prt'] = aspects_keys[aspect.typ]
                strong_aspect[planet_name]['prd'] = round(aspect.aspdif, 1)
                # just in case that this fields was not filled before due no aspect
                lon = int(self.planets.planets[i].data[planets.Planet.LONG])
                lat = round(self.planets.planets[i].data[planets.Planet.LAT], 1)
                speed = round(self.planets.planets[i].data[planets.Planet.SPLON], 2)
                strong_aspect[planet_name]['lon'] = lon
                strong_aspect[planet_name]['lat'] = lat
                strong_aspect[planet_name]['sp'] = speed

        return strong_aspect

    def getPlanetAspects(self, pid):
        planet_aspects = PlanetAspects()

        for i in range(self.planets.PLANETS_NUM-1):
            for j in range(1, self.planets.PLANETS_NUM-1):
                aspect = self.aspmatrix[j][i]
                aspect.plel = 0

                # Ignore if the aspect don't correspond to the interested planet
                if i == pid:
                    aspect.pid = j
                elif j == pid:
                    aspect.pid = i
                else:
                    continue
                if self.aspmatrix[j][i].typ != Chart.NONE:
                    # copy aspect instance to don't affect other parts with below alterations
                    if self.aspmatrix[j][i].parallel == Chart.PARALLEL:
                        aspect.plel = 1
                    if self.aspmatrix[j][i].parallel == Chart.CONTRAPARALLEL:
                        aspect.plel = 2

                    aspect.extxt = ''
                    if self.aspmatrix[j][i].exact:
                        aspect.extxt = 'E'

                    aspect.appltxt = 'S'
                    if self.aspmatrix[j][i].appl:
                        aspect.appltxt = 'A'

                    if self.aspmatrix[j][i].sinister:
                        aspect.dexter = 'F'
                    else:
                        aspect.dexter = 'T'

                    if self.aspmatrix[j][i].aspdif > 180:
                        aspect.aspdif = 360.0 - self.aspmatrix[j][i].aspdif
                    else:
                        aspect.aspdif = self.aspmatrix[j][i].aspdif

                    planet_aspects.aspects.append(aspect)

        return planet_aspects


    def calcAspectAstrodinas(self, aspect, planet_power = 0):
        '''Score how strong is an aspect depending on the orb.'''

        if aspect.appltxt in ['S', 'SE']:
            # reduce the distributable astrodinas when aspect is separative and more weaker
            decay_cons = 2
        else:
            # when aspect is aplicative or exact the decay is less proportional to the orb
            decay_cons = 5

        # get the proportional planet power based on the aspect it forms
        prop_planet_power = self.calcProportionalAstrodinas(aspect.typ, planet_power)
        # sum the power of the aspect plus power of the planet
        distribute_astrodinas = Asp.aspect_astrodinas[aspect.typ] + prop_planet_power
        # distribute the power proportional to the orb of the aspect
        given_astrodinas = distribute_astrodinas / math.exp(float(aspect.aspdif) / decay_cons)

        return round(given_astrodinas, 1)

    def calcProportionalAstrodinas(self, aspect_type, given_astrodinas):
        '''Calculate the proportion of power of planet astrodinas depending the potential of the aspect it forms'''
        # Total power must be proportional to the scale of the aspect
        # considering the maximum value as the totally power and getting the
        # proportion of the current aspect because in effect a conjuction will
        # be much strong than a semisextile.
        return given_astrodinas / (max(Asp.aspect_astrodinas) / Asp.aspect_astrodinas[aspect_type])
