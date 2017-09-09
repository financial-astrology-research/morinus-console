import math
import astrology
import chart
import houses
import util


class MunProfections:

	def __init__(self, radix, y, m, d, t, cnt=0): #t is in GMT
		placelon = radix.place.lon
		placelat = radix.place.lat #negative on SH?
		ramc = radix.houses.ascmc2[houses.Houses.MC][houses.Houses.RA]
		declAsc = radix.houses.ascmc2[houses.Houses.ASC][houses.Houses.DECL]
#radian!!
		oaAsc = util.normalize(ramc+90.0)
		val = math.tan(math.radians(declAsc))*math.tan(math.radians(placelat))
		adlatAsc = 0.0
		if math.fabs(val) <= 1.0:
			adlatAsc = math.degrees(math.asin(val))

		dsalatAsc = 90.0+adlatAsc
		nsalatAsc = 90.0-adlatAsc

		dhlatAsc = dsalatAsc/3.0 #diurnal house
		nhlatAsc = nsalatAsc/3.0 #nocturnal house

		#placelon is negative in case of western long!!
		lon360 = placelon
		if placelon < 0.0:
			lon360 = 360.0+placelon

		jdbirth = astrology.swe_julday(y, m, d, t, astrology.SE_GREG_CAL)
		jd = jdbirth+cnt*365.2421904

		#deltaYear
		diffYear = (jd-radix.time.jd)/365.2421904

		#Profection cycle in Years
		cycInYears = diffYear-(int(diffYear/12.0))*12

		#Number of diurnal steps (real)
		DCycInYears = cycInYears
		if cycInYears > 6.0:
			DCycInYears = 6.0

		#Number of nocturnal steps (real)
		NCycInYears = 0.0
		if cycInYears > 6.0:
			NCycInYears = cycInYears-DCycInYears

		# Delta geographical longitude for the fictious movement
		diffLon = DCycInYears*dhlatAsc+NCycInYears*nhlatAsc
		
		#New geographical long. to cast the fictious chart (range 0-360)
		lon360Z = util.normalize(lon360+diffLon)

		#Convert (0-360) --> E/W the longitude
		self.lonZ = lon360Z
		self.east = True
		if lon360Z > 180.0:
			self.lonZ = 360.0-lon360Z
			self.east = False

		#Cast the new chart. 1. Keep all the native data except for long. Instead of placelon use lonZ

		#planets will be handled in planets.py




