import math
import astrology
import primdirs
import placidiancommonpd
import planets
import houses
import chart
import fortune
import syzygy
import fixstars
import secmotion
import customerpd
import util


#The UTP is zodiacal only.

class PlacidianUTPPD(placidiancommonpd.PlacidianCommonPD):
	'Implements Placidian(UnderThePole) Primary Directions'

	def __init__(self, chrt, options, pdrange, direction, abort):
		placidiancommonpd.PlacidianCommonPD.__init__(self, chrt, options, pdrange, direction, abort)


	def calcInterPlanetary(self, mundane):
		'''Calculates mundane/zodiacal directions of the promissors to aspects of significators'''

		for p in range(len(self.chart.planets.planets)):
			if not self.options.promplanets[p]:
				continue

			if self.abort.abort:
				return

			plprom = self.chart.planets.planets[p]
			lonprom = plprom.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LONG]
			raprom = plprom.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.RA]
			declprom = plprom.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.DECL]

			if self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
				raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

			self.toPlanets(mundane, p, raprom, declprom)


	def calcCustomerPlanetary(self, mundane):
		'''Calculates mundane/zodiacal directions of the Customer-promissor to aspects of significators'''

		lonprom = self.chart.cpd.speculums[primdirs.PrimDirs.PLACSPECULUM][customerpd.CustomerPD.LONG]
		raprom = self.chart.cpd.speculums[primdirs.PrimDirs.PLACSPECULUM][customerpd.CustomerPD.RA]
		declprom = self.chart.cpd.speculums[primdirs.PrimDirs.PLACSPECULUM][customerpd.CustomerPD.DECL]

		if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
			#recalc zodiacals
			raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

		self.toPlanets(mundane, primdirs.PrimDir.CUSTOMERPD, raprom, declprom)


	def calcPlanetary2Customer2(self, mundane):
		'''Calculates mundane/zodiacal directions of the promissors to the Customer2 point'''

		for p in range(len(self.chart.planets.planets)):
			if not self.options.promplanets[p]:
				continue

			if self.abort.abort:
				return

			plprom = self.chart.planets.planets[p]
			raprom = plprom.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.RA]
			declprom = plprom.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.DECL]

			if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
				#recalc zodiacals
				raprom, declprom, dist = astrology.swe_cotrans(plprom.data[planets.Planet.LONG], 0.0, 1.0, -self.chart.obl[0])

			self.toCustomer2(mundane, p, primdirs.PrimDir.NONE, raprom, declprom, chart.Chart.CONJUNCTIO, 0.0, True)


	def calcAntiscia2Planets(self, mundane):
		'''Calculates mundane/zodiacal directions of the antiscia to aspects of significators'''

		self.calcAntiscia2PlanetsSub(mundane, self.chart.antiscia.plantiscia, primdirs.PrimDir.ANTISCION)
		self.calcAntiscia2PlanetsSub(mundane, self.chart.antiscia.plcontraant, primdirs.PrimDir.CONTRAANT)

		if not mundane:
			#Antiscia/Contraant of LoF
			if self.options.pdlof[0]:
				ant = self.chart.antiscia.lofant
				ralofant = ant.ra
				decllofant = ant.decl
				self.toPlanets(mundane, primdirs.PrimDir.ANTISCIONLOF, ralofant, decllofant)

				#Contra
				cant = self.chart.antiscia.lofcontraant
				ralofcant = cant.ra
				decllofcant = cant.decl
				self.toPlanets(mundane, primdirs.PrimDir.CONTRAANTLOF, ralofcant, decllofcant)

			#Antiscia of AscMC
			for i in range(2):
				ant = self.chart.antiscia.ascmcant[i]
				raant = ant.ra
				declant = ant.decl

				typ = primdirs.PrimDir.ANTISCIONASC
				if i > 0:
					typ = primdirs.PrimDir.ANTISCIONMC

				self.toPlanets(mundane, typ, raant, declant)

			#Contraantiscia of AscMC
			for i in range(2):
				cant = self.chart.antiscia.ascmccontraant[i]
				racant = cant.ra
				declcant = cant.decl

				typ = primdirs.PrimDir.CONTRAANTASC
				if i > 0:
					typ = primdirs.PrimDir.CONTRAANTMC

				self.toPlanets(mundane, typ, racant, declcant)


	def calcAntiscia2PlanetsSub(self, mundane, pls, offs):
		for p in range(len(pls)):
			if not self.options.promplanets[p]:
				continue

			if self.abort.abort:
				return

			plprom = pls[p]
			lonprom = plprom.lon
			raprom = plprom.ra
			declprom = plprom.decl

			if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
				#recalc zodiacals
				raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

			self.toPlanets(mundane, p+offs, raprom, declprom)


	def calcAntiscia2Customer2(self, mundane):
		'''Calculates mundane/zodiacal directions of the antiscia to aspects of significators'''

		self.calcAntiscia2Customer2Sub(mundane, self.chart.antiscia.plantiscia, primdirs.PrimDir.ANTISCION)
		self.calcAntiscia2Customer2Sub(mundane, self.chart.antiscia.plcontraant, primdirs.PrimDir.CONTRAANT)

		if not mundane:
			#Antiscia/Contraant of LoF
			if self.options.pdlof[0]:
				ant = self.chart.antiscia.lofant
				ralofant = ant.ra
				decllofant = ant.decl

				self.toCustomer2(mundane, primdirs.PrimDir.ANTISCIONLOF, primdirs.PrimDir.NONE, ralofant, decllofant, chart.Chart.CONJUNCTIO)

				#Contra
				cant = self.chart.antiscia.lofcontraant
				ralofcant = cant.ra
				decllofcant = cant.decl
				self.toCustomer2(mundane, primdirs.PrimDir.CONTRAANTLOF, primdirs.PrimDir.NONE, ralofcant, decllofcant, chart.Chart.CONJUNCTIO)

			#Antiscia of AscMC
			for i in range(2):
				ant = self.chart.antiscia.ascmcant[i]
				raant = ant.ra
				declant = ant.decl

				typ = primdirs.PrimDir.ANTISCIONASC
				if i > 0:
					typ = primdirs.PrimDir.ANTISCIONMC

				self.toCustomer2(mundane, typ, primdirs.PrimDir.NONE, raant, declant, chart.Chart.CONJUNCTIO)

			#Contraantiscia of AscMC
			for i in range(2):
				cant = self.chart.antiscia.ascmccontraant[i]
				racant = cant.ra
				declcant = cant.decl

				typ = primdirs.PrimDir.CONTRAANTASC
				if i > 0:
					typ = primdirs.PrimDir.CONTRAANTMC

				self.toCustomer2(mundane, typ, primdirs.PrimDir.NONE, racant, declcant, chart.Chart.CONJUNCTIO)


	def calcAntiscia2Customer2Sub(self, mundane, pls, offs):
		for p in range(len(pls)):
			if not self.options.promplanets[p]:
				continue

			if self.abort.abort:
				return

			plprom = pls[p]
			lonprom = plprom.lon
			raprom = plprom.ra
			declprom = plprom.decl

			if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
				#recalc zodiacals
				raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

			self.toCustomer2(mundane, p+offs, primdirs.PrimDir.NONE, raprom, declprom, chart.Chart.CONJUNCTIO)


	def calcZodPromAspsInterPlanetary(self):
		'''Calclucates zodiacal directions of the aspects of promissors to significators'''
		SINISTER = 0
		DEXTER = 1

		NODES = 2

		for p in range(len(self.chart.planets.planets)-NODES):
			if not self.options.promplanets[p]:
				continue

			plprom = self.chart.planets.planets[p]
			pllat = plprom.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LAT]

			for promasp in range(chart.Chart.CONJUNCTIO+1, chart.Chart.OPPOSITIO+1):
				if not self.options.pdaspects[promasp]:
					continue

				if self.abort.abort:
					return

				for k in range(DEXTER+1):
					aspect = chart.Chart.Aspects[promasp]
					if k == DEXTER:
						if promasp == chart.Chart.OPPOSITIO:
							break

						aspect *= -1

					lonprom = plprom.data[planets.Planet.LONG]+aspect
					lonprom = util.normalize(lonprom)
					raprom, declprom = 0.0, 0.0
					if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
						latprom = 0.0
						if self.options.bianchini:
							val = self.getBianchini(pllat, chart.Chart.Aspects[promasp])
							if math.fabs(val) > 1.0:
								continue
							latprom = math.degrees(math.asin(val))
						else:
							latprom = pllat

						raprom, declprom, dist = astrology.swe_cotrans(lonprom, latprom, 1.0, -self.chart.obl[0])
					else:
						raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

					for s in range(len(self.chart.planets.planets)):
						if not self.options.sigplanets[s]:
							continue

						if self.abort.abort:
							return

						self.toPlanet(False, p, primdirs.PrimDir.NONE, raprom, declprom, promasp, s, chart.Chart.CONJUNCTIO, True, aspect)


	def calcZodPromAspsInterPlanetary2Customer2(self):
		'''Calclucates zodiacal directions of the aspects of promissors to Customer2'''

		SINISTER = 0
		DEXTER = 1

		NODES = 2

		for p in range(len(self.chart.planets.planets)-NODES):
			if not self.options.promplanets[p]:
				continue

			plprom = self.chart.planets.planets[p]
			pllat = plprom.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LAT]

			for promasp in range(chart.Chart.CONJUNCTIO+1, chart.Chart.OPPOSITIO+1):
				if not self.options.pdaspects[promasp]:
					continue

				if self.abort.abort:
					return

				for k in range(DEXTER+1):
					aspect = chart.Chart.Aspects[promasp]
					if k == DEXTER:
						if promasp == chart.Chart.OPPOSITIO:
							break

						aspect *= -1

					lonprom = plprom.data[planets.Planet.LONG]+aspect
					lonprom = util.normalize(lonprom)
					raprom, declprom = 0.0, 0.0
					if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
						latprom = 0.0
						if self.options.bianchini:
							val = self.getBianchini(pllat, chart.Chart.Aspects[promasp])
							if math.fabs(val) > 1.0:
								continue
							latprom = math.degrees(math.asin(val))
						else:
							latprom = pllat

						raprom, declprom, dist = astrology.swe_cotrans(lonprom, latprom, 1.0, -self.chart.obl[0])
					else:
						raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

					self.toCustomer2(False, p, primdirs.PrimDir.NONE, raprom, declprom, promasp, aspect, True)


	def calcZodPromAntisciaAspsInterPlanetary(self):
		'''Calclucates zodiacal directions of the aspects of Antiscia to significators'''

		self.calcZodPromAntisciaAspsInterPlanetarySub(self.chart.antiscia.plantiscia, primdirs.PrimDir.ANTISCION)
		self.calcZodPromAntisciaAspsInterPlanetarySub(self.chart.antiscia.plcontraant, primdirs.PrimDir.CONTRAANT)


	def calcZodPromAntisciaAspsInterPlanetarySub(self, pls, offs):
		SINISTER = 0
		DEXTER = 1

		NODES = 2

		for p in range(len(self.chart.planets.planets)-NODES):
			if not self.options.promplanets[p]:
				continue

			plprom = pls[p]
			pllat = plprom.lat

			for promasp in range(chart.Chart.CONJUNCTIO+1, chart.Chart.OPPOSITIO+1):
				if not self.options.pdaspects[promasp]:
					continue

				if self.abort.abort:
					return

				for k in range(DEXTER+1):
					aspect = chart.Chart.Aspects[promasp]
					if k == DEXTER:
						if promasp == chart.Chart.OPPOSITIO:
							break

						aspect *= -1

					lonprom = plprom.lon+aspect
					lonprom = util.normalize(lonprom)
					raprom, declprom = 0.0, 0.0
					if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
						latprom = 0.0
						if self.options.bianchini:
							val = self.getBianchini(pllat, chart.Chart.Aspects[promasp])
							if math.fabs(val) > 1.0:
								continue
							latprom = math.degrees(math.asin(val))
						else:
							latprom = pllat

						raprom, declprom, dist = astrology.swe_cotrans(lonprom, latprom, 1.0, -self.chart.obl[0])
					else:
						raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

					for s in range(len(self.chart.planets.planets)):
						if not self.options.sigplanets[s]:
							continue

						if self.abort.abort:
							return

						self.toPlanet(False, p+offs, primdirs.PrimDir.NONE, raprom, declprom, promasp, s, chart.Chart.CONJUNCTIO)


	def calcZodPromAntisciaAspsInterPlanetary2Customer2(self):
		'''Calclucates zodiacal directions of the aspects of Antiscia to Customer2'''

		self.calcZodPromAntisciaAspsInterPlanetary2Customer2Sub(self.chart.antiscia.plantiscia, primdirs.PrimDir.ANTISCION)
		self.calcZodPromAntisciaAspsInterPlanetary2Customer2Sub(self.chart.antiscia.plcontraant, primdirs.PrimDir.CONTRAANT)


	def calcZodPromAntisciaAspsInterPlanetary2Customer2Sub(self, pls, offs):

		SINISTER = 0
		DEXTER = 1

		NODES = 2

		for p in range(len(self.chart.planets.planets)-NODES):
			if not self.options.promplanets[p]:
				continue

			plprom = pls[p]
			pllat = plprom.lat

			for promasp in range(chart.Chart.CONJUNCTIO+1, chart.Chart.OPPOSITIO+1):
				if not self.options.pdaspects[promasp]:
					continue

				if self.abort.abort:
					return

				for k in range(DEXTER+1):
					aspect = chart.Chart.Aspects[promasp]
					if k == DEXTER:
						if promasp == chart.Chart.OPPOSITIO:
							break

						aspect *= -1

					lonprom = plprom.lon+aspect
					lonprom = util.normalize(lonprom)
					raprom, declprom = 0.0, 0.0
					if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
						latprom = 0.0
						if self.options.bianchini:
							val = self.getBianchini(pllat, chart.Chart.Aspects[promasp])
							if math.fabs(val) > 1.0:
								continue
							latprom = math.degrees(math.asin(val))
						else:
							latprom = pllat

						raprom, declprom, dist = astrology.swe_cotrans(lonprom, latprom, 1.0, -self.chart.obl[0])
					else:
						raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

					self.toCustomer2(False, p+offs, primdirs.PrimDir.NONE, raprom, declprom, promasp, aspect, True)


	def calcZodAsc2Planets(self):
		'''Calculates zodiacal Asc and its aspects to Planets'''

		lonprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON]
		self.calcZodAscMC2Planets(primdirs.PrimDir.ASC, lonprom)


	def calcZodMC2Planets(self):
		'''Calculates zodiacal MC and its aspects to Planets'''

		lonprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]
		self.calcZodAscMC2Planets(primdirs.PrimDir.MC, lonprom)


	def calcZodAscMC2Planets(self, p, lonprom):
		SINISTER = 0
		DEXTER = 1

		beg = chart.Chart.CONJUNCTIO
		if self.options.zodpromsigasps[primdirs.PrimDirs.PROMSTOSIGASPS]:
			beg += 1

