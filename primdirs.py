# -*- coding: utf-8 -*-

import math
import datetime
import astrology
import houses
import chart
import fortune
import syzygy
import planets
import fixstars
import transits
import secmotion
import customerpd
import mtexts
import util


class AbortPD:
	def __init__(self):
		self.abort = False

	def aborting(self):
		self.abort = True


class PrimDir:
	'''Represents a direction'''

	NONE = -1

	OFFSANGLES = astrology.SE_TRUE_NODE+1

	ASC = OFFSANGLES 
	DESC = ASC+1
	MC = DESC+1
	IC = MC+1

	HC2 = IC+1
	HC3 = HC2+1
	HC5 = HC3+1
	HC6 = HC5+1
	HC8 = HC6+1
	HC9 = HC8+1
	HC11 = HC9+1
	HC12 = HC11+1

	LOF = HC12+1

	SYZ = LOF+1

	CUSTOMERPD = SYZ+1

	ANTISCION = CUSTOMERPD+1
	ANTISCIONLOF = ANTISCION+12+1
	ANTISCIONASC = ANTISCIONLOF+1
	ANTISCIONMC = ANTISCIONASC+1
	CONTRAANT = ANTISCIONMC+1
	CONTRAANTLOF = CONTRAANT+12+1
	CONTRAANTASC = CONTRAANTLOF+1
	CONTRAANTMC = CONTRAANTASC+1

	TERM = CONTRAANTMC+1

	FIXSTAR = TERM+12+1


	def __init__(self):
		self.mundane = True
		self.prom = PrimDir.NONE
		self.prom2 = PrimDir.NONE
		self.sig = PrimDir.NONE
		self.promasp = PrimDir.NONE
		self.sigasp = PrimDir.NONE
		self.arc = 0.0
		self.direct = True
		self.parallelaxis = 0
		self.time = 0.0
		self.age = 0.0


class PrimDirs:
	'''Implements the PDs that are common in all systems (directions to Asc-MC) and also implements the MidPoints and Rapt Parallels'''

	#Primary Directions
	PLACIDIANSEMIARC = 0
	PLACIDIANUNDERTHEPOLE = 1
	REGIOMONTAN = 2
	CAMPANIAN = 3

	#Speculums
	PLACSPECULUM = 0
	REGIOSPECULUM = 1

	MUNDANE = 0
	ZODIACAL = 1
	BOTH = 2

	#subzodiacals
	SZNEITHER = 0
	SZPROMISSOR = 1
	SZSIGNIFICATOR = 2
	SZBOTH = 3

	#zodical options
	ASPSPROMSTOSIGS = 0
	PROMSTOSIGASPS = 1

	#Dynamic Keys
	TRUESOLAREQUATORIALARC = 0
	BIRTHDAYSOLAREQUATORIALARC = 1
	TRUESOLARECLIPTICALARC = 2
	BIRTHDAYSOLARECLIPTICALARC = 3

	#Static Keys
	NAIBOD = 0
	CARDAN = 1
	PTOLEMY = 2
	CUSTOMER = 3


	DEG = 0
	MIN = 1
	SEC = 2
	COEFF = 3
	staticData = ((0, 59, 8, 1.01456164), (0, 59, 12, 1.0135135), (1, 0, 0, 1.0))

	#Directions
	DIRECT = 0
	CONVERSE = 1
	BOTHDC = 2

	#Range
	RANGE25 = 0
	RANGE50 = 1
	RANGE75 = 2
	RANGE100 = 3
	RANGEALL = 4
	RANGEREV = 5

	LIMIT = 100.0
	REVOLUTIO = 360.0

	Ranges = ((0.0, 25.0), (25.0, 50.0), (50.0, 75.0), (75.0, 100.0), (0.0, LIMIT), (0.0, REVOLUTIO))
	LOW = 0
	HIGH = 1


	def __init__(self, chrt, options, pdrange, direction, abort):
		self.chart = chrt
		self.options = options
		self.pdrange = pdrange
		self.direction = direction

		self.abort = abort

		self.pds = []

		self.ramc = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.RA]
		self.raic = self.ramc+180.0
		if self.raic >= 360.0:
			self.raic -= 360.0

		self.aoasc = self.ramc+90.0
		if self.aoasc >= 360.0:
			self.aoasc -= 360.0

		self.dodesc = self.raic+90.0
		if self.dodesc >= 360.0:
			self.dodesc -= 360.0

		self.calc()
#		self.sort()

		self.pds = self.qsort(self.pds)


	def calc(self):
		if self.options.subprimarydir == PrimDirs.MUNDANE:
			self.calcMunPDs()
		if self.options.subprimarydir == PrimDirs.ZODIACAL:
			self.calcZodPDs()
		if self.options.subprimarydir == PrimDirs.BOTH:
			self.calcMunPDs()
			self.calcZodPDs()


	def calcMunPDs(self):
		self.calcAscMC()
		if self.chart.htype == chart.Chart.RADIX and self.options.pdantiscia:
			self.calcAntiscia2AscMC()
			self.calcAntiscia2Planets(True)
		self.calcInterPlanetary(True)
		if self.chart.htype == chart.Chart.RADIX and self.options.pdparallels[0]:
			self.calcParallels()
			if self.options.pdantiscia:
				self.calcAntiscia2Parallels()
			if self.options.pdcustomer and self.chart.cpd != None:
				self.calcCustomer2Parallels()
		if self.options.primarydir == PrimDirs.PLACIDIANSEMIARC and self.options.pdparallels[1]:
			self.calcRaptParallels()
		if self.chart.htype == chart.Chart.RADIX and self.options.pdmidpoints:
			self.calcMidPoints()
		if self.options.sighouses:
			self.calc2HouseCusps(True)
			if self.chart.htype == chart.Chart.RADIX and self.options.pdantiscia:
				self.calcAntiscia2HouseCusps(True)
		if self.options.primarydir == PrimDirs.PLACIDIANSEMIARC and self.options.pdlof[1]:
			self.calcPlanets2MLoF()
			if self.chart.htype == chart.Chart.RADIX and self.options.pdantiscia:
				self.calcAntiscia2MLoF()
		if self.chart.htype == chart.Chart.RADIX and self.options.pdcustomer and self.chart.cpd != None:
			self.calcCustomer2AscMC(True)
			self.calcCustomerPlanetary(True)
			if self.options.primarydir == PrimDirs.PLACIDIANSEMIARC and self.options.pdlof[1]:
				self.calcCustomer2MLoF()
			if self.options.sighouses:
				self.calcCustomer2HouseCusps(True)
		if self.chart.htype == chart.Chart.RADIX and self.options.pdcustomer2 and self.chart.cpd2 != None:
			self.calcPlanetary2Customer2(True)
			if self.options.pdantiscia:
				self.calcAntiscia2Customer2(True)
			if self.options.pdmidpoints:
				self.calcMidPoints2Customer2()


	def calcZodPDs(self):
		self.calcZodAscMC()
		if self.chart.htype == chart.Chart.RADIX and self.options.pdantiscia:
			self.calcZodAntiscia2AscMC()
			self.calcAntiscia2Planets(False)
			if self.options.pdcustomer2 and self.chart.cpd2 != None:
				self.calcAntiscia2Customer2(False)
		self.calcInterPlanetary(False)
		if self.chart.htype == chart.Chart.RADIX and self.options.pdcustomer2 and self.chart.cpd2 != None:
			self.calcPlanetary2Customer2(False)
		if self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS]:
			self.calcZodPromAspsInterPlanetary()
			if self.options.sighouses:
				self.calcZodPromAsps2HCs()#
			if self.chart.htype == chart.Chart.RADIX and self.options.pdcustomer2 and self.chart.cpd2 != None:
				self.calcZodPromAspsInterPlanetary2Customer2()
			if self.chart.htype == chart.Chart.RADIX and self.options.pdantiscia:
				self.calcZodPromAntisciaAspsInterPlanetary()
				if self.options.pdcustomer2 and self.chart.cpd2 != None:
					self.calcZodPromAntisciaAspsInterPlanetary2Customer2()
		if self.options.pdlof[0]:
			self.calcZodLoF2Planets()
			if self.chart.htype == chart.Chart.RADIX and self.options.pdsyzygy:
				self.calcZodLoF2Syzygy()
			if self.chart.htype == chart.Chart.RADIX and self.options.pdcustomer2 and self.chart.cpd2 != None:
				self.calcZodLoF2Customer2()
		if self.options.pdlof[1]:
			self.calcZodPlanets2LoF()
			if self.chart.htype == chart.Chart.RADIX and self.options.pdantiscia:
				self.calcZodAntiscia2LoF()
		if self.chart.htype == chart.Chart.RADIX and self.options.pdsyzygy:
			self.calcZodPlanets2Syzygy()
			if self.options.pdantiscia:
				self.calcZodAntiscia2Syzygy()
		if self.chart.htype == chart.Chart.RADIX and self.options.pdparallels[0]:
			self.calcZodParallels()
			if self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS]:
				self.calcZodParallelsAscMC()
				if self.options.pdlof[1]:
					self.calcZodParallels2LoF()
				if self.options.pdsyzygy:
					self.calcZodParallels2Syzygy()
			if self.options.zodpromsigasps[PrimDirs.PROMSTOSIGASPS]:
				if self.options.pdlof[0]:
					self.calcZodLoF2ZodParallels()
		if self.chart.htype == chart.Chart.RADIX and self.options.pdmidpoints:
			self.calcZodMidPoints()
			self.calcZodMidPointsAscMC()
			if self.options.pdlof[1]:
				self.calcZodMidPoints2LoF()
			if self.options.pdsyzygy:
				self.calcZodMidPoints2Syzygy()
			if self.options.pdcustomer2 and self.chart.cpd2 != None:
				self.calcZodMidPoints2Customer2()
		if self.options.sighouses:
			self.calc2HouseCusps(False)
			if self.options.pdlof[0]:
				self.calcZodLoF2HouseCusps()
			if self.chart.htype == chart.Chart.RADIX and self.options.pdantiscia:
				self.calcAntiscia2HouseCusps(False)
		if self.options.pdterms:
			self.calcZodTerms()
		if self.chart.htype == chart.Chart.RADIX and self.options.pdfixstars:
			self.calcZodFixStars2AscMC()
			self.calcZodFixStars2Planets()
			if self.options.pdlof[1]:
				self.calcZodFixStars2LoF()
			if self.options.pdsyzygy:
				self.calcZodFixStars2Syzygy()
			if self.options.sighouses:
				self.calcZodFixStars2HouseCusps()
			if self.options.pdcustomer2 and self.chart.cpd2 != None:
				self.calcZodFixStars2Customer2()
		if self.chart.htype == chart.Chart.RADIX and self.options.pdcustomer and self.chart.cpd != None:
			self.calcCustomer2AscMC(False)
			self.calcCustomerPlanetary(False)
			if self.options.pdlof[1]:
				self.calcZodCustomer2LoF()
			if self.options.pdsyzygy:
				self.calcZodCustomer2Syzygy()
			if self.options.sighouses:
				self.calcCustomer2HouseCusps(False)
		if self.options.ascmchcsasproms:
