import math
import astrology
import primdirs
import planets
import chart
import fixstars
import fortune
import syzygy
import secmotion
import customerpd
import util


class PlacidianCommonPD(primdirs.PrimDirs):
	'Implements Placidian Common(semiarc, utp) Primary Directions'

	def __init__(self, chrt, options, pdrange, direction, abort):
		primdirs.PrimDirs.__init__(self, chrt, options, pdrange, direction, abort)


	def calc2HouseCusps(self, mundane):
		'''Calculates directions of Promissors to intermediate house cusps'''

		#aspects of proms to HCs in Zodiacal!?

		for i in range(len(self.chart.planets.planets)):
			if not self.options.promplanets[i]:
				continue

			if self.abort.abort:
				return

			pl = self.chart.planets.planets[i]
			rapl = pl.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.RA]
			dsa = pl.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.SA]
			nsa = pl.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.SA]

			if dsa < 0.0:
				dsa = 180.0+dsa
				nsa *= -1
			else:
				nsa = 180.0-dsa
				
			if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
				rapl, declpl, dist = astrology.swe_cotrans(pl.data[planets.Planet.LONG], 0.0, 1.0, -self.chart.obl[0])
				val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declpl))
				if math.fabs(val) > 1.0:
					continue
				adlat = math.degrees(math.asin(val))
				dsa = 90.0+adlat
				nsa = 90.0-adlat

			self.toHCs(mundane, i, rapl, dsa, nsa, chart.Chart.CONJUNCTIO)


	def calcZodPromAsps2HCs(self):
		'''Calclucates zodiacal directions of the aspects of promissors to housecusps'''

		NODES = 2

		SINISTER = 0
		DEXTER = 1

		for p in range(len(self.chart.planets.planets)-NODES):
			if not self.options.promplanets[p]:
				continue

			plprom = self.chart.planets.planets[p]
			pllat = plprom.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LAT]
#			raprom = plprom.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.RA]
#			adprom = plprom.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.ADLAT]

			for psidx in range(chart.Chart.CONJUNCTIO+1, chart.Chart.OPPOSITIO+1):
				if not self.options.pdaspects[psidx]:
					continue

				if self.abort.abort:
					return

				for k in range(DEXTER+1):
					aspect = chart.Chart.Aspects[psidx]
					if k == DEXTER:
						if psidx == chart.Chart.OPPOSITIO:
							break

						aspect *= -1

					lon = plprom.data[planets.Planet.LONG]+aspect
					lon = util.normalize(lon)
					raprom, adprom = 0.0, 0.0
					if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
						latprom = 0.0
						if self.options.bianchini:
							val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
							if math.fabs(val) > 1.0:
								continue
							latprom = math.degrees(math.asin(val))
						else:
							latprom = pllat

						#calc real(wahre)ra and adlat