#		for psidx in range(beg, chart.Chart.OPPOSITIO+1):
		for psidx in range(beg, chart.Chart.CONJUNCTIO+1):
			if not self.options.pdaspects[psidx]:
				continue

			if not self.options.zodpromsigasps[primdirs.PrimDirs.ASPSPROMSTOSIGS] and psidx > chart.Chart.CONJUNCTIO:
				break

			if self.abort.abort:
				return

			for k in range(DEXTER+1):
				aspect = chart.Chart.Aspects[psidx]
				if k == DEXTER:
					if psidx == chart.Chart.CONJUNCTIO or psidx == chart.Chart.OPPOSITIO:
						break

					aspect *= -1

				lon = util.normalize(lonprom+aspect)
				raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])

				for s in range(len(self.chart.planets.planets)):
					if not self.options.sigplanets[s]:
						continue

					if self.abort.abort:
						return

					plsig = self.chart.planets.planets[s]
					self.toPlanet(False, p, primdirs.PrimDir.NONE, raprom, declprom, psidx, s, chart.Chart.CONJUNCTIO)


	def calcZodAsc2AspPlanets(self):
		'''Calculates zodiacal Asc to Planets and their aspects'''

		lonprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON]
		raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

		self.toPlanets(False, primdirs.PrimDir.ASC, raprom, declprom)


	def calcZodAsc2ParallelPlanets(self):
		lonprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON]
		raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

		self.toZodParallels(primdirs.PrimDir.ASC, raprom, declprom)


	def calcZodMC2AspPlanets(self):
		'''Calculates zodiacal MC to Planets and their aspects'''

		lonprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]
		raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

		self.toPlanets(False, primdirs.PrimDir.MC, raprom, declprom)


	def calcZodMC2ParallelPlanets(self):
		lonprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]
		raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

		self.toZodParallels(primdirs.PrimDir.MC, raprom, declprom)


	def calcZodAsc2HCs(self):
		'''Calculates zodiacal Asc to housecusps'''

		raprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.RA]
		declprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.DECL]
		val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
		if math.fabs(val) > 1.0:
			return
		adprom = math.degrees(math.asin(val))

		dsa = 90.0+adprom
		nsa = 90.0-adprom

		self.toHCs(False, primdirs.PrimDir.ASC, raprom, dsa, nsa, chart.Chart.CONJUNCTIO)


	def calcZodMC2HCs(self):
		'''Calculates zodiacal MC to housecusps'''

		raprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.RA]
		declprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.DECL]
		val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
		if math.fabs(val) > 1.0:
			return
		adprom = math.degrees(math.asin(val))

		dsa = 90.0+adprom
		nsa = 90.0-adprom

		self.toHCs(False, primdirs.PrimDir.MC, raprom, dsa, nsa, chart.Chart.CONJUNCTIO)


	def calcZodAsc2LoF(self):
		'''Calculates zodiacal Asc to LoF'''

		lonprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON]
		self.calcZodAscMC2LoF(primdirs.PrimDir.ASC, lonprom)


	def calcZodMC2LoF(self):
		'''Calculates zodiacal MC to LoF'''

		lonprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]
		self.calcZodAscMC2LoF(primdirs.PrimDir.MC, lonprom)


	def calcZodAscMC2LoF(self, p, lonprom):
		SINISTER = 0
		DEXTER = 1