#			if self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS] and self.options.sigascmc[0]:
#				self.calcZodAspAsc2Asc()
			if self.options.zodpromsigasps[PrimDirs.PROMSTOSIGASPS]:
				self.calcZodAsc2AspPlanets()
				if self.chart.htype == chart.Chart.RADIX and self.options.pdparallels[0]:
					self.calcZodAsc2ParallelPlanets()
			self.calcZodAsc2Planets()
			if self.options.pdlof[1]:
				self.calcZodAsc2LoF()
			if self.chart.htype == chart.Chart.RADIX and self.options.pdsyzygy:
				self.calcZodAsc2Syzygy()
			if self.chart.htype == chart.Chart.RADIX and self.options.pdcustomer2 and self.chart.cpd2 != None:
				self.calcZodAsc2Customer2()
			if self.options.sighouses:
				self.calcZodAsc2HCs()
			if self.options.sigascmc[1]:
				self.calcZodAsc2MC()
#				if self.chart.htype == chart.Chart.RADIX and self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS] and self.options.pdparallels[0]:
#					self.calcZodParallelAsc2MCAsc()
#			if self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS] and self.options.sigascmc[1]:
#				self.calcZodAspMC2MC()
			if self.options.zodpromsigasps[PrimDirs.PROMSTOSIGASPS]:
				self.calcZodMC2AspPlanets()
				if self.chart.htype == chart.Chart.RADIX and self.options.pdparallels[0]:
					self.calcZodMC2ParallelPlanets()
			self.calcZodMC2Planets()
			if self.options.pdlof[1]:
				self.calcZodMC2LoF()
			if self.chart.htype == chart.Chart.RADIX and self.options.pdsyzygy:
				self.calcZodMC2Syzygy()
			if self.chart.htype == chart.Chart.RADIX and self.options.pdcustomer2 and self.chart.cpd2 != None:
				self.calcZodMC2Customer2()
			if self.options.sighouses:
				self.calcZodMC2HCs()
			if self.options.sigascmc[0]:
				self.calcZodMC2Asc()
