import math
import astrology
import houses
import planets
import fortune
import chart
import mtexts
import util


class ArabicParts:
	'''Computes Arabic Parts'''

	NAME = 0
	FORMULA = 1
	DIURNAL = 2
	LONG = 3
	DEGWINNER = 4

	REFASC = 0
	REFHC2 = REFASC+1
	REFHC3 = REFHC2+1
	REFIC = REFHC3+1
	REFHC5 = REFIC+1
	REFHC6 = REFHC5+1
	REFDESC = REFHC6+1
	REFHC8 = REFDESC+1
	REFHC9 = REFHC8+1
	REFMC = REFHC9+1
	REFHC11 = REFMC+1
	REFHC12 = REFHC11+1

	ASC = 0
	HC2 = ASC+1
	HC3 = HC2+1
	IC = HC3+1
	HC5 = IC+1
	HC6 = HC5+1
	DESC = HC6+1
	HC8 = DESC+1
	HC9 = HC8+1
	MC = HC9+1
	HC11 = MC+1
	HC12 = HC11+1
	PLOFFS = HC12+1
	SUN = PLOFFS
	MOON = SUN+1
	MERCURY = MOON+1
	VENUS = MERCURY+1
	MARS = VENUS+1
	JUPITER = MARS+1
	SATURN = JUPITER+1
	LORDOFFS = SATURN+1
	ASCLORD = LORDOFFS
	HC2LORD = ASCLORD+1
	HC3LORD = HC2LORD+1
	ICLORD = HC3LORD+1
	HC5LORD = ICLORD+1
	HC6LORD = HC5LORD+1
	DESCLORD = HC6LORD+1
	HC8LORD = DESCLORD+1
	HC9LORD = HC8LORD+1
	MCLORD = HC9LORD+1
	HC11LORD = MCLORD+1
	HC12LORD = HC11LORD+1
	SPECIAL = HC12LORD+1
	LOF = SPECIAL
	LOFLORD = LOF+1
	SYZ = LOFLORD+1
	SYZLORD = SYZ+1

	HNUM = houses.Houses.HOUSE_NUM-1

	def __init__(self, ar, ascmc, pls, hs, cusps, fort, syz, opts): #ar is from options
		if ar == None:
			self.parts = None
		else:
			self.doms = [4, 3, 2, 1, 0, 2, 3, 4, 5, 6, 6, 5]
			self.exals = [0, 1, -1, 5, -1, -1, 6, -1, -1, 4, -1, 3]
			self.tripls = [0, 3, 1, 2, 0, 3, 1, 2, 0, 3, 1, 2]

			asc = hs.ascmc[houses.Houses.ASC]
			desc = util.normalize(hs.ascmc[houses.Houses.ASC]+180.0)
			mc = hs.ascmc[houses.Houses.MC]
			ic = util.normalize(hs.ascmc[houses.Houses.MC]+180.0)

			cps = (asc, cusps[2], cusps[3], ic, cusps[5], cusps[6], desc, cusps[8], cusps[9], mc, cusps[11], cusps[12])

			self.parts = []
			num = len(ar)
			for i in range(num):
				part = [ar[i][ArabicParts.NAME], (ar[i][ArabicParts.FORMULA][0], ar[i][ArabicParts.FORMULA][1], ar[i][ArabicParts.FORMULA][2]), ar[i][ArabicParts.DIURNAL], 0.0, [[-1,0],[-1,0],[-1,0]]]

				#calc longitude
				#A
				idA = part[ArabicParts.FORMULA][0]
				lonA = 0.0
				if idA < ArabicParts.PLOFFS:
					idA = self.adjustAscendant(idA, opts)
					lonA = cps[idA]
				elif idA < ArabicParts.LORDOFFS:
					lonA = pls.planets[idA-ArabicParts.PLOFFS].data[planets.Planet.LONG]
				elif idA < ArabicParts.SPECIAL:
					idA -= ArabicParts.LORDOFFS
					idA = self.adjustAscendant(idA, opts)
					lonTmp = cps[idA]

					sign = int(lonTmp/chart.Chart.SIGN_DEG)
					lord = -1
					for pid in range(astrology.SE_SATURN+1):
						if opts.dignities[pid][0][sign]:
							lord = pid

					if lord != -1: #lord was found
						lonA = pls.planets[lord].data[planets.Planet.LONG]						
					else:
						continue
				else:
					if idA < ArabicParts.SYZ:
						#recalc LOF if Asc is another housecusp?
						idAsc = self.adjustAscendant(ArabicParts.ASC, opts)
						asclon = cps[idAsc]
						lonA = self.getLoFLon(opts.lotoffortune, asclon, pls, fort.abovehorizon)
