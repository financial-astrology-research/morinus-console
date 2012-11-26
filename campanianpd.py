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


class CampanianPD(regiocampbasepd.RegioCampBasePD):
	'Implements Campanian Primary Directions'

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
					wprom = util.normalize(wprom)
				else:
					if mundane:
						cmpap = plsig.speculums[primdirs.PrimDirs.REGIOSPECULUM][planets.Planet.CMP]+aspect
						cmpap = util.normalize(cmpap)

						zdap = math.fabs(cmpap-90.0)
						val = math.sin(math.radians(self.chart.place.lat))*math.sin(math.radians(zdap))
						if math.fabs(val) > 1.0:
							continue
						poleap = math.degrees(math.asin(val))
						if (self.chart.place.lat < 0.0 and poleap > 0.0) or (self.chart.place.lat > 0.0 and poleap < 0.0):
							poleap *= -1

						val = math.sin(math.radians(self.chart.place.lat))*math.sin(math.radians(cmpap))
						if math.fabs(val) > 1.0:
							continue
						declap = -math.degrees(math.asin(val))
						val = math.tan(math.radians(declap))*math.tan(math.radians(poleap))
						if math.fabs(val) > 1.0:
							continue
						qap = math.degrees(math.asin(val))

						X = math.degrees(math.atan(math.cos(math.radians(self.chart.place.lat))*math.tan(math.radians(cmpap))))

						raap = 0.0
						if (cmpap >= 0.0 and cmpap < 90.0) or (cmpap > 270.0 and cmpap <= 360.0):
							raap = self.ramc+90.0+X
							wsig = raap-qap
						if (cmpap > 90.0 and cmpap < 270.0):
							raap = self.ramc-90.0+X
							wsig = raap+qap
						raap = util.normalize(raap)
						wsig = util.normalize(wsig)

						val = math.tan(math.radians(declprom))*math.tan(math.radians(poleap))
						if math.fabs(val) > 1.0:
							continue
						qprom = math.degrees(math.asin(val))

						if (cmpap >= 0.0 and cmpap < 90.0) or (cmpap > 270.0 and cmpap <= 360.0):
							wprom = raprom-qprom
						if (cmpap > 90.0 and cmpap < 270.0):
							wprom = raprom+qprom
						wprom = util.normalize(wprom)
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
		'''Calculates directions of Promissor to intermediate house cusps'''

		#aspects of proms to HCs in Zodiacal!?

		ID = 0
		W = 1
		MD = 2
		UMD = 3
		EASTERN = 4

		#Campanus: Campanus AO/DO(w) of housecusps (equator)
		#Find addendus
		cusps = []
		for i in range(1, houses.Houses.HOUSE_NUM+1):
			ko = 60.000001+30.0*(float(i))
			dn = math.degrees(math.atan(math.tan(math.radians(ko))*math.cos(math.radians(self.chart.place.lat))))
			if (dn < 0.0):
				dn += 180.0
			if (math.sin(math.radians(ko)) < 0.0):
				dn += 180.0

			cusps.append(dn)

		HL = 30.0
		HC11 = util.normalize(self.ramc+cusps[10]) #AO11. = ARMC+addendus of cusp11
		HC12 = util.normalize(self.ramc+cusps[11])
		HC2 = util.normalize(self.ramc+cusps[1])
		HC3 = util.normalize(self.ramc+cusps[2])
		HC5 = util.normalize(self.ramc+cusps[4])
		HC6 = util.normalize(self.ramc+cusps[5])
		HC8 = util.normalize(self.ramc+cusps[7])
		HC9 = util.normalize(self.ramc+cusps[8])

		MD11 = cusps[10]
		MD12 = cusps[11]
		MD2 = util.normalize(math.fabs(self.raic-HC2))
		MD3 = util.normalize(math.fabs(self.raic-HC3))
		MD5 = util.normalize(math.fabs(self.raic-HC5))
		MD6 = util.normalize(math.fabs(self.raic-HC6))
		MD8 = util.normalize(math.fabs(self.ramc-HC8))
		MD9 = util.normalize(math.fabs(self.ramc-HC9))

		#housecusps
		hcps = ((primdirs.PrimDir.HC2, HC2, MD2, False, True), (primdirs.PrimDir.HC3, HC3, MD3, False, True), (primdirs.PrimDir.HC5, HC5, MD5, False, False), (primdirs.PrimDir.HC6, HC6, MD6, False, False), (primdirs.PrimDir.HC8, HC8, MD8, True, False), (primdirs.PrimDir.HC9, HC9, MD9, True, False), (primdirs.PrimDir.HC11, HC11, MD11, True, True), (primdirs.PrimDir.HC12, HC12, MD12, True, True))

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

		Cmp = 0.0
		if eastern:
			if umd:
				Cmp = 270+zd
			else:
				Cmp = 90-zd
		else:
			if umd:
				Cmp = 270-zd
			else:
				Cmp = 90+zd

		return True, util.normalize(Cmp)


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
				wprom = util.normalize(wprom)
			else:
				if mundane:
					cmpap = plsig.speculums[primdirs.PrimDirs.REGIOSPECULUM][planets.Planet.CMP]+aspect
					cmpap = util.normalize(cmpap)

					zdap = math.fabs(cmpap-90.0)

					val = math.sin(math.radians(self.chart.place.lat))*math.sin(math.radians(zdap))
					if math.fabs(val) > 1.0:
						return False, 0.0
					poleap = math.degrees(math.asin(val))
					if (self.chart.place.lat < 0.0 and poleap > 0.0) or (self.chart.place.lat > 0.0 and poleap < 0.0):
						poleap *= -1

					val = math.sin(math.radians(self.chart.place.lat))*math.sin(math.radians(cmpap))
					if math.fabs(val) > 1.0:
						return False, 0.0
					declap = -math.degrees(math.asin(val))
					val = math.tan(math.radians(declap))*math.tan(math.radians(poleap))
					if math.fabs(val) > 1.0:
						return False, 0.0
					qap = math.degrees(math.asin(val))

					X = math.degrees(math.atan(math.cos(math.radians(self.chart.place.lat))*math.tan(math.radians(cmpap))))

					raap = 0.0
					if (cmpap >= 0.0 and cmpap < 90.0) or (cmpap > 270.0 and cmpap <= 360.0):
						raap = self.ramc+90.0+X
						wsig = raap-qap
					if (cmpap > 90.0 and cmpap < 270.0):
						raap = self.ramc-90.0+X
						wsig = raap+qap
					raap = util.normalize(raap)
					wsig = util.normalize(wsig)

					val = math.tan(math.radians(declprom))*math.tan(math.radians(poleap))
					if math.fabs(val) > 1.0:
						return False, 0.0
					qprom = math.degrees(math.asin(val))

					if (cmpap >= 0.0 and cmpap < 90.0) or (cmpap > 270.0 and cmpap <= 360.0):
						wprom = raprom-qprom
					if (cmpap > 90.0 and cmpap < 270.0):
						wprom = raprom+qprom
					wprom = util.normalize(wprom)
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