#				if self.chart.htype == chart.Chart.RADIX and self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS] and self.options.pdparallels[0]:
#					self.calcZodParallelMC2AscMC()


	def calcAscMC(self):
		'''Calculates mundane directions to Asc-MC (mundane planets to Asc-MC)'''

		for i in range(len(self.chart.planets.planets)):
			if not self.options.promplanets[i]:
				continue

			if self.abort.abort:
				return

			pl = self.chart.planets.planets[i]
			rapl = pl.speculums[PrimDirs.PLACSPECULUM][planets.Planet.RA]
			adlat = pl.speculums[PrimDirs.PLACSPECULUM][planets.Planet.ADLAT]

			self.toAscMC(i, rapl, adlat)


	def calcAntiscia2AscMC(self):
		'''Calculates mundane directions to Asc-MC (mundane antiscia to Asc-MC)'''

		#Antiscia(Planets)
		for i in range(len(self.chart.antiscia.plantiscia)):
			if not self.options.promplanets[i]:
				continue

			if self.abort.abort:
				return

			ant = self.chart.antiscia.plantiscia[i]
			raant = ant.ra

			val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(ant.decl))
			if math.fabs(val) > 1.0:
				continue
			adlat = math.degrees(math.asin(val))

			self.toAscMC(PrimDir.ANTISCION+i, raant, adlat)

		#ContraAntiscia(Planets)
		for i in range(len(self.chart.antiscia.plcontraant)):
			if not self.options.promplanets[i]:
				continue

			if self.abort.abort:
				return

			ant = self.chart.antiscia.plcontraant[i]
			raant = ant.ra

			val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(ant.decl))
			if math.fabs(val) > 1.0:
				continue
			adlat = math.degrees(math.asin(val))

			self.toAscMC(PrimDir.CONTRAANT+i, raant, adlat)


	def toAscMC(self, idp, ra, adlat):
		if not self.options.pdaspects[chart.Chart.CONJUNCTIO]:
			return

		#MC
		if self.options.sigascmc[1]:
			if idp == astrology.SE_MOON and self.options.pdsecmotion:
				for itera in range(self.options.pdsecmotioniter+1):
					ra, adlat = self.calcSM(idp, ra-self.ramc)

			self.create(True, idp, PrimDir.NONE, PrimDir.MC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, ra-self.ramc)

			# to IC
			if idp == astrology.SE_MOON and self.options.pdsecmotion:
				for itera in range(self.options.pdsecmotioniter+1):
					ra, adlat = self.calcSM(idp, ra-self.raic)

			self.create(True, idp, PrimDir.NONE, PrimDir.IC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, ra-self.raic)

		#Asc
		if self.options.sigascmc[0]:
			ao = ra-adlat
			if idp == astrology.SE_MOON and self.options.pdsecmotion:
				for itera in range(self.options.pdsecmotioniter+1):
					ra, adlat = self.calcSM(idp, ao-self.aoasc)
					ao = ra-adlat
			self.create(True, idp, PrimDir.NONE, PrimDir.ASC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, ao-self.aoasc)

			# to DESC
			do = ra+adlat
			if idp == astrology.SE_MOON and self.options.pdsecmotion:
				for itera in range(self.options.pdsecmotioniter+1):
					ra, adlat = self.calcSM(idp, do-self.dodesc)
					do = ra+adlat
			self.create(True, idp, PrimDir.NONE, PrimDir.DESC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, do-self.dodesc)


	def calcCustomer2AscMC(self, mundane):
		lonpl = self.chart.cpd.speculums[PrimDirs.PLACSPECULUM][customerpd.CustomerPD.LONG]
		rapl = self.chart.cpd.speculums[PrimDirs.PLACSPECULUM][customerpd.CustomerPD.RA]
		adlat = self.chart.cpd.speculums[PrimDirs.PLACSPECULUM][customerpd.CustomerPD.ADLAT]
		advalid = True

		if not mundane and self.options.subzodiacal != PrimDirs.SZPROMISSOR and self.options.subzodiacal != PrimDirs.SZBOTH:
			rapl, declpl, dist = astrology.swe_cotrans(lonpl, 0.0, 1.0, -self.chart.obl[0])
			val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declpl))
			if math.fabs(val) <= 1.0:
				adlat = math.degrees(math.asin(val))
			else:
				advalid = False

		#MC
		if self.options.sigascmc[1]:
			self.create(mundane, PrimDir.CUSTOMERPD, PrimDir.NONE, PrimDir.MC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, rapl-self.ramc)

			# to IC
			self.create(mundane, PrimDir.CUSTOMERPD, PrimDir.NONE, PrimDir.IC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, rapl-self.raic)

		#Asc
		if self.options.sigascmc[0] and advalid:
			ao = rapl-adlat
			self.create(mundane, PrimDir.CUSTOMERPD, PrimDir.NONE, PrimDir.ASC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, ao-self.aoasc)

			# to DESC
			do = rapl+adlat
			self.create(mundane, PrimDir.CUSTOMERPD, PrimDir.NONE, PrimDir.DESC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, do-self.dodesc)


	def calcSM(self, idp, arc):
		sm = secmotion.SecMotion(self.chart.time, self.chart.place, idp, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
		ra = sm.planet.speculums[PrimDirs.PLACSPECULUM][planets.Planet.RA]
		adlat = sm.planet.speculums[PrimDirs.PLACSPECULUM][planets.Planet.ADLAT]

		return ra, adlat


	def calcZodAscMC(self):
		'''Calculates zodiacal directions to Asc-MC (zodiacal planets and their aspects to Asc-MC)'''

		SINISTER = 0
		DEXTER = 1

		for i in range(len(self.chart.planets.planets)):
			if not self.options.promplanets[i]:
				continue

			pl = self.chart.planets.planets[i]
			self.toZodAscMC(pl.data[planets.Planet.LONG], pl.data[planets.Planet.LAT], i, 0)

		#LoF
		if self.options.pdlof[0]:
			ralof = self.chart.fortune.fortune[fortune.Fortune.RA]
			decllof = self.chart.fortune.fortune[fortune.Fortune.DECL]
			val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(decllof))

			#MC
			if self.options.sigascmc[1]:
				self.create(False, PrimDir.LOF, PrimDir.NONE, PrimDir.MC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, ralof-self.ramc)
				#IC
				self.create(False, PrimDir.LOF, PrimDir.NONE, PrimDir.IC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, ralof-self.raic)

			if math.fabs(val) <= 1.0:
				adlat = math.degrees(math.asin(val))

				#Asc
				if self.options.sigascmc[0]:
					aolof = ralof-adlat
					self.create(False, PrimDir.LOF, PrimDir.NONE, PrimDir.ASC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, aolof-self.aoasc)
					#Desc
					dolof = ralof+adlat
					self.create(False, PrimDir.LOF, PrimDir.NONE, PrimDir.DESC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, dolof-self.dodesc)

		#Terms
		if self.options.pdterms:
			if self.options.sigascmc[0] or self.options.sigascmc[1]:
				num = len(self.options.terms[0])
				subnum = len(self.options.terms[0][0])
				for i in range(num):
					summa = 0
					for j in range(subnum):
						self.options.terms[self.options.selterm][i][j][0]
						lonterm = i*chart.Chart.SIGN_DEG+summa
						if self.options.ayanamsha != 0:
							lonterm += self.chart.ayanamsha
							lonterm = util.normalize(lonterm)
						raterm, declterm, dist = astrology.swe_cotrans(lonterm, 0.0, 1.0, -self.chart.obl[0])

						val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declterm))
						if math.fabs(val) > 1.0:
							continue
						adlat = math.degrees(math.asin(val))
						#MC
						if self.options.sigascmc[1]:
							self.create(False, PrimDir.TERM+i, self.options.terms[self.options.selterm][i][j][0], PrimDir.MC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, raterm-self.ramc)
							#IC
							self.create(False, PrimDir.TERM+i, self.options.terms[self.options.selterm][i][j][0], PrimDir.IC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, raterm-self.raic)

						#Asc
						if self.options.sigascmc[0]:
							aoterm = raterm-adlat
							self.create(False, PrimDir.TERM+i, self.options.terms[self.options.selterm][i][j][0], PrimDir.ASC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, aoterm-self.aoasc)
							#Desc
							doterm = raterm+adlat
							self.create(False, PrimDir.TERM+i, self.options.terms[self.options.selterm][i][j][0], PrimDir.DESC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, doterm-self.dodesc)

						summa += self.options.terms[self.options.selterm][i][j][1]


	def calcZodAntiscia2AscMC(self):
		'''Calculates zodiacal directions to Asc-MC (zodiacal antiscia/contra and their aspects to Asc-MC)'''

		#Antiscia of the planets
		for i in range(len(self.chart.antiscia.plantiscia)):
			if not self.options.promplanets[i]:
				continue

			ant = self.chart.antiscia.plantiscia[i]
			lonant = ant.lon
			latant = ant.lat
			self.toZodAscMC(lonant, latant, i, PrimDir.ANTISCION)

		#Contraantiscia of the planets
		for i in range(len(self.chart.antiscia.plcontraant)):
			if not self.options.promplanets[i]:
				continue

			cant = self.chart.antiscia.plcontraant[i]
			loncant = cant.lon
			latcant = cant.lon
			self.toZodAscMC(loncant, latcant, i, PrimDir.CONTRAANT)

		#Antiscia/Contraant of LoF
		if self.options.pdlof[0]:
			ant = self.chart.antiscia.lofant
			ralofant = ant.ra
			decllofant = ant.decl

			val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(decllofant))
			if math.fabs(val) <= 1.0:
				adlat = math.degrees(math.asin(val))
				self.toZodAscMCSub(PrimDir.ANTISCIONLOF, ralofant, adlat)

			#Contra
			cant = self.chart.antiscia.lofcontraant
			ralofcant = ant.ra
			decllofcant = ant.decl
			val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(decllofcant))
			if math.fabs(val) <= 1.0:
				adlat = math.degrees(math.asin(val))
				self.toZodAscMCSub(PrimDir.CONTRAANTLOF, ralofcant, adlat)

		#Antiscia of AscMC
		for i in range(2):
			ant = self.chart.antiscia.ascmcant[i]
			raant = ant.ra
			declant = ant.decl

			val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declant))
			if math.fabs(val) > 1.0:
				continue
			adlat = math.degrees(math.asin(val))

			typ = PrimDir.ANTISCIONASC
			if i > 0:
				typ = PrimDir.ANTISCIONMC

			self.toZodAscMCSub(typ, raant, adlat)

		#Contraantiscia of AscMC
		for i in range(2):
			cant = self.chart.antiscia.ascmccontraant[i]
			racant = ant.ra
			declcant = ant.decl

			val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declcant))
			if math.fabs(val) > 1.0:
				continue
			adlat = math.degrees(math.asin(val))

			typ = PrimDir.CONTRAANTASC
			if i > 0:
				typ = PrimDir.CONTRAANTMC

			self.toZodAscMCSub(typ, racant, adlat)


	def toZodAscMCSub(self, i, ra, adlat):
		#MC
		if self.options.sigascmc[1]:
			self.create(False, i, PrimDir.NONE, PrimDir.MC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, ra-self.ramc)
			#IC
			self.create(False, i, PrimDir.NONE, PrimDir.IC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, ra-self.raic)

		#Asc
		if self.options.sigascmc[0]:
			ao = ra-adlat
			self.create(False, i, PrimDir.NONE, PrimDir.ASC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, ao-self.aoasc)
			#Desc
			do = ra+adlat
			self.create(False, i, PrimDir.NONE, PrimDir.DESC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, do-self.dodesc)


	def toZodAscMC(self, pllon, pllat, i, ioffs):
		SINISTER = 0
		DEXTER = 1

		for j in range(chart.Chart.OPPOSITIO+1):
			if not self.options.pdaspects[j]:
				continue

			if not self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS] and j > chart.Chart.CONJUNCTIO:
				continue

			#We don't need the aspects of the nodes
			if i > astrology.SE_PLUTO and j > chart.Chart.CONJUNCTIO:
				break

			if self.abort.abort:
				return

			aspectus = chart.Chart.Aspects[j]
			for k in range(DEXTER+1):
				lon = 0.0
				if k == SINISTER:
					lon = pllon+chart.Chart.Aspects[j]
					if lon >= 360.0:
						lon -= 360.0

					aspectus = chart.Chart.Aspects[j]
				else:
					if j == chart.Chart.CONJUNCTIO or j == chart.Chart.OPPOSITIO:
						continue

					lon = pllon-chart.Chart.Aspects[j]
					if lon < 0.0:
						lon += 360.0

					aspectus = -chart.Chart.Aspects[j]

				rapl = 0.0
				adlat = 0.0
				if self.options.subzodiacal == PrimDirs.SZPROMISSOR or self.options.subzodiacal == PrimDirs.SZBOTH:
					latprom = 0.0
					if self.options.bianchini:
						val = self.getBianchini(pllat, chart.Chart.Aspects[j])
						if math.fabs(val) > 1.0:
							continue
						latprom = math.degrees(math.asin(val))
					else:
						latprom = pllat

					#calc real(wahre)ra and adlat
