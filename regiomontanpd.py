import math
import astrology
import primdirs
import regiocampbasepd
import planets
import chart
import fortune
import houses
import secmotion
import util


class RegiomontanPD(regiocampbasepd.RegioCampBasePD):
	'Implements Regiomontanian Primary Directions'

	def __init__(self, chrt, options, pdrange, direction, abort):
		regiocampbasepd.RegioCampBasePD.__init__(self, chrt, options, pdrange, direction, abort)


	def toPlanet(self, mundane, idprom, idprom2, lonprom, latprom, raprom, declprom, promasp, sig, sigasp, calcsecmotion=True, paspect=chart.Chart.NONE):
		plsig = self.chart.planets.planets[sig]
		aspect = chart.Chart.Aspects[sigasp]

		SINISTER = 0
		DEXTER = 1

		for k in range(DEXTER+1):
			if k == DEXTER:
				if sigasp == chart.Chart.CONJUNCTIO or sigasp == chart.Chart.OPPOSITIO:
					break

				aspect *= -1

			wprom, wsig = 0.0, 0.0
			if mundane or self.options.subzodiacal == primdirs.PrimDirs.SZSIGNIFICATOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH: #mundane or zod with sig's latitude
				wsig = plsig.speculums[primdirs.PrimDirs.REGIOSPECULUM][planets.Planet.W]

				if sigasp == chart.Chart.CONJUNCTIO:
					val = math.tan(math.radians(declprom))*math.tan(math.radians(plsig.speculums[primdirs.PrimDirs.REGIOSPECULUM][planets.Planet.POLE]))
					if math.fabs(val) > 1.0:
						continue
					qprom = math.degrees(math.asin(val))
					if plsig.eastern:
						wprom = raprom-qprom
					else:
						wprom = raprom+qprom
					wprom = util.normalize(wprom)#
				else:
					if mundane:
						wsig += aspect
						wsig = util.normalize(wsig)
						med = math.fabs(self.ramc-wsig)
	
						if med > 180.0:
							med = 360.0-med
						icd = math.fabs(self.raic-wsig)
						if icd > 180.0:
							icd = 360.0-icd
						mdsig = med
						if icd < med:
							mdsig = icd

						val = math.tan(math.radians(declprom))*math.tan(math.radians(self.chart.place.lat))*math.sin(math.radians(mdsig))
						if math.fabs(val) > 1.0:
							continue
						qprom = math.degrees(math.asin(val))

						eastern = True
						if self.ramc > self.raic:
							if wsig > self.raic and wsig < self.ramc:
								eastern = False
						else:
							if (wsig > self.raic and wsig < 360.0) or (wsig < self.ramc and wsig > 0.0):
								eastern = False

						if eastern:
							wprom = raprom-qprom
						else:
							wprom = raprom+qprom
						wprom = util.normalize(wprom)#
					else:#zodiacal with sig's latitude
						lonsig = plsig.speculums[primdirs.PrimDirs.REGIOSPECULUM][planets.Planet.LONG]+aspect
						lonsig = util.normalize(lonsig)
						latsig = plsig.speculums[primdirs.PrimDirs.REGIOSPECULUM][planets.Planet.LAT]

						if self.options.bianchini:
							val = self.getBianchini(latsig, chart.Chart.Aspects[sigasp])
							if math.fabs(val) > 1.0:
								continue
							latsig = math.degrees(math.asin(val))

						ok, wsig, spole, seastern, md, umd = self.getZodW(plsig, lonsig, latsig)
						if not ok:
							continue

						ok, wprom, ppole, seastern, md, umd = self.getZodW(plsig, lonprom, latprom, spole, seastern)
						if not ok:
							continue
			else: #zodiacal
				lonsig = plsig.speculums[primdirs.PrimDirs.REGIOSPECULUM][planets.Planet.LONG]+aspect
				lonsig = util.normalize(lonsig)
				ok, wsig, spole, seastern, md, umd = self.getZodW(plsig, lonsig, 0.0)
				if not ok:
					continue

				ok, wprom, ppole, seastern, md, umd = self.getZodW(plsig, lonprom, latprom, spole, seastern)
				if not ok:
					continue

			arc = wprom-wsig
			ok = True
			if idprom == astrology.SE_MOON and idprom2 == primdirs.PrimDir.NONE and self.options.pdsecmotion and calcsecmotion:
				if paspect == chart.Chart.NONE:
					for itera in range(self.options.pdsecmotioniter+1):
						ok, arc = self.calcArcWithSM(mundane, idprom, latprom, sig, sigasp, aspect, arc)
						if not ok:
							break
				else:
					for itera in range(self.options.pdsecmotioniter+1):
						ok, arc = self.calcArcWithSM2(idprom, promasp, sig, paspect, arc)
						if not ok:
							break

			if ok:
				self.create(mundane, idprom, idprom2, sig, promasp, sigasp, arc)


	def toHCs(self, mundane, idprom, raprom, declprom, aspect, asp=0.0):
		'''Calculates directions of the Promissor to intermediate house cusps'''

		#aspects of proms to HCs in Zodiacal!?

		ID = 0
		W = 1
		MD = 2
		UMD = 3
		EASTERN = 4

		#Regiomontan: W of housecusps (equator)
		HL = 30.0
		HC11 = util.normalize(self.ramc+HL)
		HC12 = util.normalize(HC11+HL)
		HC2 = util.normalize(HC12+2*HL)
		HC3 = util.normalize(HC2+HL)
		HC5 = util.normalize(self.raic+HL)
		HC6 = util.normalize(HC5+HL)
		HC8 = util.normalize(HC6+2*HL)
		HC9 = util.normalize(HC8+HL)

		#housecusps
		hcps = ((primdirs.PrimDir.HC2, HC2, 2*HL, False, True), (primdirs.PrimDir.HC3, HC3, HL, False, True), (primdirs.PrimDir.HC5, HC5, HL, False, False), (primdirs.PrimDir.HC6, HC6, 2*HL, False, False), (primdirs.PrimDir.HC8, HC8, 2*HL, True, False), (primdirs.PrimDir.HC9, HC9, HL, True, False), (primdirs.PrimDir.HC11, HC11, HL, True, True), (primdirs.PrimDir.HC12, HC12, 2*HL, True, True))

		pl = self.chart.planets.planets[0]

		for h in range(len(hcps)):
			#get zd of HC
			zdsig = pl.getZD(hcps[h][MD], self.chart.place.lat, 0.0, hcps[h][UMD])
			val = math.sin(math.radians(self.chart.place.lat))*math.sin(math.radians(zdsig))
			if math.fabs(val) > 1.0:
				continue
			polesig = math.degrees(math.asin(val))

			val = math.tan(math.radians(declprom))*math.tan(math.radians(polesig))
			if math.fabs(val) > 1.0:
				continue
			qprom = math.degrees(math.asin(val))
			wprom = 0.0
			if hcps[h][EASTERN]:
				wprom = raprom-qprom
			else:
				wprom = raprom+qprom
			wprom = util.normalize(wprom)

			arc = wprom-hcps[h][W]
			ok = True
			if idprom == astrology.SE_MOON and self.options.pdsecmotion:
				for itera in range(self.options.pdsecmotioniter+1):
					ok, arc = self.calcHArcWithSM(mundane, idprom, h, hcps, arc, aspect, asp)
					if not ok:
						break

			if ok:
				self.create(mundane, idprom, primdirs.PrimDir.NONE, hcps[h][ID], aspect, chart.Chart.CONJUNCTIO, arc)


	def calcMP(self, ra, decl, pl):
		eastern = True
		if self.ramc > self.raic:
			if ra > self.raic and ra < self.ramc:
				eastern = False
		else:
			if (ra > self.raic and ra < 360.0) or (ra < self.ramc and ra > 0.0):
				eastern = False

		med = math.fabs(self.ramc-ra)

		if med > 180.0:
			med = 360.0-med
		icd = math.fabs(self.raic-ra)
		if icd > 180.0:
			icd = 360.0-icd

		md = med
		umd = True
		if icd < med:
			md = icd
			umd = False

		#zd
		zd = pl.getZD(md, self.chart.place.lat, decl, umd)

		#pole
		val = math.sin(math.radians(self.chart.place.lat))*math.sin(math.radians(zd))
		if math.fabs(val) > 1.0:
			return False, 0.0
		pole = math.degrees(math.asin(val))

		#Q
		val = math.tan(math.radians(decl))*math.tan(math.radians(pole))
		if math.fabs(val) > 1.0:
			return False, 0.0
		Q = math.degrees(math.asin(val))

		#W
		W = 0.0
		if eastern:
			W = ra-Q
		else:
			W = ra+Q

		return True, util.normalize(W)


