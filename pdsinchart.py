import math
import astrology
import houses
import chart
import util

class PDsInChart:

	def __init__(self, radix, da):
		placelon = radix.place.lon
		placelat = radix.place.lat #negative on SH?

#		calflag = astrology.SE_GREG_CAL
#		if radix.time.cal == chart.Time.JULIAN:
#			calflag = astrology.SE_JUL_CAL
		jdN = radix.time.jd #astrology.swe_julday(y, m, d, t, calflag)

		ramc = radix.houses.ascmc2[houses.Houses.MC][houses.Houses.RA]
		declAsc = radix.houses.ascmc2[houses.Houses.ASC][houses.Houses.DECL]

		oaAsc = util.normalize(ramc+90.0)
		val = math.tan(math.radians(declAsc))*math.tan(math.radians(placelat))
		adlatAsc = 0.0
		if math.fabs(val) <= 1.0:
			adlatAsc = math.degrees(math.asin(val))

		dsalatAsc = 90.0+adlatAsc
		nsalatAsc = 90.0-adlatAsc

		dhlatAsc = dsalatAsc/3.0 #diurnal house
		nhlatAsc = nsalatAsc/3.0 #nocturnal house

		deltaSdT = 240.0*da #in sec
#		t1 = int(deltaSdT/3600.0)
#		t2 = deltaSdT-t1*3600.0
#		t2 = int(t2/60.0)
#		t3 = deltaSdT-(t1*3600.0+t2*60.0)
#		print 'deltaSdT=%f' % deltaSdT
#		print 'deltaSdT=%02d:%02d:%02d' % (t1, t2, t3)

		deltaSrT = 0.9972695664*deltaSdT #sec
#		t1 = int(deltaSrT/3600.0)
#		t2 = deltaSrT-t1*3600.0
#		t2 = int(t2/60.0)
#		t3 = deltaSrT-(t1*3600.0+t2*60.0)
#		print 'deltaSrT=%f' % deltaSrT
#		print 'deltaSrT=%02d:%02d:%02d' % (t1, t2, t3)

		jdZ = jdN+deltaSrT/86400.0
#		print 'jdZ=%f' % jdZ

		self.yz, self.mz, self.dz, self.tz = astrology.swe_revjul(jdZ, 1) #cast a chart with this date and time for the natal place
#		print '%d.%d.%d %f' % (self.yz, self.mz, self.dz, self.tz)

		#rest is in planets.py  and fortune.py (calcMundaneProfPos [first two options], and calcFullAstronomicalProc [third, F in Roberto's algorithm])