#					rapl, declpl = util.getRaDecl(lon, latprom, self.chart.obl[0])
					rapl, declpl, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
					val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declpl))
					if math.fabs(val) > 1.0:
						continue
					adlat = math.degrees(math.asin(val))
				else:
					rapl, declpl, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
					val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declpl))
					if math.fabs(val) > 1.0:
						continue
					adlat = math.degrees(math.asin(val))

				#MC
				if self.options.sigascmc[1]:
					ok = True
					if i == astrology.SE_MOON and ioffs == 0 and self.options.pdsecmotion:
						for itera in range(self.options.pdsecmotioniter+1):
							ok, rapl, adlat = self.calcZodSM(i, j, aspectus, rapl-self.ramc)
					
					if ok:
						self.create(False, i+ioffs, PrimDir.NONE, PrimDir.MC, j, chart.Chart.CONJUNCTIO, rapl-self.ramc)
					#IC
					if (not self.options.pdaspects[chart.Chart.OPPOSITIO] or not self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS]) and j == chart.Chart.CONJUNCTIO:
						ok = True
						if i == astrology.SE_MOON and ioffs == 0 and self.options.pdsecmotion:
							for itera in range(self.options.pdsecmotioniter+1):
								ok, rapl, adlat = self.calcZodSM(i, j, aspectus, rapl-self.raic)

						if ok:
							self.create(False, i+ioffs, PrimDir.NONE, PrimDir.IC, j, chart.Chart.CONJUNCTIO, rapl-self.raic)

				#Asc
				if self.options.sigascmc[0]:
					aopl = rapl-adlat
					ok = True
					if i == astrology.SE_MOON and ioffs == 0 and self.options.pdsecmotion:
						for itera in range(self.options.pdsecmotioniter+1):
							ok, rapl, adlat = self.calcZodSM(i, j, aspectus, aopl-self.aoasc)
							aopl = rapl-adlat

					if ok:
						self.create(False, i+ioffs, PrimDir.NONE, PrimDir.ASC, j, chart.Chart.CONJUNCTIO, aopl-self.aoasc)

					#Desc
					if (not self.options.pdaspects[chart.Chart.OPPOSITIO] or not self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS]) and j == chart.Chart.CONJUNCTIO:
						dopl = rapl+adlat
						ok = True
						if i == astrology.SE_MOON and ioffs == 0 and self.options.pdsecmotion:
							for itera in range(self.options.pdsecmotioniter+1):
								ok, rapl, adlat = self.calcZodSM(i, j, aspectus, dopl-self.dodesc)
								dopl = rapl+adlat

						if ok:
							self.create(False, i+ioffs, PrimDir.NONE, PrimDir.DESC, j, chart.Chart.CONJUNCTIO, dopl-self.dodesc)


	def calcZodSM(self, idp, j, aspect, arc):
		sm = secmotion.SecMotion(self.chart.time, self.chart.place, idp, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
		pllon = sm.planet.speculums[PrimDirs.PLACSPECULUM][planets.Planet.LONG]
		pllat = sm.planet.speculums[PrimDirs.PLACSPECULUM][planets.Planet.LAT]

		lon = pllon+aspect
		lon = util.normalize(lon)

		rapl = 0.0
		adlat = 0.0
		if self.options.subzodiacal == PrimDirs.SZPROMISSOR or self.options.subzodiacal == PrimDirs.SZBOTH:
			latprom = 0.0
			if self.options.bianchini:
				val = self.getBianchini(pllat, chart.Chart.Aspects[j])
				if math.fabs(val) > 1.0:
					return False, 0.0, 0.0
				latprom = math.degrees(math.asin(val))
			else:
				latprom = pllat

			#calc real(wahre)ra and adlat
#			rapl, declpl = util.getRaDecl(lon, latprom, self.chart.obl[0])
			rapl, declpl, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
			val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declpl))
			if math.fabs(val) > 1.0:
				return False, 0.0, 0.0
			adlat = math.degrees(math.asin(val))
		else:
			rapl, declpl, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
			val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declpl))
			if math.fabs(val) > 1.0:
				return False, 0.0, 0.0
			adlat = math.degrees(math.asin(val))

		return True, rapl, adlat


	def calcZodParallelsAscMC(self):
		NODES = 2

		for i in range(len(self.chart.planets.planets)-NODES):
			if not self.options.promplanets[i]:
				continue

			ok = self.chart.zodpars.pars[i].valid
			points = self.chart.zodpars.pars[i].pts

			if not ok:
				continue

			for k in range(len(points)):
				if points[k][0] == -1.0:
					continue

				if self.abort.abort:
					return

				rapl, declpl, dist = astrology.swe_cotrans(points[k][0], 0.0, 1.0, -self.chart.obl[0])
				val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declpl))
				if math.fabs(val) > 1.0:
					continue
				adlat = math.degrees(math.asin(val))

				#MC
				if self.options.sigascmc[1]:
					self.create(False, i, PrimDir.NONE, PrimDir.MC, points[k][1], chart.Chart.CONJUNCTIO, rapl-self.ramc)
					#to IC would be a duplicate: par Mars->MC is contrapar Mars->IC

				#Asc
				if self.options.sigascmc[0]:
					aopl = rapl-adlat
					self.create(False, i, PrimDir.NONE, PrimDir.ASC, points[k][1], chart.Chart.CONJUNCTIO, aopl-self.aoasc)
					#to Desc would be a duplicate


	def calcZodAntisciaParallels2AscMC(self): #not used
		self.calcZodAntisciaParallels2AscMCSub(self.chart.antzodpars.apars, PrimDir.ANTISCION)
		self.calcZodAntisciaParallels2AscMCSub(self.chart.antzodpars.cpars, PrimDir.CONTRAANT)


	def calcZodAntisciaParallels2AscMCSub(self, pars, ioffs):
		NODES = 2

		for i in range(len(pls)-NODES):
			if not self.options.promplanets[i]:
				continue

			ok = pars[i].valid
			points = pars[i].pts

			if not ok:
				continue

			for k in range(len(points)):
				if points[k][0] == -1.0:
					continue

				if self.abort.abort:
					return

				rapl, declpl, dist = astrology.swe_cotrans(points[k][0], 0.0, 1.0, -self.chart.obl[0])

				val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declpl))
				if math.fabs(val) > 1.0:
					continue
				adlat = math.degrees(math.asin(val))

				#MC
				if self.options.sigascmc[1]:
					self.create(False, i+ioffs, PrimDir.NONE, PrimDir.MC, points[k][1], chart.Chart.CONJUNCTIO, rapl-self.ramc)
					#to IC would be a duplicate: par Mars->MC is contrapar Mars->IC

				#Asc
				if self.options.sigascmc[0]:
					aopl = rapl-adlat
					self.create(False, i+ioffs, PrimDir.NONE, PrimDir.ASC, points[k][1], chart.Chart.CONJUNCTIO, aopl-self.aoasc)
					#to Desc would be a duplicate


	def calcZodMidPointsAscMC(self):
		'''Calclucates zodiacal midpoint directions to Asc-MC'''

		mids = self.chart.midpoints.mids
		if self.options.subzodiacal == PrimDirs.SZPROMISSOR or self.options.subzodiacal == PrimDirs.SZBOTH:
			mids = self.chart.midpoints.midslat

		#promissors
		for mid in mids:
			if not self.options.promplanets[mid.p1] or not self.options.promplanets[mid.p2]:
				continue		

			if self.abort.abort:
				return

			raprom, declprom, dist = astrology.swe_cotrans(mid.m, mid.lat, 1.0, -self.chart.obl[0])
			val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
			if math.fabs(val) > 1.0:
				continue
			adprom = math.degrees(math.asin(val))

			#MC
			if self.options.sigascmc[1]:
				self.create(False, mid.p1, mid.p2, PrimDir.MC, chart.Chart.MIDPOINT, chart.Chart.CONJUNCTIO, raprom-self.ramc)
				# to IC
				self.create(False, mid.p1, mid.p2, PrimDir.IC, chart.Chart.MIDPOINT, chart.Chart.CONJUNCTIO, raprom-self.raic)

			#Asc
			if self.options.sigascmc[0]:
				aoprom = raprom-adprom
				self.create(False, mid.p1, mid.p2, PrimDir.ASC, chart.Chart.MIDPOINT, chart.Chart.CONJUNCTIO, aoprom-self.aoasc)
				# to DESC
				doprom = raprom+adprom
				self.create(False, mid.p1, mid.p2, PrimDir.DESC, chart.Chart.MIDPOINT, chart.Chart.CONJUNCTIO, doprom-self.dodesc)


	def calcZodAsc2MC(self):
		lonprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON]

		SINISTER = 0
		DEXTER = 1
		for i in range(chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO+1):#, chart.Chart.OPPOSITIO+1):
			if not self.options.pdaspects[i]:
				continue

			if not self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS] and i > chart.Chart.CONJUNCTIO:
				break

			if self.abort.abort:
				return

			for k in range(DEXTER+1):
				lon = 0.0
				if k == SINISTER:
					lon = util.normalize(lonprom+chart.Chart.Aspects[i])
				else:
					if i == chart.Chart.CONJUNCTIO or i == chart.Chart.OPPOSITIO:
						continue

					lon = util.normalize(lonprom-chart.Chart.Aspects[i])

				ra, decl, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])

				self.create(False, PrimDir.ASC, PrimDir.NONE, PrimDir.MC, i, chart.Chart.CONJUNCTIO, ra-self.ramc)

				if (not self.options.pdaspects[chart.Chart.OPPOSITIO] or not self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS]) and i == chart.Chart.CONJUNCTIO:
					# to IC
					self.create(False, PrimDir.ASC, PrimDir.NONE, PrimDir.IC, i, chart.Chart.CONJUNCTIO, ra-self.raic)


	def calcZodParallelAsc2MCAsc(self):
		lonprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON]
		raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
		ok, points = self.getEclPoints(lonprom, declprom, True)

		if not ok:
			return

		for k in range(len(points)):
			if points[k][0] == -1.0:
				continue

			if self.abort.abort:
				return

			rapl, declpl, dist = astrology.swe_cotrans(points[k][0], 0.0, 1.0, -self.chart.obl[0])

			val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declpl))
			if math.fabs(val) > 1.0:
				continue
			adlat = math.degrees(math.asin(val))

			#MC
			if self.options.sigascmc[1]:
				self.create(False, PrimDir.ASC, PrimDir.NONE, PrimDir.MC, points[k][1], chart.Chart.CONJUNCTIO, rapl-self.ramc)
				#to IC would be a duplicate: par Mars->MC is contrapar Mars->IC

			#Asc
			if self.options.sigascmc[0]:
				aopl = rapl-adlat
				self.create(False, PrimDir.ASC, PrimDir.NONE, PrimDir.ASC, points[k][1], chart.Chart.CONJUNCTIO, aopl-self.aoasc)
				#to Desc would be a duplicate


	def calcZodAspAsc2Asc(self):
		lonprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON]

		SINISTER = 0
		DEXTER = 1
		for i in range(chart.Chart.CONJUNCTIO+1, chart.Chart.OPPOSITIO): #we don't need the opposition
			if not self.options.pdaspects[i]:
				continue

			if self.abort.abort:
				return

			for k in range(DEXTER+1):
				lon = 0.0
				if k == SINISTER:
					lon = util.normalize(lonprom+chart.Chart.Aspects[i])
				else:
					if i == chart.Chart.OPPOSITIO:
						continue

					lon = util.normalize(lonprom-chart.Chart.Aspects[i])

				ra, decl, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
				val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(decl))
				if math.fabs(val) > 1.0:
					continue
				adlat = math.degrees(math.asin(val))
				ao = ra-adlat

				self.create(False, PrimDir.ASC, PrimDir.NONE, PrimDir.ASC, i, chart.Chart.CONJUNCTIO, ao-self.aoasc)
				#Asc->Desc would be over 100


	def calcZodMC2Asc(self):
		lonprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]

		SINISTER = 0
		DEXTER = 1
		for i in range(chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO+1):#, chart.Chart.OPPOSITIO+1):
			if not self.options.pdaspects[i]:
				continue

			if not self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS] and i > chart.Chart.CONJUNCTIO:
				continue

			if self.abort.abort:
				return

			for k in range(DEXTER+1):
				lon = 0.0
				if k == SINISTER:
					lon = util.normalize(lonprom+chart.Chart.Aspects[i])
				else:
					if i == chart.Chart.CONJUNCTIO or i == chart.Chart.OPPOSITIO:
						continue

					lon = util.normalize(lonprom-chart.Chart.Aspects[i])

				ra, decl, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
				val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(decl))
				if math.fabs(val) > 1.0:
					continue
				adlat = math.degrees(math.asin(val))

				aoprom = ra-adlat
				self.create(False, PrimDir.MC, PrimDir.NONE, PrimDir.ASC, i, chart.Chart.CONJUNCTIO, aoprom-self.aoasc)

				if (not self.options.pdaspects[chart.Chart.OPPOSITIO] or not self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS]) and i == chart.Chart.CONJUNCTIO:
					# to DESC
					doprom = ra+adlat
					self.create(False, PrimDir.MC, PrimDir.NONE, PrimDir.DESC, i, chart.Chart.CONJUNCTIO, doprom-self.dodesc)


	def calcZodParallelMC2AscMC(self):
		lonprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]
		raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
		ok, points = self.getEclPoints(lonprom, declprom, True)

		if not ok:
			return

		for k in range(len(points)):
			if points[k][0] == -1.0:
				continue

			if self.abort.abort:
				return

			rapl, declpl, dist = astrology.swe_cotrans(points[k][0], 0.0, 1.0, -self.chart.obl[0])
			val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declpl))
			if math.fabs(val) > 1.0:
				continue
			adlat = math.degrees(math.asin(val))

			#MC
			if self.options.sigascmc[1]:
				self.create(False, PrimDir.MC, PrimDir.NONE, PrimDir.MC, points[k][1], chart.Chart.CONJUNCTIO, rapl-self.ramc)
				#to IC would be a duplicate: par Mars->MC is contrapar Mars->IC

			#Asc
			if self.options.sigascmc[0]:
				aopl = rapl-adlat
				self.create(False, PrimDir.MC, PrimDir.NONE, PrimDir.ASC, points[k][1], chart.Chart.CONJUNCTIO, aopl-self.aoasc)
				#to Desc would be a duplicate


	def calcZodAspMC2MC(self):
		lonprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]

		SINISTER = 0
		DEXTER = 1
		for i in range(chart.Chart.CONJUNCTIO+1, chart.Chart.OPPOSITIO): #we don't need the opposition
			if not self.options.pdaspects[i]:
				continue

			if self.abort.abort:
				return

			for k in range(DEXTER+1):
				lon = 0.0
				if k == SINISTER:
					lon = util.normalize(lonprom+chart.Chart.Aspects[i])
				else:
					if i == chart.Chart.OPPOSITIO:
						continue

					lon = util.normalize(lonprom-chart.Chart.Aspects[i])

				ra, decl, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])

				self.create(False, PrimDir.MC, PrimDir.NONE, PrimDir.MC, i, chart.Chart.CONJUNCTIO, ra-self.ramc)
				#MC->IC would be over 100


	def calcZodFixStars2AscMC(self):
		'''Calculates zodiacal directions of fixstars to Asc-MC'''

		OFFS = PrimDir.FIXSTAR

		for i in range(len(self.chart.fixstars.data)):
			if not self.options.pdfixstarssel[self.chart.fixstars.mixed[i]]:
				continue

			if self.abort.abort:
				return

			star = self.chart.fixstars.data[i]
			lonstar = star[fixstars.FixStars.LON]
			rastar = star[fixstars.FixStars.RA]
			declstar = star[fixstars.FixStars.DECL]

			if self.options.subzodiacal != PrimDirs.SZPROMISSOR and self.options.subzodiacal != PrimDirs.SZBOTH:
				rastar, declstar, dist = astrology.swe_cotrans(lonstar, 0.0, 1.0, -self.chart.obl[0])

			val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declstar))
			advalid = True
			adlat = 0.0
			if math.fabs(val) > 1.0:
				advalid = False
			else:
				adlat = math.degrees(math.asin(val))

			#MC
			if self.options.sigascmc[1]:
				self.create(False, i+OFFS, PrimDir.NONE, PrimDir.MC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, rastar-self.ramc)
				# to IC
				self.create(False, i+OFFS, PrimDir.NONE, PrimDir.IC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, rastar-self.raic)

			#Asc
			if self.options.sigascmc[0] and advalid:
				aostar = rastar-adlat
				self.create(False, i+OFFS, PrimDir.NONE, PrimDir.ASC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, aostar-self.aoasc)

				# to DESC
				dostar = rastar+adlat
				self.create(False, i+OFFS, PrimDir.NONE, PrimDir.DESC, chart.Chart.CONJUNCTIO, chart.Chart.CONJUNCTIO, dostar-self.dodesc)


	def calcMidPoints(self):
		'''Computes mundane midpoints to significators'''

		NODES = 2

		MP = planets.Planet.PMP
		SPECULUM = PrimDirs.PLACSPECULUM