#						raprom, declprom = util.getRaDecl(lon, latprom, self.chart.obl[0])
						raprom, declprom, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
						val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
						if math.fabs(val) > 1.0:
							continue
						adprom = math.degrees(math.asin(val))
					else:
						raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
						val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
						if math.fabs(val) > 1.0:
							continue
						adprom = math.degrees(math.asin(val))

					dsa = 90.0+adprom
					nsa = 90.0-adprom
					self.toHCs(False, p, raprom, dsa, nsa, psidx, aspect)


	def calcCustomer2HouseCusps(self, mundane):
		'''Calculates directions of Customer-Promissor to intermediate house cusps'''

		lonpl = self.chart.cpd.speculums[primdirs.PrimDirs.PLACSPECULUM][customerpd.CustomerPD.LONG]
		rapl = self.chart.cpd.speculums[primdirs.PrimDirs.PLACSPECULUM][customerpd.CustomerPD.RA]
		dsa = self.chart.cpd.speculums[primdirs.PrimDirs.PLACSPECULUM][customerpd.CustomerPD.SA]
		nsa = self.chart.cpd.speculums[primdirs.PrimDirs.PLACSPECULUM][customerpd.CustomerPD.SA]

		if dsa < 0.0:
			dsa = 180.0+dsa
			nsa *= -1
		else:
			nsa = 180.0-dsa
				
		if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
			rapl, declpl, dist = astrology.swe_cotrans(lonpl, 0.0, 1.0, -self.chart.obl[0])
			val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declpl))
			if math.fabs(val) > 1.0:
				return
			adlat = math.degrees(math.asin(val))
			dsa = 90.0+adlat
			nsa = 90.0-adlat

		self.toHCs(mundane, primdirs.PrimDir.CUSTOMERPD, rapl, dsa, nsa, chart.Chart.CONJUNCTIO)


	def calcAntiscia2HouseCusps(self, mundane):
		'''Calculates directions of Promissors to intermediate house cusps'''

		self.calcAntiscia2HouseCuspsSub(mundane, self.chart.antiscia.plantiscia, primdirs.PrimDir.ANTISCION)
		self.calcAntiscia2HouseCuspsSub(mundane, self.chart.antiscia.plcontraant, primdirs.PrimDir.CONTRAANT)


	def calcAntiscia2HouseCuspsSub(self, mundane, pls, offs):
		#aspects of proms to HCs in Zodiacal!?

		for i in range(len(pls)):
			if not self.options.promplanets[i]:
				continue

			if self.abort.abort:
				return

			pl = pls[i]
			lonpl = pl.lon
			rapl = pl.ra
			declpl = pl.decl
				
			if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
				rapl, declpl, dist = astrology.swe_cotrans(lonpl, 0.0, 1.0, -self.chart.obl[0])

			val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declpl))
			if math.fabs(val) > 1.0:
				continue
			adlat = math.degrees(math.asin(val))
			dsa = 90.0+adlat
			nsa = 90.0-adlat

			self.toHCs(mundane, i+offs, rapl, dsa, nsa, chart.Chart.CONJUNCTIO)


	def calcZodFixStars2HouseCusps(self):
		'''Calculates zodiacal directions of fixstars to HCs'''

		OFFS = primdirs.PrimDir.FIXSTAR

		for i in range(len(self.chart.fixstars.data)):
			if not self.options.pdfixstarssel[self.chart.fixstars.mixed[i]]:
				continue

			if self.abort.abort:
				return

			star = self.chart.fixstars.data[i]
			lonstar = star[fixstars.FixStars.LON]
			rastar = star[fixstars.FixStars.RA]
			declstar = star[fixstars.FixStars.DECL]

			if self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
				rastar, declstar, dist = astrology.swe_cotrans(lonstar, 0.0, 1.0, -self.chart.obl[0])

			val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declstar))
			if math.fabs(val) > 1.0:
				continue
			adstar = math.degrees(math.asin(val))

			dsa = 90.0+adstar
			nsa = 90.0-adstar

			self.toHCs(False, i+OFFS, rastar, dsa, nsa, chart.Chart.CONJUNCTIO)


	def	calcZodLoF2HouseCusps(self):
		'''Calculates zodiacal LoF to housecusps'''

		ralof = self.chart.fortune.fortune[fortune.Fortune.RA]
		decllof = self.chart.fortune.fortune[fortune.Fortune.DECL]
		val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(decllof))
		if math.fabs(val) > 1.0:
			return
		adlat = math.degrees(math.asin(val))

		dsa = 90.0+adlat
		nsa = 90.0-adlat
		self.toHCs(False, primdirs.PrimDir.LOF, ralof, dsa, nsa, chart.Chart.CONJUNCTIO)


	def toHCs(self, mundane, idprom, raprom, dsa, nsa, aspect, asp=0.0):
		#day-house, night-house length
		dh = dsa/3.0
		nh = nsa/3.0

		#ra rise, ra set
		rar = self.ramc+dsa
		ras = self.raic+nsa

		rar = util.normalize(rar)
		ras = util.normalize(ras)

		#ra housecusps
		rahcps = ((primdirs.PrimDir.HC2, rar+nh), (primdirs.PrimDir.HC3, rar+2*nh), (primdirs.PrimDir.HC5, self.raic+nh), (primdirs.PrimDir.HC6, self.raic+2*nh), (primdirs.PrimDir.HC8, ras+dh), (primdirs.PrimDir.HC9, ras+2*dh), (primdirs.PrimDir.HC11, self.ramc+dh), (primdirs.PrimDir.HC12, self.ramc+2*dh))

		for h in range(len(rahcps)):
			rahcp = rahcps[h][1]
			rahcp = util.normalize(rahcp)

			arc = raprom-rahcp
			ok = True
			if idprom == astrology.SE_MOON and self.options.pdsecmotion:
				for itera in range(self.options.pdsecmotioniter+1):
					ok, arc = self.calcHArcWithSM(mundane, idprom, h, arc, aspect, asp)
					if not ok:
						break

			if ok:
				self.create(mundane, idprom, primdirs.PrimDir.NONE, rahcps[h][0], aspect, chart.Chart.CONJUNCTIO, arc)


	def calcMP(self, ra, decl, pl):
		eastern = True
		if self.ramc > self.raic:
			if ra > self.raic and ra < self.ramc:
				eastern = False
		else:
			if (ra > self.raic and ra < 360.0) or (ra < self.ramc and ra > 0.0):
				eastern = False

		#adlat
		val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(decl))
		if math.fabs(val) > 1.0:
			return False, 0.0
		adlat = math.degrees(math.asin(val))

		#md
		med = math.fabs(self.ramc-ra)

		if med > 180.0:
			med = 360.0-med
		icd = math.fabs(self.raic-ra)
		if icd > 180.0:
			icd = 360.0-icd

		md = med
		if icd < med:
			md = icd

		#sa (southern hemisphere!?)
		dsa = 90.0+adlat
		nsa = 90.0-adlat

		abovehorizon = True
		if med > dsa:
			abovehorizon = False

		sa = dsa
		if not abovehorizon:
			sa = nsa

		if not abovehorizon and eastern:
			pmp = 90.0-90.0*(md/sa)
		elif not abovehorizon and not eastern:
			pmp = 90.0+90.0*(md/sa)
		elif abovehorizon and not eastern:
			pmp = 270.0-90.0*(md/sa)
		elif abovehorizon and eastern:
			pmp = 270.0+90.0*(md/sa)

		return True, pmp
		