#		for psidx in range(chart.Chart.OPPOSITIO+1):
		for psidx in range(chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO+1):
			if not self.options.pdaspects[psidx]:
				continue

			if not self.options.zodpromsigasps[primdirs.PrimDirs.ASPSPROMSTOSIGS] and psidx > chart.Chart.CONJUNCTIO:
				break

			if self.abort.abort:
				return

			for k in range(DEXTER+1):
				aspect = chart.Chart.Aspects[psidx]
				if k == DEXTER:
					if psidx == chart.Chart.CONJUNCTIO or psidx == chart.Chart.OPPOSITIO:
						break

					aspect *= -1

				lon = util.normalize(lonprom+aspect)
				raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])

				self.toLoF(p, primdirs.PrimDir.NONE, raprom, declprom, psidx)


	def calcZodAsc2Customer2(self):
		'''Calculates zodiacal Asc to Customer2'''

		lonprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON]
		self.calcZodAscMC2Customer2(primdirs.PrimDir.ASC, lonprom)


	def calcZodMC2Customer2(self):
		'''Calculates zodiacal MC to Customer2'''

		lonprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]
		self.calcZodAscMC2Customer2(primdirs.PrimDir.MC, lonprom)


	def calcZodAscMC2Customer2(self, p, lonprom):
		SINISTER = 0
		DEXTER = 1

#		for psidx in range(chart.Chart.OPPOSITIO+1):
		for psidx in range(chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO+1):
			if not self.options.pdaspects[psidx]:
				continue

			if not self.options.zodpromsigasps[primdirs.PrimDirs.ASPSPROMSTOSIGS] and psidx > chart.Chart.CONJUNCTIO:
				break

			if self.abort.abort:
				return

			for k in range(DEXTER+1):
				aspect = chart.Chart.Aspects[psidx]
				if k == DEXTER:
					if psidx == chart.Chart.CONJUNCTIO or psidx == chart.Chart.OPPOSITIO:
						break

					aspect *= -1

				lon = util.normalize(lonprom+aspect)
				raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])

				self.toCustomer2(False, p, primdirs.PrimDir.NONE, raprom, declprom, psidx, aspect)


	def calcZodAsc2Syzygy(self):
		'''Calculates zodiacal Asc to Syzygy'''

		lonprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON]
		self.calcZodAscMC2Syzygy(primdirs.PrimDir.ASC, lonprom)


	def calcZodMC2Syzygy(self):
		'''Calculates zodiacal MC to Syzygy'''

		lonprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]
		self.calcZodAscMC2Syzygy(primdirs.PrimDir.MC, lonprom)


	def calcZodAscMC2Syzygy(self, p, lonprom):
		SINISTER = 0
		DEXTER = 1