#		if self.options.primarydir == PrimDirs.PLACIDIANUNDERTHEPOLE:
#			MP = planets.Planet.PMP
#			SPECULUM = PrimDirs.PLACSPECULUM
		if self.options.primarydir == PrimDirs.REGIOMONTAN:
			MP = planets.Planet.W
			SPECULUM = PrimDirs.REGIOSPECULUM
		if self.options.primarydir == PrimDirs.CAMPANIAN:
			MP = planets.Planet.CMP
			SPECULUM = PrimDirs.REGIOSPECULUM

		#Promissor1
		for p1 in range(len(self.chart.planets.planets)-NODES):
			if not self.options.promplanets[p1]:
				continue

			plprom1 = self.chart.planets.planets[p1]
			raprom1 = plprom1.speculums[SPECULUM][planets.Planet.RA]
			declprom1 = plprom1.speculums[SPECULUM][planets.Planet.DECL]

			#Promissor2
			for p2 in range(p1+1, len(self.chart.planets.planets)):
				if not self.options.promplanets[p2]:
					continue

				#exclude Midpoints of AscNode,DescNode or vice-versa
				if (p1 == astrology.SE_MEAN_NODE and p2 == astrology.SE_TRUE_NODE) or (p1 == astrology.SE_TRUE_NODE and p2 == astrology.SE_MEAN_NODE):
					continue

				plprom2 = self.chart.planets.planets[p2]
				raprom2 = plprom2.speculums[SPECULUM][planets.Planet.RA]
				declprom2 = plprom2.speculums[SPECULUM][planets.Planet.DECL]

				ramid = util.normalize((raprom1+raprom2)/2.0)

				#Significator
				for s in range(len(self.chart.planets.planets)):
					if not self.options.sigplanets[s]:
						continue

					if self.abort.abort:
						return

					plsig = self.chart.planets.planets[s]

#					print 'p1=%d, p2=%d, s=%d' % (p1, p2, s)#

					rasig = plsig.speculums[SPECULUM][planets.Planet.RA]
					declsig = plsig.speculums[SPECULUM][planets.Planet.DECL]
					mpsig = plsig.speculums[SPECULUM][MP]

					if math.fabs(ramid-rasig) > 90.0:
						ramid += 180.0
						if ramid >= 360.0:
							ramid -= 360.0

					arc = self.getDiff(ramid-rasig)
#					print 'ramid=%f, rasig=%f, arc=%f' % (ramid, rasig, arc)
#					print '********'

					LIM = 30
					x = 0
					good = True
					while x < LIM:
						initarc = arc
						ok, arc = self.iterate(raprom1, declprom1, raprom2, declprom2, mpsig, arc, plsig)
						if not ok:
							good = False
							break
						arc = self.getDiff(arc)#

#						print '%d: initarc=%f, arc=%f' % (x, initarc, arc)
						x += 1
						if math.fabs(math.fabs(arc)-initarc) < 0.001:
							break

						if self.abort.abort:
							return

					if not good:
						continue

					if x == LIM:
						arc = (arc+initarc)/2.0 #Is this OK!?

					self.create(True, p1, p2, s, chart.Chart.MIDPOINT, chart.Chart.CONJUNCTIO, arc)


	def calcMidPoints2Customer2(self):
		'''Computes mundane midpoints to Customer2'''

		NODES = 2

		MP = customerpd.CustomerPD.PMP
		SPECULUM = PrimDirs.PLACSPECULUM
#		if self.options.primarydir == PrimDirs.PLACIDIANUNDERTHEPOLE:
#			MP = customerpd.CustomerPD.Planet.PMP
#			SPECULUM = PrimDirs.PLACSPECULUM
		if self.options.primarydir == PrimDirs.REGIOMONTAN:
			MP = customerpd.CustomerPD.W
			SPECULUM = PrimDirs.REGIOSPECULUM
		if self.options.primarydir == PrimDirs.CAMPANIAN:
			MP = customerpd.CustomerPD.CMP
			SPECULUM = PrimDirs.REGIOSPECULUM

		#Promissor1
		for p1 in range(len(self.chart.planets.planets)-NODES):
			if not self.options.promplanets[p1]:
				continue

			plprom1 = self.chart.planets.planets[p1]
			raprom1 = plprom1.speculums[SPECULUM][planets.Planet.RA]
			declprom1 = plprom1.speculums[SPECULUM][planets.Planet.DECL]

			#Promissor2
			for p2 in range(p1+1, len(self.chart.planets.planets)):
				if not self.options.promplanets[p2]:
					continue

				#exclude Midpoints of AscNode,DescNode or vice-versa
				if (p1 == astrology.SE_MEAN_NODE and p2 == astrology.SE_TRUE_NODE) or (p1 == astrology.SE_TRUE_NODE and p2 == astrology.SE_MEAN_NODE):
					continue

				plprom2 = self.chart.planets.planets[p2]
				raprom2 = plprom2.speculums[SPECULUM][planets.Planet.RA]
				declprom2 = plprom2.speculums[SPECULUM][planets.Planet.DECL]

				ramid = util.normalize((raprom1+raprom2)/2.0)

				if self.abort.abort:
					return

				#Significator
				rasig = self.chart.cpd2.speculums[SPECULUM][customerpd.CustomerPD.RA]
				declsig = self.chart.cpd2.speculums[SPECULUM][customerpd.CustomerPD.DECL]
				mpsig = self.chart.cpd2.speculums[SPECULUM][MP]

				if math.fabs(ramid-rasig) > 90.0:
					ramid += 180.0
					if ramid >= 360.0:
						ramid -= 360.0

				arc = self.getDiff(ramid-rasig)