##################################### Sec. Motion of the Moon
	def calcHArcWithSM(self, mundane, idprom, h, arc, aspect, asp=0.0):
		sm = secmotion.SecMotion(self.chart.time, self.chart.place, idprom, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
		lonprom = sm.planet.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LONG]
		pllat = sm.planet.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LAT]
		raprom = sm.planet.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.RA]
		dsa = sm.planet.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.SA]
		nsa = sm.planet.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.SA]

		if dsa < 0.0:
			dsa = 180.0+dsa
			nsa *= -1
		else:
			nsa = 180.0-dsa

		if not mundane:
			lonprom += asp
			lonprom = util.normalize(lonprom)
			latprom, raprom, adprom = 0.0, 0.0, 0.0
			if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
				latprom = 0.0
				if self.options.bianchini:
					val = self.getBianchini(pllat, chart.Chart.Aspects[aspect])
					if math.fabs(val) > 1.0:
						return False, 0.0
					latprom = math.degrees(math.asin(val))
				else:
					latprom = pllat

				#calc real(wahre)ra and adlat
#				raprom, declprom = util.getRaDecl(lonprom, latprom, self.chart.obl[0])
				raprom, declprom, dist = astrology.swe_cotrans(lonprom, latprom, 1.0, -self.chart.obl[0])
				val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
				if math.fabs(val) > 1.0:
					return False, 0.0
				adprom = math.degrees(math.asin(val))
			else:
				raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
				val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
				if math.fabs(val) > 1.0:
					return False, 0.0
				adprom = math.degrees(math.asin(val))

			dsa = 90.0+adprom
			nsa = 90.0-adprom

		#day-house, night-house length
		dh = dsa/3.0
		nh = nsa/3.0

		#ra rise, ra set
		rar = self.ramc+dsa
		ras = self.raic+nsa

		rar = util.normalize(rar)
		ras = util.normalize(ras)

		#ra housecusps
		rahcps = ((primdirs.PrimDir.HC2, rar+nh), (primdirs.PrimDir.HC3, rar+2*nh), (primdirs.PrimDir.HC5, self.raic+nh), (primdirs.PrimDir.HC6, self.raic+2*nh), (primdirs.PrimDir.HC8, ras+dh), (primdirs.PrimDir.HC9, ras+2*dh), (primdirs.PrimDir.HC11, self.ramc+dh), (primdirs.PrimDir.HC12, self.ramc+2*dh))

		rahcp = rahcps[h][1]
		rahcp = util.normalize(rahcp)

		arc = raprom-rahcp

		return True, arc