#						lonA = fort.fortune[fortune.Fortune.LON]
						if idA == ArabicParts.LOFLORD:
							sign = int(lonA/chart.Chart.SIGN_DEG)
							lord = -1
							for pid in range(astrology.SE_SATURN+1):
								if opts.dignities[pid][0][sign]:
									lord = pid

							if lord != -1: #lord was found
								lonA = pls.planets[lord].data[planets.Planet.LONG]						
							else:
								continue
					else:
						lonA = syz.lon
						if idA == ArabicParts.SYZLORD:
							sign = int(lonA/chart.Chart.SIGN_DEG)
							lord = -1
							for pid in range(astrology.SE_SATURN+1):
								if opts.dignities[pid][0][sign]:
									lord = pid

							if lord != -1: #lord was found
								lonA = pls.planets[lord].data[planets.Planet.LONG]						
							else:
								continue

				#B
				idB = part[ArabicParts.FORMULA][1]
				lonB = 0.0
				if idB < ArabicParts.PLOFFS:
					idB = self.adjustAscendant(idB, opts)
					lonB = cps[idB]
				elif idB < ArabicParts.LORDOFFS:
					lonB = pls.planets[idB-ArabicParts.PLOFFS].data[planets.Planet.LONG]
				elif idB < ArabicParts.SPECIAL:
					idB -= ArabicParts.LORDOFFS
					idB = self.adjustAscendant(idB, opts)
					lonTmp = cps[idB]

					sign = int(lonTmp/chart.Chart.SIGN_DEG)
					lord = -1
					for pid in range(astrology.SE_SATURN+1):
						if opts.dignities[pid][0][sign]:
							lord = pid

					if lord != -1: #lord was found
						lonB = pls.planets[lord].data[planets.Planet.LONG]						
					else:
						continue
				else:
					if idB < ArabicParts.SYZ:
						#recalc LOF if Asc is another housecusp?
						idAsc = self.adjustAscendant(ArabicParts.ASC, opts)
						asclon = cps[idAsc]
						lonB = self.getLoFLon(opts.lotoffortune, asclon, pls, fort.abovehorizon)
#						lonB = fort.fortune[fortune.Fortune.LON]
						if idB == ArabicParts.LOFLORD:
							sign = int(lonB/chart.Chart.SIGN_DEG)
							lord = -1
							for pid in range(astrology.SE_SATURN+1):
								if opts.dignities[pid][0][sign]:
									lord = pid

							if lord != -1: #lord was found
								lonB = pls.planets[lord].data[planets.Planet.LONG]						
							else:
								continue
					else:
						lonB = syz.lon
						if idB == ArabicParts.SYZLORD:
							sign = int(lonB/chart.Chart.SIGN_DEG)
							lord = -1
							for pid in range(astrology.SE_SATURN+1):
								if opts.dignities[pid][0][sign]:
									lord = pid

							if lord != -1: #lord was found
								lonB = pls.planets[lord].data[planets.Planet.LONG]						
							else:
								continue

				#C
				idC = part[ArabicParts.FORMULA][2]
				lonC = 0.0
				if idC < ArabicParts.PLOFFS:
					idC = self.adjustAscendant(idC, opts)
					lonC = cps[idC]
				elif idC < ArabicParts.LORDOFFS:
					lonC = pls.planets[idC-ArabicParts.PLOFFS].data[planets.Planet.LONG]
				elif idC < ArabicParts.SPECIAL:
					idC -= ArabicParts.LORDOFFS
					idC = self.adjustAscendant(idC, opts)
					lonTmp = cps[idC]

					sign = int(lonTmp/chart.Chart.SIGN_DEG)
					lord = -1
					for pid in range(astrology.SE_SATURN+1):
						if opts.dignities[pid][0][sign]:
							lord = pid

					if lord != -1: #lord was found
						lonC = pls.planets[lord].data[planets.Planet.LONG]						
					else:
						continue
				else:
					if idC < ArabicParts.SYZ:
						#recalc LOF if Asc is another housecusp?
						idAsc = self.adjustAscendant(ArabicParts.ASC, opts)
						asclon = cps[idAsc]
						lonC = self.getLoFLon(opts.lotoffortune, asclon, pls, fort.abovehorizon)