#		for psidx in range(chart.Chart.OPPOSITIO+1):
		for psidx in range(chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO+1):
			if not self.options.pdaspects[psidx]:
				continue

			if not self.options.zodpromsigasps[primdirs.PrimDirs.ASPSPROMSTOSIGS] and psidx > chart.Chart.CONJUNCTIO:
				break

			if self.abort.abort:
				return

			for k in range(DEXTER+1):
				aspect = chart.Chart.Aspects[psidx]
				if k == DEXTER:
					if psidx == chart.Chart.CONJUNCTIO or psidx == chart.Chart.OPPOSITIO:
						break

					aspect *= -1

				lon = util.normalize(lonprom+aspect)
				raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])

				self.toSyzygy(p, primdirs.PrimDir.NONE, raprom, declprom, psidx)


	def calcZodLoF2Planets(self):
		'''Calculates zodiacal LoF to Planets and their aspects'''

		raprom = self.chart.fortune.fortune[fortune.Fortune.RA]
		declprom = self.chart.fortune.fortune[fortune.Fortune.DECL]

		self.toPlanets(False, primdirs.PrimDir.LOF, raprom, declprom)


	def calcZodLoF2Customer2(self):
		'''Calculates zodiacal LoF to Customer2'''

		raprom = self.chart.fortune.fortune[fortune.Fortune.RA]
		declprom = self.chart.fortune.fortune[fortune.Fortune.DECL]

		self.toCustomer2(False, primdirs.PrimDir.LOF, primdirs.PrimDir.NONE, raprom, declprom, chart.Chart.CONJUNCTIO)


	def calcZodPlanets2LoF(self):
		'''Calculates zodiacal Planets and their aspects to LoF'''

		SINISTER = 0
		DEXTER = 1

		NODES = 2

		for p in range(len(self.chart.planets.planets)-NODES):
			if not self.options.promplanets[p]:
				continue

			plprom = self.chart.planets.planets[p]
			pllat = plprom.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LAT]

			for promasp in range(chart.Chart.CONJUNCTIO, chart.Chart.OPPOSITIO+1):
				if not self.options.pdaspects[promasp]:
					continue

				if self.abort.abort:
					return

				for k in range(DEXTER+1):
					aspect = chart.Chart.Aspects[promasp]
					if k == DEXTER:
						if promasp == chart.Chart.CONJUNCTIO or promasp == chart.Chart.OPPOSITIO:
							break

						aspect *= -1

					lonprom = plprom.data[planets.Planet.LONG]+aspect
					lonprom = util.normalize(lonprom)
					raprom, declprom = 0.0, 0.0
					if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
						latprom = 0.0
						if self.options.bianchini:
							val = self.getBianchini(pllat, chart.Chart.Aspects[promasp])
							if math.fabs(val) > 1.0:
								continue
							latprom = math.degrees(math.asin(val))
						else:
							latprom = pllat

						raprom, declprom, dist = astrology.swe_cotrans(lonprom, latprom, 1.0, -self.chart.obl[0])
					else:
						raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

					if self.abort.abort:
						return

					self.toLoF(p, primdirs.PrimDir.NONE, raprom, declprom, promasp, aspect, True)


	def calcZodPlanets2Syzygy(self):
		'''Calculates zodiacal Planets and their aspects to Syzygy'''

		SINISTER = 0
		DEXTER = 1

		NODES = 2

		for p in range(len(self.chart.planets.planets)-NODES):
			if not self.options.promplanets[p]:
				continue

			plprom = self.chart.planets.planets[p]
			pllat = plprom.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LAT]

			for promasp in range(chart.Chart.CONJUNCTIO, chart.Chart.OPPOSITIO+1):
				if not self.options.pdaspects[promasp]:
					continue

				if self.abort.abort:
					return

				for k in range(DEXTER+1):
					aspect = chart.Chart.Aspects[promasp]
					if k == DEXTER:
						if promasp == chart.Chart.CONJUNCTIO or promasp == chart.Chart.OPPOSITIO:
							break

						aspect *= -1

					lonprom = plprom.data[planets.Planet.LONG]+aspect
					lonprom = util.normalize(lonprom)
					raprom, declprom = 0.0, 0.0
					if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
						latprom = 0.0
						if self.options.bianchini:
							val = self.getBianchini(pllat, chart.Chart.Aspects[promasp])
							if math.fabs(val) > 1.0:
								continue
							latprom = math.degrees(math.asin(val))
						else:
							latprom = pllat

						raprom, declprom, dist = astrology.swe_cotrans(lonprom, latprom, 1.0, -self.chart.obl[0])
					else:
						raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

					if self.abort.abort:
						return

					self.toSyzygy(p, primdirs.PrimDir.NONE, raprom, declprom, promasp, aspect, True)


	def calcZodCustomer2LoF(self):
		'''Calculates zodiacal Customer to LoF'''

		lonprom = self.chart.cpd.speculums[primdirs.PrimDirs.PLACSPECULUM][customerpd.CustomerPD.LONG]
		raprom = self.chart.cpd.speculums[primdirs.PrimDirs.PLACSPECULUM][customerpd.CustomerPD.RA]
		declprom = self.chart.cpd.speculums[primdirs.PrimDirs.PLACSPECULUM][customerpd.CustomerPD.DECL]

		if self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
			raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

		self.toLoF(primdirs.PrimDir.CUSTOMERPD, primdirs.PrimDir.NONE, raprom, declprom, chart.Chart.CONJUNCTIO)


	def calcZodCustomer2Syzygy(self):
		'''Calculates zodiacal Customer to Syzygy'''

		lonprom = self.chart.cpd.speculums[primdirs.PrimDirs.PLACSPECULUM][customerpd.CustomerPD.LONG]
		raprom = self.chart.cpd.speculums[primdirs.PrimDirs.PLACSPECULUM][customerpd.CustomerPD.RA]
		declprom = self.chart.cpd.speculums[primdirs.PrimDirs.PLACSPECULUM][customerpd.CustomerPD.DECL]

		if self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
			raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

		self.toSyzygy(primdirs.PrimDir.CUSTOMERPD, primdirs.PrimDir.NONE, raprom, declprom, chart.Chart.CONJUNCTIO)


	def calcZodAntiscia2LoF(self):
		'''Calculates zodiacal Antiscia and their aspects to LoF'''

		self.calcZodAntiscia2LoFSub(self.chart.antiscia.plantiscia, primdirs.PrimDir.ANTISCION)
		self.calcZodAntiscia2LoFSub(self.chart.antiscia.plcontraant, primdirs.PrimDir.CONTRAANT)

		if self.options.pdlof[0]:
			#Antiscia/Contraant of LoF
			ant = self.chart.antiscia.lofant
			ralofant = ant.ra
			decllofant = ant.decl
			self.toLoF(primdirs.PrimDir.ANTISCIONLOF, primdirs.PrimDir.NONE, ralofant, decllofant, chart.Chart.CONJUNCTIO)

			#Contra
			cant = self.chart.antiscia.lofcontraant
			ralofcant = ant.ra
			decllofcant = ant.decl
			self.toLoF(primdirs.PrimDir.ANTISCIONLOF, primdirs.PrimDir.NONE, ralofcant, decllofcant, chart.Chart.CONJUNCTIO)

		#Antiscia of AscMC
		for i in range(2):
			ant = self.chart.antiscia.ascmcant[i]
			raant = ant.ra
			declant = ant.decl

			typ = primdirs.PrimDir.ANTISCIONASC
			if i > 0:
				typ = primdirs.PrimDir.ANTISCIONMC

			self.toLoF(typ, primdirs.PrimDir.NONE, raant, declant, chart.Chart.CONJUNCTIO)

		#Contraantiscia of AscMC
		for i in range(2):
			cant = self.chart.antiscia.ascmccontraant[i]
			racant = ant.ra
			declcant = ant.decl

			typ = primdirs.PrimDir.CONTRAANTASC
			if i > 0:
				typ = primdirs.PrimDir.CONTRAANTMC

			self.toLoF(typ, primdirs.PrimDir.NONE, racant, declcant, chart.Chart.CONJUNCTIO)


	def calcZodAntiscia2LoFSub(self, pls, offs):
		SINISTER = 0
		DEXTER = 1

		for p in range(len(pls)):
			if not self.options.promplanets[p]:
				continue

			plprom = pls[p]
			pllat = plprom.lat

			if self.abort.abort:
				return

			for psidx in range(chart.Chart.OPPOSITIO+1):
				if not self.options.pdaspects[psidx]:
					continue

				if not self.options.zodpromsigasps[primdirs.PrimDirs.ASPSPROMSTOSIGS] and psidx > chart.Chart.CONJUNCTIO:
					continue

				#We don't need the aspects of the nodes
				if p > astrology.SE_PLUTO and psidx > chart.Chart.CONJUNCTIO:
					break

				for k in range(DEXTER+1):
					aspect = chart.Chart.Aspects[psidx]
					if k == DEXTER:
						if psidx == chart.Chart.CONJUNCTIO or psidx == chart.Chart.OPPOSITIO:
							break

						aspect *= -1

					lon = plprom.lon+aspect
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

						raprom, declprom, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
					else:
						raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])

					if self.abort.abort:
						return

					self.toLoF(p+offs, primdirs.PrimDir.NONE, raprom, declprom, psidx)


	def calcZodAntiscia2Syzygy(self):
		'''Calculates zodiacal Antiscia and their aspects to Syzygy'''

		self.calcZodAntiscia2SyzygySub(self.chart.antiscia.plantiscia, primdirs.PrimDir.ANTISCION)
		self.calcZodAntiscia2SyzygySub(self.chart.antiscia.plcontraant, primdirs.PrimDir.CONTRAANT)

		if self.options.pdlof[0]:
			#Antiscia/Contraant of LoF
			ant = self.chart.antiscia.lofant
			ralofant = ant.ra
			decllofant = ant.decl
			self.toSyzygy(primdirs.PrimDir.ANTISCIONLOF, primdirs.PrimDir.NONE, ralofant, decllofant, chart.Chart.CONJUNCTIO)

			#Contra
			cant = self.chart.antiscia.lofcontraant
			ralofcant = ant.ra
			decllofcant = ant.decl
			self.toSyzygy(primdirs.PrimDir.ANTISCIONLOF, primdirs.PrimDir.NONE, ralofcant, decllofcant, chart.Chart.CONJUNCTIO)

		#Antiscia of AscMC
		for i in range(2):
			ant = self.chart.antiscia.ascmcant[i]
			raant = ant.ra
			declant = ant.decl

			typ = primdirs.PrimDir.ANTISCIONASC
			if i > 0:
				typ = primdirs.PrimDir.ANTISCIONMC

			self.toSyzygy(typ, primdirs.PrimDir.NONE, raant, declant, chart.Chart.CONJUNCTIO)

		#Contraantiscia of AscMC
		for i in range(2):
			cant = self.chart.antiscia.ascmccontraant[i]
			racant = ant.ra
			declcant = ant.decl

			typ = primdirs.PrimDir.CONTRAANTASC
			if i > 0:
				typ = primdirs.PrimDir.CONTRAANTMC

			self.toSyzygy(typ, primdirs.PrimDir.NONE, racant, declcant, chart.Chart.CONJUNCTIO)


	def calcZodAntiscia2SyzygySub(self, pls, offs):
		SINISTER = 0
		DEXTER = 1

		for p in range(len(pls)):
			if not self.options.promplanets[p]:
				continue

			plprom = pls[p]
			pllat = plprom.lat

			if self.abort.abort:
				return

			for psidx in range(chart.Chart.OPPOSITIO+1):
				if not self.options.pdaspects[psidx]:
					continue

				if not self.options.zodpromsigasps[primdirs.PrimDirs.ASPSPROMSTOSIGS] and psidx > chart.Chart.CONJUNCTIO:
					continue

				#We don't need the aspects of the nodes
				if p > astrology.SE_PLUTO and psidx > chart.Chart.CONJUNCTIO:
					break

				for k in range(DEXTER+1):
					aspect = chart.Chart.Aspects[psidx]
					if k == DEXTER:
						if psidx == chart.Chart.CONJUNCTIO or psidx == chart.Chart.OPPOSITIO:
							break

						aspect *= -1

					lon = plprom.lon+aspect
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

						raprom, declprom, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
					else:
						raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])

					if self.abort.abort:
						return

					self.toSyzygy(p+offs, primdirs.PrimDir.NONE, raprom, declprom, psidx)


	def calcZodTerms(self):
		'''Calculates zodiacal terms to Planets, LoF, Syzygy and Customer2'''

		num = len(self.options.terms[0])
		subnum = len(self.options.terms[0][0])
		for i in range(num):
			summa = 0
			for j in range(subnum):
				lonprom = i*chart.Chart.SIGN_DEG+summa
				if self.options.ayanamsha != 0:
					lonprom += self.chart.ayanamsha
					lonprom = util.normalize(lonprom)
				raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

				if self.abort.abort:
					return

				#Planets
				for s in range(len(self.chart.planets.planets)):
					if self.options.sigplanets[s]:
						self.toPlanet(False, primdirs.PrimDir.TERM+i, self.options.terms[self.options.selterm][i][j][0], raprom, declprom, chart.Chart.CONJUNCTIO, s, chart.Chart.CONJUNCTIO)

				#LoF
				if self.options.pdlof[1]:
					self.toLoF(primdirs.PrimDir.TERM+i, self.options.terms[self.options.selterm][i][j][0], raprom, declprom, chart.Chart.CONJUNCTIO)

				#Syzygy
				if self.options.pdsyzygy:
					self.toSyzygy(primdirs.PrimDir.TERM+i, self.options.terms[self.options.selterm][i][j][0], raprom, declprom, chart.Chart.CONJUNCTIO)

				#Customer2
				if self.options.pdcustomer2 and self.chart.cpd2 != None:
					self.toCustomer2(False, primdirs.PrimDir.TERM+i, self.options.terms[self.options.selterm][i][j][0], raprom, declprom, chart.Chart.CONJUNCTIO)

				summa += self.options.terms[self.options.selterm][i][j][1]


	def calcZodFixStars2Planets(self):
		'''Calculates zodiacal directions of fixstars to planets'''

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

			for s in range(len(self.chart.planets.planets)):
				if not self.options.sigplanets[s]:
					continue

				if self.abort.abort:
					return

				self.toPlanet(False, i+OFFS, primdirs.PrimDir.NONE, rastar, declstar, chart.Chart.CONJUNCTIO, s, chart.Chart.CONJUNCTIO)


	def calcZodFixStars2Customer2(self):
		'''Calculates zodiacal directions of fixstars to Customer2'''

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

			self.toCustomer2(False, i+OFFS, primdirs.PrimDir.NONE, rastar, declstar, chart.Chart.CONJUNCTIO)


	def calcParallels(self):
		'''Calculates mundo parallels'''

		pass


	def calcAntiscia2Parallels(self):
		'''Calculates antiscia to mundo parallels'''

		pass


	def calcAntiscia2ParallelsSub(self, pls, offs):
		pass


	def calcCustomer2Parallels(self):
		'''Calculates mundo parallels of the Customer Point'''

		pass


	def calcZodParallels(self):
		'''Calculates zodiacal parallels'''

		if self.options.zodpromsigasps[primdirs.PrimDirs.PROMSTOSIGASPS]:
			for p in range(len(self.chart.planets.planets)):
				if not self.options.promplanets[p]:
					continue

				if self.abort.abort:
					return

				plprom = self.chart.planets.planets[p]
				lonprom = plprom.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LONG]

				raprom, declprom = 0.0, 0.0
				if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
					#Bianchini is the same since only conjunctio
					raprom = plprom.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.RA]
					declprom = plprom.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.DECL]
				else:
					raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

				self.toZodParallels(p, raprom, declprom)

			if self.options.pdcustomer and self.chart.cpd != None:
				lonprom = self.chart.cpd.speculums[primdirs.PrimDirs.PLACSPECULUM][customerpd.CustomerPD.LONG]

				raprom, declprom = 0.0, 0.0
				if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
					#Bianchini is the same since only conjunctio
					raprom = self.chart.cpd.speculums[primdirs.PrimDirs.PLACSPECULUM][customerpd.CustomerPD.RA]
					declprom = self.chart.cpd.speculums[primdirs.PrimDirs.PLACSPECULUM][customerpd.CustomerPD.DECL]
				else:
					raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

				self.toZodParallels(primdirs.PrimDir.CUSTOMERPD, raprom, declprom)

		if self.options.zodpromsigasps[primdirs.PrimDirs.ASPSPROMSTOSIGS]:
			NODES = 2

			for p in range(len(self.chart.planets.planets)-NODES):
				if not self.options.promplanets[p]:
					continue

				if self.abort.abort:
					return

				ok = self.chart.zodpars.pars[p].valid
				points = self.chart.zodpars.pars[p].pts

				if not ok:
					continue

				for k in range(len(points)):
					if points[k][0] == -1.0:
						continue

					raprom, declprom, dist = astrology.swe_cotrans(points[k][0], 0.0, 1.0, -self.chart.obl[0])

					for s in range(len(self.chart.planets.planets)):
						if not self.options.sigplanets[s]:
							continue

						if self.abort.abort:
							return

						self.toPlanet(False, p, primdirs.PrimDir.NONE, raprom, declprom, points[k][1], s, chart.Chart.CONJUNCTIO, False)

					if self.options.pdcustomer2 and self.chart.cpd2 != None:
						self.toCustomer2(False, p, primdirs.PrimDir.NONE, raprom, declprom, points[k][1])


	def calcZodAntisciaParallels(self):
		'''Calculates zodiacal parallels(Antiscia)'''

		self.calcZodAntisciaParallelsSub(self.chart.antiscia.plantiscia, self.chart.antzodpars.apars, primdirs.PrimDir.ANTISCION)
		self.calcZodAntisciaParallelsSub(self.chart.antiscia.plcontraant, self.chart.antzodpars.cpars, primdirs.PrimDir.CONTRAANT)


	def calcZodAntisciaParallelsSub(self, pls, pars, offs):
		if self.options.zodpromsigasps[primdirs.PrimDirs.PROMSTOSIGASPS]:
			for p in range(len(pls)):
				if not self.options.promplanets[p]:
					continue

				if self.abort.abort:
					return

				plprom = pls[p]
				lonprom = plprom.lon
				pllat = plprom.lat

				raprom, adprom = 0.0, 0.0
				if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
					#This is only conjunction, so bianchini is the same
					raprom, declprom, dist = astrology.swe_cotrans(lon, pllat, 1.0, -self.chart.obl[0])
				else:
					raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

				self.toZodParallels(p+offs, raprom, declprom)

			if self.options.pdlof[0]:
				ant = self.chart.antiscia.lofant
				ralofant = ant.ra
				decllofant = ant.decl
				self.toZodParallels(primdirs.PrimDir.ANTISCIONLOF, ralofant, decllofant)

				#Contra
				cant = self.chart.antiscia.lofcontraant
				ralofcant = cant.ra
				decllofcant = cant.decl
				self.toZodParallels(primdirs.PrimDir.CONTRAANTLOF, ralofcant, decllofcant)

			#Antiscia of AscMC
			for i in range(2):
				ant = self.chart.antiscia.ascmcant[i]
				raant = ant.ra
				declant = ant.decl

				typ = primdirs.PrimDir.ANTISCIONASC
				if i > 0:
					typ = primdirs.PrimDir.ANTISCIONMC

				self.toZodParallels(typ, raant, declant)

			#Contraantiscia of AscMC
			for i in range(2):
				cant = self.chart.antiscia.ascmccontraant[i]
				racant = cant.ra
				declcant = cant.decl

				typ = primdirs.PrimDir.CONTRAANTASC
				if i > 0:
					typ = primdirs.PrimDir.CONTRAANTMC

				self.toZodParallels(typ, racant, declcant)

		if self.options.zodpromsigasps[primdirs.PrimDirs.ASPSPROMSTOSIGS]:
			NODES = 2
			for p in range(planets.Planets.PLANETS_NUM-NODES):#Nodes are excluded
				if not self.options.promplanets[p]:
					continue

				if self.abort.abort:
					return

				ok = pars[i].valid
				points = pars[i].pts

				if not ok:
					continue

				for k in range(len(points)):
					if points[k][0] == -1.0:
						continue

					raprom, declprom, dist = astrology.swe_cotrans(points[k][0], 0.0, 1.0, -self.chart.obl[0])

					for s in range(len(self.chart.planets.planets)):
						if not self.options.sigplanets[s]:
							continue

						if self.abort.abort:
							return

						self.toPlanet(False, p+offs, primdirs.PrimDir.NONE, raprom, declprom, points[k][1], s, chart.Chart.CONJUNCTIO)


	def calcZodLoF2ZodParallels(self):
		'''Calculates zodiacal LoF to zodiacal parallels'''

		raprom = self.chart.fortune.fortune[fortune.Fortune.RA]
		declprom = self.chart.fortune.fortune[fortune.Fortune.DECL]

		self.toZodParallels(primdirs.PrimDir.LOF, raprom, declprom)


	def calcZodLoF2Syzygy(self):
		'''Calculates zodiacal LoF to Syzygy'''

		raprom = self.chart.fortune.fortune[fortune.Fortune.RA]
		declprom = self.chart.fortune.fortune[fortune.Fortune.DECL]

		self.toSyzygy(primdirs.PrimDir.LOF, primdirs.PrimDir.NONE, raprom, declprom, chart.Chart.CONJUNCTIO)


	def calcZodParallels2LoF(self):
		'''Calculates zodiacal parallels to zodiacal LoF'''

		NODES = 2
		for p in range(len(self.chart.planets.planets)-NODES):
			if not self.options.promplanets[p]:
				continue

			if self.abort.abort:
				return

			ok = self.chart.zodpars.pars[p].valid
			points = self.chart.zodpars.pars[p].pts

			if not ok:
				continue

			for k in range(len(points)):
				if points[k][0] == -1.0:
					continue

				raprom, declprom, dist = astrology.swe_cotrans(points[k][0], 0.0, 1.0, -self.chart.obl[0])

				self.toLoF(p, primdirs.PrimDir.NONE, raprom, declprom, points[k][1])


	def calcZodParallels2Syzygy(self):
		'''Calculates zodiacal parallels to zodiacal Syzygy'''

		NODES = 2
		for p in range(len(self.chart.planets.planets)-NODES):
			if not self.options.promplanets[p]:
				continue

			if self.abort.abort:
				return

			ok = self.chart.zodpars.pars[p].valid
			points = self.chart.zodpars.pars[p].pts

			if not ok:
				continue

			for k in range(len(points)):
				if points[k][0] == -1.0:
					continue

				raprom, declprom, dist = astrology.swe_cotrans(points[k][0], 0.0, 1.0, -self.chart.obl[0])

				self.toSyzygy(p, primdirs.PrimDir.NONE, raprom, declprom, points[k][1])


	def calcZodAntisciaParallels2LoF(self):
		'''Calculates zodiacal parallels to zodiacal LoF'''

		self.calcZodAntisciaParallels2LoFSub(self.chart.antzodpars.apars, primdirs.PrimDir.ANTISCION)
		self.calcZodAntisciaParallels2LoFSub(self.chart.antzodpars.cpars, primdirs.PrimDir.CONTRAANT)


	def calcZodAntisciaParallels2LoFSub(self, pars, offs):
		NODES = 2

		for p in range(planets.Planets.PLANETS_NUM-NODES):#Nodes are excluded
			if not self.options.promplanets[p]:
				continue

			if self.abort.abort:
				return

			ok = pars[i].valid
			points = pars[i].pts

			if not ok:
				continue

			for k in range(len(points)):
				if points[k][0] == -1.0:
					continue

				raprom, declprom, dist = astrology.swe_cotrans(points[k][0], 0.0, 1.0, -self.chart.obl[0])

				self.toLoF(p+offs, primdirs.PrimDir.NONE, raprom, declprom, points[k][1])


	def calcZodMidPoints(self):
		'''Calclucates zodiacal midpoint directions'''

		mids = self.chart.midpoints.mids
		if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
			mids = self.chart.midpoints.midslat

		#promissors
		for mid in mids:
			if not self.options.promplanets[mid.p1] or not self.options.promplanets[mid.p2]:
				continue		

			if self.abort.abort:
				return

			#significators
			for s in range(len(self.chart.planets.planets)):
				if not self.options.sigplanets[s]:
					continue

				if self.abort.abort:
					return

				plsig = self.chart.planets.planets[s]
				lonsig = plsig.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LONG]
				lonmid = mid.m

				#if sig is closer to midpoint+180
				if math.fabs(lonmid-lonsig) > 90.0:
					lonmid += 180.0
					if lonmid >= 360.0:
						lonmid -= 360.0

				raprom, declprom, dist = astrology.swe_cotrans(lonmid, mid.lat, 1.0, -self.chart.obl[0])

				self.toPlanet(False, mid.p1, mid.p2, raprom, declprom, chart.Chart.MIDPOINT, s, chart.Chart.CONJUNCTIO)


	def calcZodMidPoints2LoF(self):
		'''Calclucates zodiacal midpoint directions to LoF'''

		lonsig = self.chart.fortune.fortune[fortune.Fortune.LON]

		mids = self.chart.midpoints.mids
		if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
			mids = self.chart.midpoints.midslat

		#promissors
		for mid in mids:
			if not self.options.promplanets[mid.p1] or not self.options.promplanets[mid.p2]:
				continue		

			lonmid = mid.m

			if self.abort.abort:
				return

			#if sig is closer to midpoint+180
			if math.fabs(lonmid-lonsig) > 90.0:
				lonmid += 180.0
				if lonmid >= 360.0:
					lonmid -= 360.0

			raprom, declprom, dist = astrology.swe_cotrans(lonmid, mid.lat, 1.0, -self.chart.obl[0])

			self.toLoF(mid.p1, mid.p2, raprom, declprom, chart.Chart.MIDPOINT)


	def calcZodMidPoints2Syzygy(self):
		'''Calclucates zodiacal midpoint directions to Syzygy'''

		lonsig = self.chart.syzygy.speculum[syzygy.Syzygy.LON]

		mids = self.chart.midpoints.mids
		if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
			mids = self.chart.midpoints.midslat

		#promissors
		for mid in mids:
			if not self.options.promplanets[mid.p1] or not self.options.promplanets[mid.p2]:
				continue		

			lonmid = mid.m

			if self.abort.abort:
				return

			#if sig is closer to midpoint+180
			if math.fabs(lonmid-lonsig) > 90.0:
				lonmid += 180.0
				if lonmid >= 360.0:
					lonmid -= 360.0

			raprom, declprom, dist = astrology.swe_cotrans(lonmid, mid.lat, 1.0, -self.chart.obl[0])

			self.toSyzygy(mid.p1, mid.p2, raprom, declprom, chart.Chart.MIDPOINT)


	def calcZodMidPoints2Customer2(self):
		'''Calclucates zodiacal midpoint directions to Customer'''

		lonsig = self.chart.cpd2.speculums[primdirs.PrimDirs.PLACSPECULUM][customerpd.CustomerPD.LONG]

		mids = self.chart.midpoints.mids
		if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
			mids = self.chart.midpoints.midslat

		#promissors
		for mid in mids:
			if not self.options.promplanets[mid.p1] or not self.options.promplanets[mid.p2]:
				continue		

			lonmid = mid.m

			if self.abort.abort:
				return

			#if sig is closer to midpoint+180
			if math.fabs(lonmid-lonsig) > 90.0:
				lonmid += 180.0
				if lonmid >= 360.0:
					lonmid -= 360.0

			raprom, declprom, dist = astrology.swe_cotrans(lonmid, mid.lat, 1.0, -self.chart.obl[0])

			self.toCustomer2(False, mid.p1, mid.p2, raprom, declprom, chart.Chart.MIDPOINT)


	def calcZodFixStars2LoF(self):
		'''Calclucates zodiacal Fixstars directions to LoF'''

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

			self.toLoF(i+OFFS, primdirs.PrimDir.NONE, rastar, declstar, chart.Chart.CONJUNCTIO)


	def calcZodFixStars2Syzygy(self):
		'''Calclucates zodiacal Fixstars directions to Syzygy'''

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

			self.toSyzygy(i+OFFS, primdirs.PrimDir.NONE, rastar, declstar, chart.Chart.CONJUNCTIO)


	def calcPlanets2MLoF(self):
		pass


	def calcCustomer2MLoF(self):
		pass


	def calcAntiscia2MLoF(self):
		pass


	def calcAntiscia2MLoFSub(self, pls, offs):
		pass


	def toPlanets(self, mundane, idprom, raprom, declprom):
		'''Calculates the directions of the promissor to the planets and their aspects'''

		for s in range(len(self.chart.planets.planets)):
			if not self.options.sigplanets[s]:
				continue

			if self.abort.abort:
				return

			#exclude AscNode -> DescNode or vice-versa
			if (idprom == astrology.SE_MEAN_NODE and s == astrology.SE_TRUE_NODE) or (idprom == astrology.SE_TRUE_NODE and s == astrology.SE_MEAN_NODE):
				continue

			for sigasp in range(chart.Chart.OPPOSITIO+1):
				if not self.options.pdaspects[sigasp] or (idprom == s and sigasp == chart.Chart.CONJUNCTIO):
					continue

				if not self.options.zodpromsigasps[primdirs.PrimDirs.PROMSTOSIGASPS] and sigasp > chart.Chart.CONJUNCTIO:
					continue

				if self.abort.abort:
					return

				#We don't need the aspects of the nodes
				if s > astrology.SE_PLUTO and sigasp > chart.Chart.CONJUNCTIO:
					break

				self.toPlanet(mundane, idprom, primdirs.PrimDir.NONE, raprom, declprom, chart.Chart.CONJUNCTIO, s, sigasp)


	def toPlanet(self, mundane, idprom, idprom2, raprom, declprom, promasp, sig, sigasp, calcsecmotion=True, paspect=chart.Chart.NONE):
		SINISTER = 0
		DEXTER = 1

		plsig = self.chart.planets.planets[sig]
		latsig = plsig.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LAT]

		aspect = chart.Chart.Aspects[sigasp]

		latchanged = False
		if self.options.subzodiacal == primdirs.PrimDirs.SZSIGNIFICATOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
			if self.options.bianchini:
				val = self.getBianchini(latsig, chart.Chart.Aspects[sigasp])
				if math.fabs(val) > 1.0:
					return	
				latsig = math.degrees(math.asin(val))
				latchanged = True
		else:
			latsig = 0.0
			latchanged = True

		for k in range(DEXTER+1):
			if k == DEXTER:
				if sigasp == chart.Chart.CONJUNCTIO or sigasp == chart.Chart.OPPOSITIO:
					break

				aspect *= -1

			sigeastern = plsig.eastern
			lonsig = plsig.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LONG]
			phisig = plsig.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.POH]
			aodosig = math.fabs(plsig.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.AODO])

			if sigasp > chart.Chart.CONJUNCTIO:
				lonsig += aspect
				lonsig = util.normalize(lonsig)

			if sigasp > chart.Chart.CONJUNCTIO or latchanged: #recalc data
				ok, sigeastern, abovehorizon, phisig, aodosig = self.getData(lonsig, latsig)
				if not ok:
					continue

			val = math.tan(math.radians(declprom))*math.tan(math.radians(phisig))
			if math.fabs(val) > 1.0:
				continue
			adprom = math.degrees(math.asin(val))

			aodo = 0.0
			if sigeastern:
				aodo = raprom-adprom
			else:
				aodo = raprom+adprom
			
			arc = aodo-aodosig
			ok = True
			if idprom == astrology.SE_MOON and idprom2 == primdirs.PrimDir.NONE and self.options.pdsecmotion and calcsecmotion:
				if paspect == chart.Chart.NONE:
					for itera in range(self.options.pdsecmotioniter+1):
						ok, arc = self.calcArcWithSM(mundane, idprom, sig, sigasp, aspect, arc)
						if not ok:
							break
				else:
					for itera in range(self.options.pdsecmotioniter+1):
						ok, arc = self.calcArcWithSM2(idprom, promasp, sig, paspect, arc)
						if not ok:
							break

			if ok:
				self.create(mundane, idprom, idprom2, sig, promasp, sigasp, arc)


	def toLoF(self, idprom, idprom2, raprom, declprom, promasp, aspect = 0.0, calcsecmotion = False):
		lonsig = self.chart.fortune.fortune[fortune.Fortune.LON]

		ok, sigeastern, abovehorizon, phisig, aodosig = self.getData(lonsig, 0.0)
		if not ok:
			return

		val = math.tan(math.radians(declprom))*math.tan(math.radians(phisig))
		if math.fabs(val) > 1.0:
			return
		adprom = math.degrees(math.asin(val))

		aodo = 0.0
		if sigeastern:
			aodo = raprom-adprom
		else:
			aodo = raprom+adprom
			
		arc = aodo-aodosig
		ok = True
		if calcsecmotion and idprom == astrology.SE_MOON and idprom2 == primdirs.PrimDir.NONE and self.options.pdsecmotion:
			for itera in range(self.options.pdsecmotioniter+1):
				ok, arc = self.calcArcWithSMLoF(idprom, promasp, aspect, arc)
				if not ok:
					break

		if ok:
			self.create(False, idprom, idprom2, primdirs.PrimDir.LOF, promasp, chart.Chart.CONJUNCTIO, arc)


	def toCustomer2(self, mundane, idprom, idprom2, raprom, declprom, promasp, aspect = 0.0, calcsecmotion = False):
		lonsig = self.chart.cpd2.speculums[primdirs.PrimDirs.PLACSPECULUM][customerpd.CustomerPD.LONG]
		latsig = self.chart.cpd2.speculums[primdirs.PrimDirs.PLACSPECULUM][customerpd.CustomerPD.LAT]

		if self.options.subzodiacal != primdirs.PrimDirs.SZSIGNIFICATOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
			latsig = 0.0

		ok, sigeastern, abovehorizon, phisig, aodosig = self.getData(lonsig, latsig)
		if not ok:
			return

		val = math.tan(math.radians(declprom))*math.tan(math.radians(phisig))
		if math.fabs(val) > 1.0:
			return
		adprom = math.degrees(math.asin(val))

		aodo = 0.0
		if sigeastern:
			aodo = raprom-adprom
		else:
			aodo = raprom+adprom
			
		arc = aodo-aodosig
		ok = True
		if calcsecmotion and idprom == astrology.SE_MOON and idprom2 == primdirs.PrimDir.NONE and self.options.pdsecmotion:
			for itera in range(self.options.pdsecmotioniter+1):
				ok, arc = self.calcArcWithSMCustomer2(mundane, idprom, promasp, aspect, arc)
				if not ok:
					break

		if ok:
			self.create(False, idprom, idprom2, primdirs.PrimDir.CUSTOMERPD, promasp, chart.Chart.CONJUNCTIO, arc)


	def toSyzygy(self, idprom, idprom2, raprom, declprom, promasp, aspect = 0.0, calcsecmotion = False):
		lonsig = self.chart.syzygy.speculum[syzygy.Syzygy.LON]

		ok, sigeastern, abovehorizon, phisig, aodosig = self.getData(lonsig, 0.0)
		if not ok:
			return

		val = math.tan(math.radians(declprom))*math.tan(math.radians(phisig))
		if math.fabs(val) > 1.0:
			return
		adprom = math.degrees(math.asin(val))

		aodo = 0.0
		if sigeastern:
			aodo = raprom-adprom
		else:
			aodo = raprom+adprom
			
		arc = aodo-aodosig
		ok = True
		if calcsecmotion and idprom == astrology.SE_MOON and idprom2 == primdirs.PrimDir.NONE and self.options.pdsecmotion:
			for itera in range(self.options.pdsecmotioniter+1):
				ok, arc = self.calcArcWithSMSyzygy(idprom, promasp, aspect, arc)
				if not ok:
					break

		if ok:
			self.create(False, idprom, idprom2, primdirs.PrimDir.SYZ, promasp, chart.Chart.CONJUNCTIO, arc)


	def toMundaneLoF(self, idprom, idprom2, raprom, adprom, calcsecmotion=True):
		pass


	def toZodParallels(self, idprom, raprom, declprom):
		'''Calculates directions of the promissor to zodiacal parallels of the planets'''

		NODES = 2

		for s in range(len(self.chart.planets.planets)-NODES):
			if not self.options.sigplanets[s]:
				continue

			if self.abort.abort:
				return

			ok = self.chart.zodpars.pars[s].valid
			points = self.chart.zodpars.pars[s].pts

			if not ok:
				continue

			for k in range(len(points)):
				if points[k][0] == -1.0:
					continue

				if self.abort.abort:
					return

				ok, sigeastern, abovehorizon, phisig, aodosig = self.getData(points[k][0], 0.0)
				if not ok:
					return

				val = math.tan(math.radians(declprom))*math.tan(math.radians(phisig))
				if math.fabs(val) > 1.0:
					continue
				adprom = math.degrees(math.asin(val))

				aodo = 0.0
				if sigeastern:
					aodo = raprom-adprom
				else:
					aodo = raprom+adprom
			
				arc = aodo-aodosig
				self.create(False, idprom, primdirs.PrimDir.NONE, s, chart.Chart.CONJUNCTIO, points[k][1], arc)


	def getData(self, lon, lat):
		ramc = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.RA]
		raic = ramc+180.0
		if raic > 360.0:
			raic -= 360.0

		placelat = self.chart.place.lat

		ra, decl, dist = astrology.swe_cotrans(lon, lat, 1.0, -self.chart.obl[0])

		ok = True

		eastern = True
		if ramc > raic:
			if ra > raic and ra < ramc:
				eastern = False
		else:
			if (ra > raic and ra < 360.0) or (ra < ramc and ra > 0.0):
				eastern = False

		#adlat
		adlat = 0.0
		val = math.tan(math.radians(placelat))*math.tan(math.radians(decl))
		if math.fabs(val) <= 1.0:
			adlat = math.degrees(math.asin(val))
		else:
			ok = False

		#md
		md = math.fabs(ramc-ra)

		if md > 180.0:
			md = 360.0-md
		icd = math.fabs(raic-ra)
		if icd > 180.0:
			icd = 360.0-icd

		#sa (southern hemisphere!?)
		dsa = 90.0+adlat
		nsa = 90.0-adlat

		abovehorizon = True
		if md > dsa:
			abovehorizon = False

		sa = dsa
		if not abovehorizon:
			sa = nsa
			md = icd

		#adphi
		tval = math.fabs(sa)
		adphi = 0.0
		if tval != 0.0:
			adphi = math.fabs(md)*adlat/tval

		#phi
		tval = math.tan(math.radians(decl))
		phi = 0.0
		if tval != 0.0:
			phi = math.degrees(math.atan(math.sin(math.radians(adphi))/tval))

		#ao/do (southern hemisphere!?)
		if eastern:
			ao = ra-adphi
		else:
			ao = ra+adphi

		return ok, eastern, abovehorizon, phi, ao