#				print 'ramid=%f, rasig=%f, arc=%f' % (ramid, rasig, arc)
#				print '********'

				LIM = 30
				x = 0
				good = True
				while x < LIM:
					initarc = arc
					ok, arc = self.iterate(raprom1, declprom1, raprom2, declprom2, mpsig, arc, plprom1)
					if not ok:
						good = False
						break
					arc = self.getDiff(arc)#

#					print '%d: initarc=%f, arc=%f' % (x, initarc, arc)
					x += 1
					if math.fabs(math.fabs(arc)-initarc) < 0.001:
						break

					if self.abort.abort:
						return

				if not good:
					continue

				if x == LIM:
					arc = (arc+initarc)/2.0 #Is this OK!?

				self.create(True, p1, p2, PrimDir.CUSTOMERPD, chart.Chart.MIDPOINT, chart.Chart.CONJUNCTIO, arc)


	def iterate(self, raprom1, declprom1, raprom2, declprom2, mpsig, arc, pl):
		#3.
		raprom1comma = util.normalize(raprom1-arc)
		declprom1comma = declprom1

		raprom2comma = util.normalize(raprom2-arc)
		declprom2comma = declprom2

		ok, mpp1comma = self.calcMP(raprom1comma, declprom1comma, pl)
		if not ok:
			return False, 0.0
		ok, mpp2comma = self.calcMP(raprom2comma, declprom2comma, pl)
		if not ok:
			return False, 0.0

#		print 'mpp1comma=%f, mpp2comma=%f' % (mpp1comma, mpp2comma)

		mppmidcomma = util.normalize((mpp1comma+mpp2comma)/2.0)
#		print 'mppmidcomma=%f' % mppmidcomma

		if math.fabs(mppmidcomma-mpsig) > 90.0:
			mppmidcomma += 180.0
			if mppmidcomma >= 360.0:
				mppmidcomma -= 360.0

#		print 'mppmidcomma checked=%f' % mppmidcomma

#		dmp = util.normalize(mppmidcomma-mpsig)# Regiomontan Midpoints weren't found
		dmp = self.getDiff(mppmidcomma-mpsig)
#		print 'dmp=%f' % dmp

		ok, mpp1 = self.calcMP(raprom1, declprom1, pl)
		if not ok:
			return False, 0.0
#		print 'mpp1=%f' % mpp1
		darc = dmp*self.getDiff(raprom1-raprom1comma)/self.getDiff(mpp1-mpp1comma)

		return True, arc+darc


	def getEclPoints(self, lon, decl, onEcl):
		'''Calculates points of the Ecliptic from declination'''

		PARALLEL = chart.Chart.PARALLEL
		CONTRAPARALLEL = chart.Chart.CONTRAPARALLEL

		origdecl = decl

		if decl < 0.0:
			decl *= -1

		if decl > self.chart.obl[0]:
			return False, ((-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL))

		if onEcl:
			if decl == self.chart.obl[0]:
				lon += 180.0
				lon = util.normalize(lon)
				return True, ((lon, CONTRAPARALLEL), (-1.0, PARALLEL))
			else:
				lon1 = lon+180.0
				lon1 = util.normalize(lon1)
				lon2 = 360.0-lon1
				lon3 = util.normalize(lon2+180.0)
				return True, ((lon1, CONTRAPARALLEL), (lon2, PARALLEL), (lon3, CONTRAPARALLEL))
		else:
			if decl == self.chart.obl[0]:
				val = math.sin(math.radians(origdecl))/math.sin(math.radians(self.chart.obl[0]))
				if math.fabs(val) <= 1.0:
					lon1 = math.degrees(math.asin(val))
					lon1 = util.normalize(lon1)
					lon2 = util.normalize(lon1+180.0)
					return True, ((lon1, PARALLEL), (lon2, CONTRAPARALLEL))
				else:
					return False, ((-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL))
			else:
				val = math.sin(math.radians(origdecl))/math.sin(math.radians(self.chart.obl[0]))
				if math.fabs(val) <= 1.0:
					lon1 = math.degrees(math.asin(val))
					lon1 = util.normalize(lon1)
					lon2 = util.normalize(lon1+180.0)
					lon3 = 360.0-lon2
					lon4 = util.normalize(lon3+180.0)
					return True, ((lon1, PARALLEL), (lon2, CONTRAPARALLEL), (lon3, PARALLEL), (lon4, CONTRAPARALLEL))
				else:
					return False, ((-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL))

		return False, ((-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL))


	def getBianchini(self, lat, asp):
		return math.sin(math.radians(lat))*math.cos(math.radians(asp))


	def create(self, mundane, prom, prom2, sig, promasp, sigasp, arc, parallelaxis = 0):
		'''Creates a direction and pushes it into the list of directions'''

		if self.chart.htype == chart.Chart.RADIX:
			#Just for safety
			if arc <= -360.0:
				arc += 360.0
#				print '<360 prom=%d sig=%d promasp=%d sigasp=%d parallelaxis=%d' % (prom, sig, promasp, sigasp, parallelaxis)
			if arc >= 360.0:
				arc -= 360.0
#				print '>360 prom=%d sig=%d promasp=%d sigasp=%d parallelaxis=%d' % (prom, sig, promasp, sigasp, parallelaxis)

			direct = True
			if arc < 0.0:
				arc *= -1
				direct = False
			if arc > 180.0:
				arc = 360.0-arc 
				direct = not direct

			lim = PrimDirs.LIMIT
		else:
			direct = True
			if arc < 0.0:
				arc *= -1
				direct = False
			if arc > 180.0:
				arc = 360.0-arc 
				direct = not direct

			lim = PrimDirs.REVOLUTIO

			if (arc < lim or arc > -lim) and (self.direction == PrimDirs.DIRECT and direct) or (self.direction == PrimDirs.CONVERSE and not direct):
				time, age = self.calcTimeRev(arc)

				pd = PrimDir()
				pd.mundane = mundane
				pd.prom = prom
				pd.prom2 = prom2
				pd.sig = sig
				pd.promasp = promasp
				pd.sigasp = sigasp
				pd.arc = arc
				pd.direct = direct
				pd.parallelaxis = parallelaxis
				pd.time = time
				pd.age = age

				self.pds.append(pd)

			arc = 360.0-arc 
			direct = not direct

		if (arc >= lim or arc <= -lim) or (self.direction == PrimDirs.DIRECT and not direct) or (self.direction == PrimDirs.CONVERSE and direct):
			return

		if self.chart.htype == chart.Chart.RADIX:
			time, age = self.calcTime(arc, direct)
		else:
			time, age = self.calcTimeRev(arc)

		if self.chart.htype == chart.Chart.RADIX and (age < PrimDirs.Ranges[self.pdrange][PrimDirs.LOW] or age >= PrimDirs.Ranges[self.pdrange][PrimDirs.HIGH]):
			return

		pd = PrimDir()
		pd.mundane = mundane
		pd.prom = prom
		pd.prom2 = prom2
		pd.sig = sig
		pd.promasp = promasp
		pd.sigasp = sigasp
		pd.arc = arc
		pd.direct = direct
		pd.parallelaxis = parallelaxis
		pd.time = time
		pd.age = age

		self.pds.append(pd)


	def calcTime(self, arc, direct):
		'''Calculates time from arc according to the selected key (dynamic or static)'''

		ti = 0.0

		if self.options.pdkeydyn:
			if self.options.pdkeyd == PrimDirs.TRUESOLAREQUATORIALARC or self.options.pdkeyd == PrimDirs.TRUESOLARECLIPTICALARC:
				if not direct and self.options.useregressive:
					ti = self.calcTrueSolarArcRegressive(arc)
				else:
					ti = self.calcTrueSolarArc(arc)
			else:
				ti = self.calcBirthSolarArc(arc)
		else:
			if self.options.pdkeys == PrimDirs.CUSTOMER:
				val = (self.options.pdkeydeg+self.options.pdkeymin/60.0+self.options.pdkeysec/3600.0) 
				if val != 0.0:
					coeff = 1.0/val
					ti = arc*coeff
			else:
				ti = arc*PrimDirs.staticData[self.options.pdkeys][PrimDirs.COEFF]

#		jy, jm, jd, jh = astrology.swe_revjul(self.chart.time.jd+ti, 1)
#		d, m, s = util.decToDeg(jh)
#		print '%d.%2d.%2d %2d:%2d:%2d' % (jy, jm, jd, d, m, s)
		return self.chart.time.jd+ti*365.2421904, ti