#						lonC = fort.fortune[fortune.Fortune.LON]
						if idC == ArabicParts.LOFLORD:
							sign = int(lonC/chart.Chart.SIGN_DEG)
							lord = -1
							for pid in range(astrology.SE_SATURN+1):
								if opts.dignities[pid][0][sign]:
									lord = pid

							if lord != -1: #lord was found
								lonC = pls.planets[lord].data[planets.Planet.LONG]						
							else:
								continue
					else:
						lonC = syz.lon
						if idC == ArabicParts.SYZLORD:
							sign = int(lonC/chart.Chart.SIGN_DEG)
							lord = -1
							for pid in range(astrology.SE_SATURN+1):
								if opts.dignities[pid][0][sign]:
									lord = pid

							if lord != -1: #lord was found
								lonC = pls.planets[lord].data[planets.Planet.LONG]						
							else:
								continue

				if part[ArabicParts.DIURNAL] and not fort.abovehorizon:#pls.planets[astrology.SE_SUN].abovehorizon:
					tmp = lonB
					lonB = lonC
					lonC = tmp

				diff = lonB-lonC
				if diff < 0.0:
					diff += 360.0
				lon = lonA+diff
				if lon > 360.0:
					lon -= 360.0

				part[ArabicParts.LONG] = lon

				tmplon = lon
				degwinner = [[-1,0],[-1,0],[-1,0]]
				for p in range(astrology.SE_SATURN+1):
					score = 0
					scoretxt = ''
					if opts.ayanamsha != 0:
						tmplon = util.normalize(tmplon-opts.ayanamsha)

					s, st, sh = self.getData(opts, p, tmplon, fort.abovehorizon)
					score += s
					scoretxt += st

					if score > degwinner[0][1]:
						degwinner[0][0] = p
						degwinner[0][1] = score
						degwinner[1][0] = -1
						degwinner[2][0] = -1
					elif score == degwinner[0][1]:
						if degwinner[1][0] == -1:
							degwinner[1][0] = p
						else:
							degwinner[2][0] = p


				part[ArabicParts.DEGWINNER] = degwinner

				self.parts.append(part)


	def adjustAscendant(self, Id, opts):
		if opts.arabicpartsref != 0:
			Id += opts.arabicpartsref
			if Id > ArabicParts.HNUM:
				Id -= ArabicParts.HNUM

		return Id


	def getLoFLon(self, typ, asclon, pls, abovehorizon):
		lon = 0.0
		if typ == chart.Chart.LFMOONSUN:
			diff = pls.planets[astrology.SE_MOON].data[planets.Planet.LONG]-pls.planets[astrology.SE_SUN].data[planets.Planet.LONG]
			if diff < 0.0:
				diff += 360.0
			lon = asclon+diff
			if lon > 360.0:
				lon -= 360.0
		elif typ == chart.Chart.LFDSUNMOON:
			diff = 0.0
			if abovehorizon:
				diff = pls.planets[astrology.SE_SUN].data[planets.Planet.LONG]-pls.planets[astrology.SE_MOON].data[planets.Planet.LONG]
			else:
				diff = pls.planets[astrology.SE_MOON].data[planets.Planet.LONG]-pls.planets[astrology.SE_SUN].data[planets.Planet.LONG]

			if diff < 0.0:
				diff += 360.0
			lon = asclon+diff
			if lon > 360.0:
				lon -= 360.0
		elif typ == chart.Chart.LFDMOONSUN:
			diff = 0.0
			if abovehorizon:
				diff = pls.planets[astrology.SE_MOON].data[planets.Planet.LONG]-pls.planets[astrology.SE_SUN].data[planets.Planet.LONG]
			else:
				diff = pls.planets[astrology.SE_SUN].data[planets.Planet.LONG]-pls.planets[astrology.SE_MOON].data[planets.Planet.LONG]

			if diff < 0.0:
				diff += 360.0
			lon = asclon+diff
			if lon > 360.0:
				lon -= 360.0

		return lon


	def getData(self, opts, i, lon, daytime):
		'''i is the index of the planet, and lon is the longitude to check'''

		score = 0
		scoretxt = ''
		share = 0

		sign = int(lon/chart.Chart.SIGN_DEG)
		if i == self.doms[sign]:
			sc = opts.dignityscores[0]
			score += sc
			add = '+'
			if scoretxt == '':
				add = ''
			scoretxt += add+str(sc)
			share += 1
		if self.exals[sign] != -1 and i == self.exals[sign]:
			sc = opts.dignityscores[1]
			score += sc
			add = '+'
			if scoretxt == '':
				add = ''
			scoretxt += add+str(sc)
			share += 1
		if opts.oneruler:
			tr = self.tripls[sign]
			tripl = 0
			if daytime:
				tripl = opts.trips[opts.seltrip][tr][0]
			else:
				tripl = opts.trips[opts.seltrip][tr][1]

			if tripl == i:
				sc = opts.dignityscores[2]
				score += sc
				add = '+'
				if scoretxt == '':
					add = ''
				scoretxt += add+str(sc)
				share += 1
		else:
			tr = self.tripls[sign]
			for k in range(3):#3 is the maximum number of triplicity rulers
				tripl = opts.trips[opts.seltrip][tr][k]

				if tripl != -1 and tripl == i:
					sc = opts.dignityscores[2]
					score += sc 
					add = '+'
					if scoretxt == '':
						add = ''
					scoretxt += add+str(sc)
					share += 1
					break

		pos = lon%chart.Chart.SIGN_DEG

		subnum = len(opts.terms[0][0])
		summa = 0.0
		for t in range(subnum):
			summa += opts.terms[opts.selterm][sign][t][1]#degs
			if summa > pos:
				break

		term = opts.terms[opts.selterm][sign][t][0]#planet
		if term == i:
			sc = opts.dignityscores[3]
			score += sc
			add = '+'
			if scoretxt == '':
				add = ''
			scoretxt += add+str(sc)
			share += 1

		dec = int(pos/10)
		decan = opts.decans[opts.seldecan][sign][dec]
		if decan == i:
			sc = opts.dignityscores[4]
			score += sc
			add = '+'
			if scoretxt == '':
				add = ''
			scoretxt += add+str(sc)
			share += 1

		return score, scoretxt, share