#####################################Moon's SecMotion
	def calcArcWithSM(self, mundane, idprom, sig, sigasp, aspect, arc):
		sm = secmotion.SecMotion(self.chart.time, self.chart.place, idprom, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
		lonprom = sm.planet.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LONG]
		raprom = sm.planet.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.RA]
		declprom = sm.planet.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.DECL]

		if self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
			raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

		plsig = self.chart.planets.planets[sig]
		sigeastern = plsig.eastern
		lonsig = plsig.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LONG]
		latsig = plsig.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LAT]
		phisig = plsig.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.POH]
		aodosig = math.fabs(plsig.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.AODO])

		latchanged = False
		if self.options.subzodiacal == primdirs.PrimDirs.SZSIGNIFICATOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
			if self.options.bianchini:
				val = self.getBianchini(latsig, chart.Chart.Aspects[sigasp])
				if math.fabs(val) > 1.0:
					return False, 0.0
				latsig = math.degrees(math.asin(val))
				latchanged = True
		else:
			latsig = 0.0
			latchanged = True

		if sigasp > chart.Chart.CONJUNCTIO:
			lonsig += aspect
			lonsig = util.normalize(lonsig)

		if sigasp > chart.Chart.CONJUNCTIO or latchanged: #recalc data
			ok, sigeastern, abovehorizon, phisig, aodosig = self.getData(lonsig, latsig)
			if not ok:
				return False, 0.0

		val = math.tan(math.radians(declprom))*math.tan(math.radians(phisig))
		if math.fabs(val) > 1.0:
			return False, 0.0
		adprom = math.degrees(math.asin(val))

		aodo = 0.0
		if sigeastern:
			aodo = raprom-adprom
		else:
			aodo = raprom+adprom
			
		arc = aodo-aodosig

		return True, arc


	def calcArcWithSM2(self, idprom, psidx, sig, paspect, arc):
		sm = secmotion.SecMotion(self.chart.time, self.chart.place, idprom, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
		lonprom = sm.planet.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LONG]
		pllat = sm.planet.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LAT]
		lon = lonprom+paspect
		lon = util.normalize(lon)

		raprom, declprom = 0.0, 0.0
		if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
			latprom = 0.0
			if self.options.bianchini:
				val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
				if math.fabs(val) > 1.0:
					return False, 0.0
				latprom = math.degrees(math.asin(val))
			else:
				latprom = pllat
			raprom, declprom, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
		else:
			raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])

		plsig = self.chart.planets.planets[sig]
		sigeastern = plsig.eastern
		lonsig = plsig.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LONG]
		latsig = plsig.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LAT]
		phisig = plsig.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.POH]
		aodosig = math.fabs(plsig.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.AODO])

		if self.options.subzodiacal != primdirs.PrimDirs.SZSIGNIFICATOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
			latsig = 0.0
			ok, sigeastern, abovehorizon, phisig, aodosig = self.getData(lonsig, latsig)
			if not ok:
				return False, 0.0

		val = math.tan(math.radians(declprom))*math.tan(math.radians(phisig))
		if math.fabs(val) > 1.0:
			return False, 0.0
		adprom = math.degrees(math.asin(val))

		aodo = 0.0
		if sigeastern:
			aodo = raprom-adprom
		else:
			aodo = raprom+adprom
		
		arc = aodo-aodosig

		return True, arc


	def calcPArcWithSM(self, idprom, idsig, k, arc):#Mundane-Parallel
		pass


	def calcArcWithSMMLoF(self, idprom, sigasp, aspect, arc):
		pass


	def calcArcWithSMLoF(self, idprom, psidx, aspect, arc):
		sm = secmotion.SecMotion(self.chart.time, self.chart.place, idprom, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
		pllon = sm.planet.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LONG]
		pllat = sm.planet.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LAT]

		lon = pllon+aspect
		lon = util.normalize(lon)
		raprom, declprom = 0.0, 0.0
		if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
			latprom = 0.0
			if self.options.bianchini:
				val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
				if math.fabs(val) > 1.0:
					return False, 0.0
				latprom = math.degrees(math.asin(val))
			else:
				latprom = pllat

			raprom, declprom, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
		else:
			raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])

		lonsig = self.chart.fortune.fortune[fortune.Fortune.LON]

		ok, sigeastern, abovehorizon, phisig, aodosig = self.getData(lonsig, 0.0)
		if not ok:
			return False, 0.0

		val = math.tan(math.radians(declprom))*math.tan(math.radians(phisig))
		if math.fabs(val) > 1.0:
			return False, 0.0
		adprom = math.degrees(math.asin(val))

		aodo = 0.0
		if sigeastern:
			aodo = raprom-adprom
		else:
			aodo = raprom+adprom
			
		arc = aodo-aodosig

		return True, arc


	def calcArcWithSMCustomer2(self, mundane, idprom, psidx, aspect, arc):
		sm = secmotion.SecMotion(self.chart.time, self.chart.place, idprom, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
		pllon = sm.planet.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LONG]
		pllat = sm.planet.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LAT]

		lon = pllon+aspect
		lon = util.normalize(lon)
		raprom, declprom = 0.0, 0.0
		if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
			latprom = 0.0
			if self.options.bianchini:
				val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
				if math.fabs(val) > 1.0:
					return False, 0.0
				latprom = math.degrees(math.asin(val))
			else:
				latprom = pllat

			raprom, declprom, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
		else:
			raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])

		lonsig = self.chart.cpd2.speculums[primdirs.PrimDirs.PLACSPECULUM][customerpd.CustomerPD.LONG]
		latsig = self.chart.cpd2.speculums[primdirs.PrimDirs.PLACSPECULUM][customerpd.CustomerPD.LAT]

		if self.options.subzodiacal != primdirs.PrimDirs.SZSIGNIFICATOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
			latsig = 0.0

		ok, sigeastern, abovehorizon, phisig, aodosig = self.getData(lonsig, latsig)
		if not ok:
			return False, 0.0

		val = math.tan(math.radians(declprom))*math.tan(math.radians(phisig))
		if math.fabs(val) > 1.0:
			return False, 0.0
		adprom = math.degrees(math.asin(val))

		aodo = 0.0
		if sigeastern:
			aodo = raprom-adprom
		else:
			aodo = raprom+adprom
			
		arc = aodo-aodosig

		return True, arc


	def calcArcWithSMSyzygy(self, idprom, psidx, aspect, arc):
		sm = secmotion.SecMotion(self.chart.time, self.chart.place, idprom, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
		pllon = sm.planet.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LONG]
		pllat = sm.planet.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.LAT]

		lon = pllon+aspect
		lon = util.normalize(lon)
		raprom, declprom = 0.0, 0.0
		if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
			latprom = 0.0
			if self.options.bianchini:
				val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
				if math.fabs(val) > 1.0:
					return False, 0.0
				latprom = math.degrees(math.asin(val))
			else:
				latprom = pllat

			raprom, declprom, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
		else:
			raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])

		lonsig = self.chart.syzygy.speculum[syzygy.Syzygy.LON]

		ok, sigeastern, abovehorizon, phisig, aodosig = self.getData(lonsig, 0.0)
		if not ok:
			return False, 0.0

		val = math.tan(math.radians(declprom))*math.tan(math.radians(phisig))
		if math.fabs(val) > 1.0:
			return False, 0.0
		adprom = math.degrees(math.asin(val))

		aodo = 0.0
		if sigeastern:
			aodo = raprom-adprom
		else:
			aodo = raprom+adprom
			
		arc = aodo-aodosig

		return True, arc