#		return util.convDate(self.chart.time.year, self.chart.time.month, self.chart.time.day)+ti, ti


	def calcTrueSolarArc(self, arc):
		LIM = 120.0 #arbitrary value
		y = self.chart.time.year
		m = self.chart.time.month
		d = self.chart.time.day

		h, mi, s = util.decToDeg(self.chart.time.time)
		tt = 0.0

		#Add arc to Suns's pos (long or ra)
		prSunPos = self.chart.planets.planets[astrology.SE_SUN].dataEqu[planets.Planet.RAEQU]
		if self.options.pdkeyd == PrimDirs.TRUESOLARECLIPTICALARC:
			prSunPos = self.chart.planets.planets[astrology.SE_SUN].data[planets.Planet.LONG]

		prSunPosEnd = prSunPos+arc
		transition = False #Pisces-Aries
		if prSunPosEnd >= 360.0:
			transition = True

#		Find day in ephemeris
		while (prSunPos <= prSunPosEnd):
			y, m, d = util.incrDay(y, m, d)
			ti = chart.Time(y, m, d, 0, 0, 0, False, self.chart.time.cal, chart.Time.GREENWICH, True, 0, 0, False, self.chart.place, False)
			sun = planets.Planet(ti.jd, astrology.SE_SUN, astrology.SEFLG_SWIEPH)
			
			pos = sun.dataEqu[planets.Planet.RAEQU]
			if self.options.pdkeyd == PrimDirs.TRUESOLARECLIPTICALARC:
				pos = sun.data[planets.Planet.LONG]

			if transition and pos < LIM:
				pos += 360.0
			prSunPos = pos

			if self.abort.abort:
				return 0.0

		if (prSunPos != prSunPosEnd):
			y, m, d = util.decrDay(y, m, d)

			if transition:
				prSunPosEnd -= 360.0

			trlon = 0.0
			if self.options.pdkeyd == PrimDirs.TRUESOLARECLIPTICALARC:
				trlon = prSunPosEnd
			else:
				#to Longitude...
				trlon = util.ra2ecl(prSunPosEnd, self.chart.obl[0])

			trans = transits.Transits()
			trans.day(y, m, d, self.chart, astrology.SE_SUN, trlon)

			if len(trans.transits) > 0:
				tt = trans.transits[0].time
		else:
			#the time is midnight
			tt = 0.0

		#difference
		d1 = datetime.datetime(self.chart.time.year, self.chart.time.month, self.chart.time.day, h, mi, s) #in GMT
		th, tm, ts = util.decToDeg(tt)
		d2 = datetime.datetime(y, m, d, th, tm, ts) #in GMT
		diff = d2-d1
		ddays = diff.days
		dtime = diff.seconds/3600.0
		#dtime to days
		dtimeindays = dtime/24.0

		tt = ddays+dtimeindays

		return tt


	def calcTrueSolarArcRegressive(self, arc):
		LIM = 120.0 #arbitrary value
		y = self.chart.time.year
		m = self.chart.time.month
		d = self.chart.time.day

		h, mi, s = util.decToDeg(self.chart.time.time)
		tt = 0.0

		#Subtract arc from Suns's pos (long or ra)
		prSunPos = self.chart.planets.planets[astrology.SE_SUN].dataEqu[planets.Planet.RAEQU]
		if self.options.pdkeyd == PrimDirs.TRUESOLARECLIPTICALARC:
			prSunPos = self.chart.planets.planets[astrology.SE_SUN].data[planets.Planet.LONG]

		prSunPosEnd = prSunPos-arc
		transition = False #Pisces-Aries
		if prSunPosEnd < 0.0:
			prSunPos += 360.0
			prSunPosEnd += 360.0
			transition = True

#		Find day in ephemeris
		while (prSunPos >= prSunPosEnd):
			y, m, d = util.decrDay(y, m, d)
			ti = chart.Time(y, m, d, 0, 0, 0, False, self.chart.time.cal, chart.Time.GREENWICH, True, 0, 0, False, self.chart.place, False)
			sun = planets.Planet(ti.jd, astrology.SE_SUN, astrology.SEFLG_SWIEPH)
			
			pos = sun.dataEqu[planets.Planet.RAEQU]
			if self.options.pdkeyd == PrimDirs.TRUESOLARECLIPTICALARC:
				pos = sun.data[planets.Planet.LONG]
			if transition and pos < LIM:
				pos += 360.0
			prSunPos = pos

			if self.abort.abort:
				return 0.0

		if (prSunPos != prSunPosEnd):
			if transition:
				prSunPosEnd -= 360.0

			trlon = 0.0
			if self.options.pdkeyd == PrimDirs.TRUESOLARECLIPTICALARC:
				trlon = prSunPosEnd
			else:
				#to Longitude...
				trlon = util.ra2ecl(prSunPosEnd, self.chart.obl[0])

			trans = transits.Transits()
			trans.day(y, m, d, self.chart, astrology.SE_SUN, trlon)

			if len(trans.transits) > 0:
				tt = trans.transits[0].time
		else:
			#the time is midnight
			tt = 0.0

		#difference
		th, tm, ts = util.decToDeg(tt)
		d1 = datetime.datetime(y, m, d, th, tm, ts) #in GMT
		d2 = datetime.datetime(self.chart.time.year, self.chart.time.month, self.chart.time.day, h, mi, s) #in GMT
		diff = d2-d1
		ddays = diff.days
		dtime = diff.seconds/3600.0
		#dtime to days
		dtimeindays = dtime/24.0

		tt = ddays+dtimeindays

		return tt


	def calcBirthSolarArc(self, arc):
		y = self.chart.time.year
		m = self.chart.time.month
		d = self.chart.time.day

		yn, mn, dn = util.incrDay(y, m, d)

		ti1 = chart.Time(y, m, d, 0, 0, 0, False, self.chart.time.cal, chart.Time.LOCALMEAN, True, 0, 0, False, self.chart.place, False)
		ti2 = chart.Time(yn, mn, dn, 0, 0, 0, False, self.chart.time.cal, chart.Time.LOCALMEAN, True, 0, 0, False, self.chart.place, False)

		sun1 = planets.Planet(ti1.jd, astrology.SE_SUN, astrology.SEFLG_SWIEPH)
		sun2 = planets.Planet(ti2.jd, astrology.SE_SUN, astrology.SEFLG_SWIEPH)

		diff = 0.0
		if self.options.pdkeyd == PrimDirs.BIRTHDAYSOLAREQUATORIALARC:
			diff = sun2.dataEqu[planets.Planet.RAEQU]-sun1.dataEqu[planets.Planet.RAEQU]
		elif self.options.pdkeyd == PrimDirs.BIRTHDAYSOLARECLIPTICALARC:
			diff = sun2.data[planets.Planet.LONG]-sun1.data[planets.Planet.LONG]

		coeff = 0.0
		if diff != 0.0:
			coeff = 1.0/diff

		return arc*coeff


	def calcTimeRev(self, arc):
		'''Calculates time from arc in Revolutions (Solar, Lunar)'''

		if self.chart.htype == chart.Chart.SOLAR:
			ti = arc*PrimDirs.staticData[0][PrimDirs.COEFF]/365.2421904
		else:
			ti = arc*0.0758333/360.0#13.18681376/360.0 # 13.1868.. = 1/(27.3/360.0) coeff

		return self.chart.time.jd+ti*365.2421904, ti
#		return util.convDate(self.chart.time.year, self.chart.time.month, self.chart.time.day)+ti, ti #age won't be correct!!


	def sort(self):
		for j in range(len(self.pds)):
			for i in range(len(self.pds)-1):
				if self.abort.abort:
					return

				if (self.pds[i].time > self.pds[i+1].time):
					tmp = self.pds[i]
					self.pds[i] = self.pds[i+1]
					self.pds[i+1] = tmp


	def qsort(self, L):
		if L == []: return []
		return self.qsort([x for x in L[1:] if x.time < L[0].time]) + L[0:1] + self.qsort([x for x in L[1:] if x.time >= L[0].time])


	def getDiff(self, diff):
		direct = True
		if diff < 0.0:
			diff *= -1
			direct = False
		if diff > 180.0:
			diff = 360.0-diff 
			direct = not direct

		if not direct:
			diff *= -1

		return diff


	def print2file(self, fname):
		bodies = (mtexts.txts['Sun'], mtexts.txts['Moon'], mtexts.txts['Mercury'], mtexts.txts['Venus'], mtexts.txts['Mars'], mtexts.txts['Jupiter'], mtexts.txts['Saturn'], mtexts.txts['Uranus'], mtexts.txts['Neptune'], mtexts.txts['Pluto'], mtexts.txts['AscNode'], mtexts.txts['DescNode'], 'Asc', 'Desc', 'MC', 'IC', 'HC2', 'HC3', 'HC5', 'HC6', 'HC8', 'HC9', 'HC11', 'HC12', mtexts.txts['LoF'], mtexts.txts['Syzygy'], mtexts.txts['Customer2'])
		signs = ['(Aries)', '(Taurus)', '(Gemini)', '(Cancer)', '(Leo)', '(Virgo)', '(Libra)', '(Scorpio)', '(Sagittarius)', '(Capricornus)', '(Aquarius)', '(Pisces)']
		aspects = (mtexts.txts['Conjunctio'], mtexts.txts['Semisextil'], mtexts.txts['Semiquadrat'], mtexts.txts['Sextil'], mtexts.txts['Quintile'], mtexts.txts['Quadrat'], mtexts.txts['Trigon'], mtexts.txts['Sesquiquadrat'], mtexts.txts['Biquintile'], mtexts.txts['Quinqunx'], mtexts.txts['Oppositio'], mtexts.txts['Parallel'], mtexts.txts['Contraparallel'], mtexts.txts['RaptParallel'], mtexts.txts['RaptParallel'], mtexts.txts['MidPoint'])

		pdsystem = (mtexts.txts['PlacidianSemiArc'], mtexts.txts['PlacidianUnderThePole'], mtexts.txts['Regiomontan'], mtexts.txts['Campanian'])
		pdkeysdyn = (mtexts.txts['TrueSolarEquatorialArc'], mtexts.txts['BirthdaySolarEquatorialArc'], mtexts.txts['TrueSolarEclipticalArc'], mtexts.txts['BirthdaySolarEclipticalArc'])
		pdkeysstat = (mtexts.txts['Naibod'], mtexts.txts['Cardan'], mtexts.txts['Ptolemy'], mtexts.txts['Customer'])

		lines = []

		lines.append(pdsystem[self.options.primarydir])
		lines.append('\n')

		if self.options.pdkeydyn:
			lines.append(mtexts.txts['DynamicKey']+':\n')
			lines.append(pdkeysdyn[self.options.pdkeyd]) 
			lines.append('\n')
		else:
			deg = self.options.pdkeydeg
			minu = self.options.pdkeymin
			sec = self.options.pdkeysec
			if self.options.pdkeys != PrimDirs.CUSTOMER:
				deg = PrimDirs.staticData[self.options.pdkeys][PrimDirs.DEG]
				minu = PrimDirs.staticData[self.options.pdkeys][PrimDirs.MIN]
				sec = PrimDirs.staticData[self.options.pdkeys][PrimDirs.SEC]

			lines.append(mtexts.txts['StaticKey']+':\n')
			txt = pdkeysstat[self.options.pdkeys]+' '+str(deg)+mtexts.txts['DegPDList']+' '+str(minu).zfill(2)+mtexts.txts['MinPDList']+' '+str(sec).zfill(2)+mtexts.txts['SecPDList'] 
			lines.append(txt)
			lines.append('\n')

		for pd in self.pds:
			mtxt = mtexts.txts['M']
			if not pd.mundane:
				mtxt = mtexts.txts['Z']

			dirtxt = mtexts.txts['D']
			if not pd.direct:
				dirtxt = mtexts.txts['C']

			y, m, d, h = astrology.swe_revjul(pd.time, 1)