#####################################Moon's SecMotion
	def calcArcWithSM(self, mundane, idprom, latprom, sig, sigasp, aspect, arc):
		sm = secmotion.SecMotion(self.chart.time, self.chart.place, idprom, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
		lonprom = sm.planet.speculums[primdirs.PrimDirs.REGIOSPECULUM][planets.Planet.LONG]
		raprom = sm.planet.speculums[primdirs.PrimDirs.REGIOSPECULUM][planets.Planet.RA]
		declprom = sm.planet.speculums[primdirs.PrimDirs.REGIOSPECULUM][planets.Planet.DECL]
		if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
			raprom, declprom, distprom = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

		plsig = self.chart.planets.planets[sig]

		wprom, wsig = 0.0, 0.0
		if mundane or self.options.subzodiacal == primdirs.PrimDirs.SZSIGNIFICATOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH: #mundane or zod with sig's latitude
			wsig = plsig.speculums[primdirs.PrimDirs.REGIOSPECULUM][planets.Planet.W]

			if sigasp == chart.Chart.CONJUNCTIO:
				val = math.tan(math.radians(declprom))*math.tan(math.radians(plsig.speculums[primdirs.PrimDirs.REGIOSPECULUM][planets.Planet.POLE]))
				if math.fabs(val) > 1.0:
					return False, 0.0
				qprom = math.degrees(math.asin(val))
				if plsig.eastern:
					wprom = raprom-qprom
				else:
					wprom = raprom+qprom
				wprom = util.normalize(wprom)#
			else:
				if mundane:
					wsig += aspect
					wsig = util.normalize(wsig)
					med = math.fabs(self.ramc-wsig)

					if med > 180.0:
						med = 360.0-med
					icd = math.fabs(self.raic-wsig)
					if icd > 180.0:
						icd = 360.0-icd
					mdsig = med
					if icd < med:
						mdsig = icd

					val = math.tan(math.radians(declprom))*math.tan(math.radians(self.chart.place.lat))*math.sin(math.radians(mdsig))
					if math.fabs(val) > 1.0:
						return False, 0.0
					qprom = math.degrees(math.asin(val))

					eastern = True
					if self.ramc > self.raic:
						if wsig > self.raic and wsig < self.ramc:
							eastern = False
					else:
						if (wsig > self.raic and wsig < 360.0) or (wsig < self.ramc and wsig > 0.0):
							eastern = False

					if eastern:
						wprom = raprom-qprom
					else:
						wprom = raprom+qprom
					wprom = util.normalize(wprom)#
				else:#zodiacal with sig's latitude
					lonsig = plsig.speculums[primdirs.PrimDirs.REGIOSPECULUM][planets.Planet.LONG]+aspect
					lonsig = util.normalize(lonsig)
					latsig = plsig.speculums[primdirs.PrimDirs.REGIOSPECULUM][planets.Planet.LAT]

					if self.options.bianchini:
						val = self.getBianchini(latsig, chart.Chart.Aspects[sigasp])
						if math.fabs(val) > 1.0:
							return False, 0.0
						latsig = math.degrees(math.asin(val))

					ok, wsig, spole, seastern, md, umd = self.getZodW(plsig, lonsig, latsig)
					if not ok:
						return False, 0.0

					ok, wprom, ppole, seastern, md, umd = self.getZodW(plsig, lonprom, latprom, spole, seastern)
					if not ok:
						return False, 0.0
		else: #zodiacal
			lonsig = plsig.speculums[primdirs.PrimDirs.REGIOSPECULUM][planets.Planet.LONG]+aspect
			lonsig = util.normalize(lonsig)
			ok, wsig, spole, seastern, md, umd = self.getZodW(plsig, lonsig, 0.0)
			if not ok:
				return False, 0.0

			ok, wprom, ppole, seastern, md, umd = self.getZodW(plsig, lonprom, latprom, spole, seastern)
			if not ok:
				return False, 0.0

		arc = wprom-wsig

		return True, arc


	def calcHArcWithSM(self, mundane, idprom, h, hcps, arc, aspect, asp=0.0):
		sm = secmotion.SecMotion(self.chart.time, self.chart.place, idprom, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)

		lonprom = sm.planet.speculums[primdirs.PrimDirs.REGIOSPECULUM][planets.Planet.LONG]
		pllat = sm.planet.speculums[primdirs.PrimDirs.REGIOSPECULUM][planets.Planet.LAT]
		raprom = sm.planet.speculums[primdirs.PrimDirs.REGIOSPECULUM][planets.Planet.RA]
		declprom = sm.planet.speculums[primdirs.PrimDirs.REGIOSPECULUM][planets.Planet.DECL]

		if not mundane:
			lonprom += asp
			lonprom = util.normalize(lonprom)
			latprom, raprom, declprom = 0.0, 0.0, 0.0
			if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
				if self.options.bianchini:
					val = self.getBianchini(pllat, chart.Chart.Aspects[aspect])
					if math.fabs(val) > 1.0:
						return False, 0.0
					latprom = math.degrees(math.asin(val))
				else:
					latprom = pllat

				#calc real(wahre)ra
#				raprom, declprom = util.getRaDecl(lonprom, latprom, self.chart.obl[0])
				raprom, declprom, dist = astrology.swe_cotrans(lonprom, latprom, 1.0, -self.chart.obl[0])
			else:
				raprom, declprom, distprom = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

		ID = 0
		W = 1
		MD = 2
		UMD = 3
		EASTERN = 4

		pl = self.chart.planets.planets[0]

		#get zd of HC
		zdsig = pl.getZD(hcps[h][MD], self.chart.place.lat, 0.0, hcps[h][UMD])

		val = math.sin(math.radians(self.chart.place.lat))*math.sin(math.radians(zdsig))
		if math.fabs(val) > 1.0:
			return False, 0.0
		polesig = math.degrees(math.asin(val))

		val = math.tan(math.radians(declprom))*math.tan(math.radians(polesig))
		if math.fabs(val) > 1.0:
			return False, 0.0
		qprom = math.degrees(math.asin(val))
		wprom = 0.0
		if hcps[h][EASTERN]:
			wprom = raprom-qprom
		else:
			wprom = raprom+qprom
		wprom = util.normalize(wprom)

		return True, wprom-hcps[h][W]