#			y, m, d, extra = util.revConvDate(pd.time)

			#M/Z
			formattxt = '%s '
			tuptxt = [mtxt]

			#promissors
			if pd.promasp == chart.Chart.MIDPOINT or pd.sigasp == chart.Chart.RAPTPAR or pd.sigasp == chart.Chart.RAPTCONTRAPAR: 
				formattxt += '%s %s '
				tuptxt.append(bodies[pd.prom])
				tuptxt.append(bodies[pd.prom2])
			elif pd.prom >= PrimDir.ANTISCION and pd.prom < PrimDir.TERM:
				if pd.promasp != chart.Chart.CONJUNCTIO:
					formattxt += '%s '
					tuptxt.append(aspects[pd.promasp])

				anttxt = mtexts.txts['Antiscion']
				if pd.prom >= PrimDir.CONTRAANT:
					anttxt = mtexts.txts['Contraantiscion']
				formattxt += '%s '
				tuptxt.append(anttxt)

				promtxt = ''
				antoffs = PrimDir.ANTISCION
				if pd.prom >= PrimDir.CONTRAANT:
					antoffs = PrimDir.CONTRAANT
				if pd.prom == PrimDir.ANTISCIONLOF or pd.prom == PrimDir.CONTRAANTLOF:
					promtxt = bodies[pd.prom-antoffs]
				elif pd.prom == PrimDir.ANTISCIONASC or pd.prom == PrimDir.CONTRAANTASC:
					promtxt = mtexts.txts['Asc']
				elif pd.prom == PrimDir.ANTISCIONMC or pd.prom == PrimDir.CONTRAANTMC:
					promtxt = mtexts.txts['MC']
				else:
					promtxt = bodies[pd.prom-antoffs]

				formattxt += '%s '
				tuptxt.append(promtxt)
			elif pd.prom >= PrimDir.TERM and pd.prom < PrimDir.FIXSTAR:
				formattxt += '%s%s '
				tuptxt.append(signs[pd.prom-PrimDir.TERM])
				tuptxt.append(bodies[pd.prom2])
			elif pd.prom >= PrimDir.FIXSTAR:
				formattxt += '%s '
				promtxt = self.chart.fixstars.data[pd.prom-PrimDir.FIXSTAR][fixstars.FixStars.NOMNAME]
				if self.options.usetradfixstarnamespdlist:
					tradname = self.chart.fixstars.data[pd.prom-PrimDir.FIXSTAR][fixstars.FixStars.NAME].strip()
					if tradname != '':
						promtxt = tradname
				tuptxt.append(promtxt)
			elif pd.prom == PrimDir.LOF:
				formattxt += '%s '
				tuptxt.append(bodies[pd.prom])
			elif pd.prom == PrimDir.CUSTOMERPD:
				formattxt += '%s '
				tuptxt.append(bodies[pd.prom])
			elif pd.prom == PrimDir.ASC or pd.prom == PrimDir.MC:
				if pd.promasp != chart.Chart.CONJUNCTIO:
					formattxt += '%s '
					tuptxt.append(aspects[pd.promasp])
				formattxt += '%s '
				atxt = mtexts.txts['Asc']
				if pd.prom == PrimDir.MC:
					atxt = mtexts.txts['MC']
				tuptxt.append(atxt)
			elif pd.prom >= PrimDir.HC2 and pd.prom < PrimDir.LOF:#Sig is HC
				formattxt += '%s '
				HCs = (mtexts.txts['HC2'], mtexts.txts['HC3'], mtexts.txts['HC5'], mtexts.txts['HC6'], mtexts.txts['HC8'], mtexts.txts['HC9'], mtexts.txts['HC11'], mtexts.txts['HC12'])
				htxt = HCs[pd.sig-PrimDir.HC2]
				tuptxt.append(htxt)
			else:
				if pd.promasp != chart.Chart.CONJUNCTIO:
					formattxt += '%s '
					tuptxt.append(aspects[pd.promasp])
				formattxt += '%s '
				tuptxt.append(bodies[pd.prom])

			#D/C
			formattxt += '%s %s '
			tuptxt.append(dirtxt)	
			tuptxt.append('-->')	

			#significators
			if pd.sigasp == chart.Chart.PARALLEL or pd.sigasp == chart.Chart.CONTRAPARALLEL:
				formattxt += '%s %s '
				partxt = mtexts.txts['Parallel']
				if pd.parallelaxis == 0 and pd.sigasp == chart.Chart.CONTRAPARALLEL:
					partxt = mtexts.txts['Contraparallel']
				tuptxt.append(partxt)
				tuptxt.append(bodies[pd.sig])
				if pd.parallelaxis != 0:
					angles = ('('+mtexts.txts['Asc']+')', '('+mtexts.txts['Dsc']+')', '('+mtexts.txts['MC']+')', '('+mtexts.txts['IC']+')')
					formattxt += '%s '
					tuptxt.append(angles[pd.parallelaxis-PrimDir.OFFSANGLES])
			elif pd.sigasp == chart.Chart.RAPTPAR or pd.sigasp == chart.Chart.RAPTCONTRAPAR:
				formattxt += '%s %s '
				tuptxt.append(mtexts.txts['RaptParallel'])
				angles = ('('+mtexts.txts['Asc']+')', '('+mtexts.txts['Dsc']+')', '('+mtexts.txts['MC']+')', '('+mtexts.txts['IC']+')')
				tuptxt.append(angles[pd.parallelaxis-PrimDir.OFFSANGLES])
			elif pd.sig == PrimDir.LOF:
				if pd.mundane:
					if pd.sigasp != chart.Chart.CONJUNCTIO:
						formattxt += '%s '
						tuptxt.append(aspects[pd.sigasp])

				formattxt += '%s '
				tuptxt.append(mtexts.txts['LoF'])
			elif pd.sig == PrimDir.SYZ:
				formattxt += '%s '
				tuptxt.append(bodies[pd.sig])
			elif pd.sig == PrimDir.CUSTOMERPD:
				formattxt += '%s '
				tuptxt.append(mtexts.txts['User2'])
			elif pd.sig >= PrimDir.OFFSANGLES and pd.sig < PrimDir.LOF:#Sig is Asc,MC or HC
				formattxt += '%s '
				stxt = ''
				if pd.sig <= PrimDir.IC:
					angles = (mtexts.txts['Asc'], mtexts.txts['Dsc'], mtexts.txts['MC'], mtexts.txts['IC'])
					stxt = angles[pd.sig-PrimDir.OFFSANGLES]
				else: #=>HC
					HCs = (mtexts.txts['HC2'], mtexts.txts['HC3'], mtexts.txts['HC5'], mtexts.txts['HC6'], mtexts.txts['HC8'], mtexts.txts['HC9'], mtexts.txts['HC11'], mtexts.txts['HC12'])
					stxt = HCs[pd.sig-PrimDir.HC2]
				tuptxt.append(stxt)
			else:
				if pd.sigasp != chart.Chart.CONJUNCTIO:
					formattxt += '%s '
					tuptxt.append(aspects[pd.sigasp])
				formattxt += '%s '
				tuptxt.append(bodies[pd.sig])

			#Arc
			formattxt += '%f '
			tuptxt.append(pd.arc)

			#Date
			formattxt += '%d.%02d.%02d'
			tuptxt.append(y)
			tuptxt.append(m)
			tuptxt.append(d)

			formattxt += '\n'

			lines.append(formattxt % tuple(tuptxt))

		f = open(fname, 'w')
		f.writelines(lines)
		f.close()




