import copy
import astrology
import chart
import houses
import fortune
import arabicparts
import planets
import util


class Essentials:
	'''Calculates essential almuten-scores'''

	def __init__(self, chrt):
		self.chart = chrt

		#(('n1+n2+n3', num), ...) sun, moon, asc, lof, syz
		self.essentials = [] #the seven planets
		self.essentials2 = [] #the seven planets (zodiacalAlmutens from Mercury till Saturn) [in Points table]
		self.essentialsmc = [] #the seven planets [in Points table]
		self.essentialshcs = [] #the seven planets [in Points table]
		self.shares = [0, 0, 0, 0, 0, 0, 0]
		self.maxshare = [-1 ,-1, False]#idofplanet, currmaxshare, dead heat
		self.scores = [0, 0, 0, 0, 0, 0, 0]
		self.maxscore = [-1, -1, False]
		self.degwinner = [[[-1,0],[-1,0],[-1,0]], [[-1,0],[-1,0],[-1,0]], [[-1,0],[-1,0],[-1,0]], [[-1,0],[-1,0],[-1,0]], [[-1,0],[-1,0],[-1,0]]] #[pid,score] #Max three planets
		self.degwinner2 = [[[-1,0],[-1, 0], [-1, 0]], [[-1,0],[-1,0],[-1,0]], [[-1,0],[-1,0],[-1,0]], [[-1,0],[-1,0],[-1,0]], [[-1,0],[-1,0],[-1,0]]] #[pid,score] #Max three planets
		self.degwinnermc = [[-1,0],[-1,0],[-1,0]]
		self.degwinnerhcs = [[[-1,0],[-1,0],[-1,0]], [[-1,0],[-1,0],[-1,0]], [[-1,0],[-1,0],[-1,0]], [[-1,0],[-1,0],[-1,0]], [[-1,0],[-1,0],[-1,0]], [[-1,0],[-1,0],[-1,0]], [[-1,0],[-1,0],[-1,0]], [[-1,0],[-1,0],[-1,0]], [[-1,0],[-1,0],[-1,0]], [[-1,0],[-1,0],[-1,0]], [[-1,0],[-1,0],[-1,0]], [[-1,0],[-1,0],[-1,0]]] 

		self.doms = [4, 3, 2, 1, 0, 2, 3, 4, 5, 6, 6, 5]
		self.exals = [0, 1, -1, 5, -1, 2, 6, -1, -1, 4, -1, 3]
		self.tripls = [0, 3, 1, 2, 0, 3, 1, 2, 0, 3, 1, 2]

		collections = (chrt.planets.planets[astrology.SE_SUN].data[planets.Planet.LONG], chrt.planets.planets[astrology.SE_MOON].data[planets.Planet.LONG], chrt.houses.ascmc[houses.Houses.ASC], chrt.fortune.fortune[fortune.Fortune.LON], chrt.syzygy.lon)

		#check if it is a daytime chart with taking into account the day/night orb
		daytime = chrt.planets.planets[astrology.SE_SUN].abovehorizon
		if chrt.options.usedaynightorb:
			daytime = chrt.fortune.abovehorizon
		
		numcoll = len(collections)
		for i in range(astrology.SE_SATURN+1):
			score = [0, 0, 0, 0, 0]
			scoretxt = ['', '', '', '', '']
			for j in range(numcoll):
				lon = collections[j]
				if chrt.options.ayanamsha != 0:
					lon = util.normalize(lon-chrt.ayanamsha)

				s, st, sh = self.getData(i, lon, daytime)
				score[j] += s
				self.scores[i] += s
				scoretxt[j] += st
				self.shares[i] += sh

				if score[j] > self.degwinner[j][0][1]:
					self.degwinner[j][0][0] = i
					self.degwinner[j][0][1] = score[j]
					self.degwinner[j][1][0] = -1
					self.degwinner[j][2][0] = -1
				elif score[j] == self.degwinner[j][0][1]:
					if self.degwinner[j][1][0] == -1:
						self.degwinner[j][1][0] = i
					else:
						self.degwinner[j][2][0] = i

			self.essentials.append(((scoretxt[0], score[0]), (scoretxt[1], score[1]), (scoretxt[2], score[2]), (scoretxt[3], score[3]), (scoretxt[4], score[4])))

			if self.maxshare[1] == self.shares[i]:
				self.maxshare[2] = True
			elif self.maxshare[1] < self.shares[i]:
				self.maxshare[2] = False
				self.maxshare[0] = i
				self.maxshare[1] = self.shares[i]

			if self.maxscore[1] == self.scores[i]:
				self.maxscore[2] = True
			elif self.maxscore[1] < self.scores[i]:
				self.maxscore[2] = False
				self.maxscore[0] = i
				self.maxscore[1] = self.scores[i]

		#Zodiacal Almutens
		for i in range(astrology.SE_SATURN+1):
			score = [0, 0, 0, 0, 0] #planets from Mercury
			scoretxt = ['', '', '', '', '']
			for j in range(astrology.SE_MERCURY, astrology.SE_SATURN+1):#collections
				lon = self.chart.planets.planets[j].data[planets.Planet.LONG]
				if chrt.options.ayanamsha != 0:
					lon = util.normalize(lon-chrt.ayanamsha)

				s, st, sh = self.getData(i, lon, daytime)
				score[j-astrology.SE_MERCURY] += s
				scoretxt[j-astrology.SE_MERCURY] += st

				if score[j-astrology.SE_MERCURY] > self.degwinner2[j-astrology.SE_MERCURY][0][1]:
					self.degwinner2[j-astrology.SE_MERCURY][0][0] = i
					self.degwinner2[j-astrology.SE_MERCURY][0][1] = score[j-astrology.SE_MERCURY]
					self.degwinner2[j-astrology.SE_MERCURY][1][0] = -1
					self.degwinner2[j-astrology.SE_MERCURY][2][0] = -1
				elif score[j-astrology.SE_MERCURY] == self.degwinner2[j-astrology.SE_MERCURY][0][1]:
					if self.degwinner2[j-astrology.SE_MERCURY][1][0] == -1:
						self.degwinner2[j-astrology.SE_MERCURY][1][0] = i
					else:
						self.degwinner2[j-astrology.SE_MERCURY][2][0] = i

			self.essentials2.append(((scoretxt[0], score[0]), (scoretxt[1], score[1]), (scoretxt[2], score[2]), (scoretxt[3], score[3]), (scoretxt[4], score[4])))

		#MC
		for i in range(astrology.SE_SATURN+1):
			score = 0
			scoretxt = ''
			lon = self.chart.houses.ascmc[houses.Houses.MC]
			if chrt.options.ayanamsha != 0:
				lon = util.normalize(lon-chrt.ayanamsha)

			s, st, sh = self.getData(i, lon, daytime)
			score += s
			scoretxt += st

			if score > self.degwinnermc[0][1]:
				self.degwinnermc[0][0] = i
				self.degwinnermc[0][1] = score
				self.degwinnermc[1][0] = -1
				self.degwinnermc[2][0] = -1
			elif score == self.degwinnermc[0][1]:
				if self.degwinnermc[1][0] == -1:
					self.degwinnermc[1][0] = i
				else:
					self.degwinnermc[2][0] = i

			self.essentialsmc.append((scoretxt, score))

		#housecusps
		for i in range(astrology.SE_SATURN+1):
			score = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			scoretxt = ['', '', '', '', '', '', '', '', '', '', '', '']
			for j in range(houses.Houses.HOUSE_NUM):
				lon = self.chart.houses.cusps[j+1]
				if chrt.options.ayanamsha != 0 and chrt.options.hsys != 'W':
					lon = util.normalize(lon-chrt.ayanamsha)

				s, st, sh = self.getData(i, lon, daytime)
				score[j] += s
				scoretxt[j] += st

				if score[j] > self.degwinnerhcs[j][0][1]:
					self.degwinnerhcs[j][0][0] = i
					self.degwinnerhcs[j][0][1] = score[j]
					self.degwinnerhcs[j][1][0] = -1
					self.degwinnerhcs[j][2][0] = -1
				elif score[j] == self.degwinnerhcs[j][0][1]:
					if self.degwinnerhcs[j][1][0] == -1:
						self.degwinnerhcs[j][1][0] = i
					else:
						self.degwinnerhcs[j][2][0] = i

			self.essentialshcs.append(((scoretxt[0], score[0]), (scoretxt[1], score[1]), (scoretxt[2], score[2]), (scoretxt[3], score[3]), (scoretxt[4], score[4]), (scoretxt[5], score[5]), (scoretxt[6], score[6]), (scoretxt[7], score[7]), (scoretxt[8], score[8]), (scoretxt[9], score[9]), (scoretxt[10], score[10]), (scoretxt[11], score[11])))


	def getData(self, i, lon, daytime):
		'''i is the index of the planet, and lon is the longitude to check'''

		score = 0
		scoretxt = ''
		share = 0

		sign = int(lon/chart.Chart.SIGN_DEG)
		if i == self.doms[sign]:
			sc = self.chart.options.dignityscores[0]
			score += sc
			add = '+'
			if scoretxt == '':
				add = ''
			scoretxt += add+str(sc)
			share += 1
		if self.exals[sign] != -1 and i == self.exals[sign]:
			mercuryinvirgo = sign == 5 and i == 2
			if not mercuryinvirgo or (mercuryinvirgo and self.chart.options.useexaltationmercury):
				sc = self.chart.options.dignityscores[1]
				score += sc
				add = '+'
				if scoretxt == '':
					add = ''
				scoretxt += add+str(sc)
				share += 1
		if self.chart.options.oneruler:
			tr = self.tripls[sign]
			tripl = 0
			if daytime:
				tripl = self.chart.options.trips[self.chart.options.seltrip][tr][0]
			else:
				tripl = self.chart.options.trips[self.chart.options.seltrip][tr][1]

			if tripl == i:
				sc = self.chart.options.dignityscores[2]
				score += sc
				add = '+'
				if scoretxt == '':
					add = ''
				scoretxt += add+str(sc)
				share += 1
		else:
			tr = self.tripls[sign]
			for k in range(3):#3 is the maximum number of triplicity rulers
				tripl = self.chart.options.trips[self.chart.options.seltrip][tr][k]

				if tripl != -1 and tripl == i:
					sc = self.chart.options.dignityscores[2]
					score += sc 
					add = '+'
					if scoretxt == '':
						add = ''
					scoretxt += add+str(sc)
					share += 1
					break

		pos = lon%chart.Chart.SIGN_DEG

		subnum = len(self.chart.options.terms[0][0])
		summa = 0.0
		for t in range(subnum):
			summa += self.chart.options.terms[self.chart.options.selterm][sign][t][1]#degs
			if summa > pos:
				break

		term = self.chart.options.terms[self.chart.options.selterm][sign][t][0]#planet
		if term == i:
			sc = self.chart.options.dignityscores[3]
			score += sc
			add = '+'
			if scoretxt == '':
				add = ''
			scoretxt += add+str(sc)
			share += 1

		dec = int(pos/10)
		decan = self.chart.options.decans[self.chart.options.seldecan][sign][dec]
		if decan == i:
			sc = self.chart.options.dignityscores[4]
			score += sc
			add = '+'
			if scoretxt == '':
				add = ''
			scoretxt += add+str(sc)
			share += 1

		return score, scoretxt, share


class Accidentals:
	'''Calculates accidental almuten-scores'''

	def __init__(self, chrt):
		self.inhouses = [0, 0, 0, 0, 0, 0, 0] #the seven planets
		self.dayruler = [0, 0, 0, 0, 0, 0, 0] #the seven planets
		self.hourruler = [0, 0, 0, 0, 0, 0, 0] #the seven planets
		self.inphases = [0, 0, 0] #mars, jupiter and saturn only
		self.scores = [0, 0, 0, 0, 0, 0, 0] #the seven planets

		for i in range(astrology.SE_SATURN+1):
			pllon = chrt.planets.planets[i].data[planets.Planet.LONG]
			if chrt.options.ayanamsha != 0:
				pllon = util.normalize(pllon-chrt.ayanamsha)
			housenum = chrt.houses.getHousePos(pllon, chrt.options, True)
			self.inhouses[i] += chrt.options.housescores[housenum]

		orbs = (18.0, 30.0, 40.0, 80.0, 100.0, 120.0)
		num = len(orbs)-1
		sunlon = chrt.planets.planets[astrology.SE_SUN].data[planets.Planet.LONG]
		for i in range(astrology.SE_MARS, astrology.SE_SATURN+1):
			pllon = chrt.planets.planets[i].data[planets.Planet.LONG]
			for j in range(num):
				orb = (orbs[j+1]-orbs[j])/2
				asp = orbs[j]+orb
				lon1 = sunlon+orb
				lon2 = sunlon-orb
				if self.inorbsinister(lon1, lon2, pllon, asp):
					if j == 0 or j == num-1:
						self.inphases[i-astrology.SE_MARS] += chrt.options.sunphases[2]	
					elif j == 1 or j == num-2:
						self.inphases[i-astrology.SE_MARS] += chrt.options.sunphases[1]	
					elif j == 2:
						self.inphases[i-astrology.SE_MARS] += chrt.options.sunphases[0]	

		ar = (1, 4, 2, 5, 3, 6, 0)
		self.dayruler[ar[chrt.time.ph.weekday]] += chrt.options.dayhourscores[0]
		self.hourruler[chrt.time.ph.planetaryhour] += chrt.options.dayhourscores[1]

		for i in range(astrology.SE_SATURN+1):
			self.scores[i] += self.inhouses[i]
			self.scores[i] += self.dayruler[i]
			self.scores[i] += self.hourruler[i]

		for i in range(astrology.SE_MARS, astrology.SE_SATURN+1):
			self.scores[i] += self.inphases[i-astrology.SE_MARS]	


	def inorbsinister(self, val1, val2, pos, asp):
		'''Checks if inside orb (Pisces-Aries transition also!), val1 is leftorbboundary, val2 is rightorb boundary'''

		asppoint = pos+asp

		if (val1 >= 360.0 and val2 < 360.0) or (val1 > 0 and val2 < 0):#left is in Aries, right is in Pisces
			if (val1 >= 0 and val2 < 0):
				val1 += 360.0
				val2 += 360.0
			if pos < 20.0: # 20.0 is arbitrary, just to see if the planet is close to the Pisces-Aries transition
				asppoint += 360.0
		else:
			val1 = util.normalize(val1)
			val2 = util.normalize(val2)
			asppoint = util.normalize(asppoint)

		if val1 > asppoint and val2 < asppoint:
			return True

		return False 


class Topicals:
	'''Calculates the Topical Almutens'''

	#Types
	PLANET = 0
	PLANETS = 1
	HOUSECUSP = 2
	ARABICPART = 3
	SYZYGY = 4
	LIGHTOFTHETIME = 5

	#Values(Planets, inHouses, Housecusps, ArabicParts, Syzygy, LightOfTheTime)

	#RulerShips
	SELF = 0
	SIGN = 1
	EXALTATION = 2
	TRIPLICITY1 = 3
	TRIPLICITY2 = 4
	TRIPLICITY3 = 5
	TERM = 6
	DECAN = 7


	def __init__(self, chrt):
		self.chart = chrt

		self.doms = [4, 3, 2, 1, 0, 2, 3, 4, 5, 6, 6, 5]
		self.exals = [0, 1, -1, 5, -1, 2, 6, -1, -1, 4, -1, 3]
		self.tripls = [0, 3, 1, 2, 0, 3, 1, 2, 0, 3, 1, 2]

		#check if it is a daytime chart with taking into account the day/night orb
		daytime = chrt.planets.planets[astrology.SE_SUN].abovehorizon
		if chrt.options.usedaynightorb:
			daytime = chrt.fortune.abovehorizon

		self.names = []
		self.collections = []

		num = len(chrt.options.topicals)
		for i in range(num):
			subnum = len(chrt.options.topicals[i][1])
			lons = []
			for j in range(subnum):
				ok, sublons = self.getLon(chrt, chrt.options.topicals[i][1][j][0], chrt.options.topicals[i][1][j][1], chrt.options.topicals[i][1][j][2], daytime)
				if len(sublons) > 0:
					lons += sublons

			#add (tuple)lons to collections
			if len(lons) > 0:
				self.names.append(chrt.options.topicals[i][0])
				self.collections.append(tuple(lons))

		self.data = [] #numcoll*the seven planets*lon
		self.shares = []#numcoll*thesevenplanets
		self.maxshare = []#[-1 ,-1, False]#idofplanet, currmaxshare, dead heat
		self.scores = []#numcoll*thesevenplanets
		self.maxscore = []#[-1, -1, False]
		self.degwinner = []
		degwin = [[-1,0],[-1,0],[-1,0]]

		numcoll = len(self.collections)
		for i in range(numcoll):
			subnumcoll = len(self.collections[i])
			plshares = [0,0,0,0,0,0,0]
			plscores = [0,0,0,0,0,0,0]
			maxsh = [-1 ,-1, False]
			maxsc = [-1 ,-1, False]
			cdegwinner = []
			tdata = []
			for j in range(astrology.SE_SATURN+1):
				score = []
				scoretxt = []
				for k in range(subnumcoll):
					score.append(0)
					scoretxt.append('')
					if j == 0:
						cdegwinner.append(copy.deepcopy(degwin))

				dat = []
				for k in range(subnumcoll):
					lon = self.collections[i][k] #no Ayanamsha here!
					s, st, sh = self.getData(j, lon, daytime)
					score[k] += s
					plscores[j] += s
					scoretxt[k] += st
					plshares[j] += sh

					if score[k] > cdegwinner[k][0][1]:
						cdegwinner[k][0][0] = j
						cdegwinner[k][0][1] = score[k]
						cdegwinner[k][1][0] = -1
						cdegwinner[k][2][0] = -1
					elif score[k] == cdegwinner[k][0][1]:
						if cdegwinner[k][1][0] == -1:
							cdegwinner[k][1][0] = j
						else:
							cdegwinner[k][2][0] = j

					dat.append((scoretxt[k], score[k]),)

				tdata.append(tuple(dat))

				if maxsh[1] == plshares[j]:
					maxsh[2] = True
				elif maxsh[1] < plshares[j]:
					maxsh[2] = False
					maxsh[0] = j
					maxsh[1] = plshares[j]

				if maxsc[1] == plscores[j]:
					maxsc[2] = True
				elif maxsc[1] < plscores[j]:
					maxsc[2] = False
					maxsc[0] = j
					maxsc[1] = plscores[j]

			self.data.append(tuple(tdata))
			self.degwinner.append(tuple(copy.deepcopy(cdegwinner)))
			self.shares.append(plshares)
			self.scores.append(plscores)
			self.maxshare.append(tuple(maxsh))
			self.maxscore.append(tuple(maxsc))


	def getLon(self, chrt, typ, val, rul, daytime):
		ok = True
		lons = []
		lon = 0.0
		if typ == Topicals.PLANET:
			ok, lon = self.getLonSub(chrt, chrt.planets.planets[val].data[planets.Planet.LONG], rul, daytime)
			if ok:
				lons.append(lon)
		elif typ == Topicals.PLANETS:
			for i in range(astrology.SE_SATURN+1):
				pllon = chrt.planets.planets[i].data[planets.Planet.LONG]
				housenum = chrt.houses.getHousePos(pllon, chrt.options, True)
				if housenum == val:
					lons.append(pllon)
		elif typ == Topicals.HOUSECUSP:
			ok, lon = self.getLonSub(chrt, chrt.houses.cusps[val+1], rul, daytime)
			if ok:
				lons.append(lon)
		elif typ == Topicals.ARABICPART:
			longitude = chrt.fortune.fortune[fortune.Fortune.LON]
			if val > 0:
				longitude = chrt.parts.parts[val-1][arabicparts.ArabicParts.LONG]
			ok, lon = self.getLonSub(chrt, longitude, rul, daytime)
			if ok:
				lons.append(lon)
		elif typ == Topicals.SYZYGY:
			ok, lon = self.getLonSub(chrt, chrt.syzygy.lons[val], rul, daytime)
			if ok:
				lons.append(lon)
		elif typ == Topicals.LIGHTOFTHETIME:
			abovehorizonSun = chrt.planets.planets[astrology.SE_SUN].abovehorizon
			if chrt.options.usedaynightorb:
				abovehorizonSun = chrt.abovehorizonwithorb

			longitude = chrt.planets.planets[astrology.SE_SUN].data[planets.Planet.LONG]
			if not abovehorizonSun:
				longitude = chrt.planets.planets[astrology.SE_MOON].data[planets.Planet.LONG]

			ok, lon = self.getLonSub(chrt, longitude, rul, daytime)
			if ok:
				lons.append(lon)

		return ok, lons


	def getLonSub(self, chrt, lon, rul, daytime):
		ok = True
		if rul == Topicals.SELF:
			pass 
		elif rul == Topicals.SIGN:
			sign = int(lon/chart.Chart.SIGN_DEG)
			lon = chrt.planets.planets[self.doms[sign]].data[planets.Planet.LONG]
		elif rul == Topicals.EXALTATION:
			sign = int(lon/chart.Chart.SIGN_DEG)
			lon = chrt.planets.planets[self.exals[sign]].data[planets.Planet.LONG]
		elif rul == Topicals.TRIPLICITY1:
			sign = int(lon/chart.Chart.SIGN_DEG)
			tr = self.tripls[sign]
			tripl = 0
			if daytime:
				tripl = chrt.options.trips[chrt.options.seltrip][tr][0]
			else:
				tripl = chrt.options.trips[chrt.options.seltrip][tr][1]
			lon = chrt.planets.planets[tripl].data[planets.Planet.LONG]
		elif rul == Topicals.TRIPLICITY2:
			sign = int(lon/chart.Chart.SIGN_DEG)
			tr = self.tripls[sign]
			tripl = 0
			if daytime:
				tripl = chrt.options.trips[chrt.options.seltrip][tr][1]
			else:
				tripl = chrt.options.trips[chrt.options.seltrip][tr][0]
			lon = chrt.planets.planets[tripl].data[planets.Planet.LONG]
		elif rul == Topicals.TRIPLICITY3:
			sign = int(lon/chart.Chart.SIGN_DEG)
			tr = self.tripls[sign]
			tripl = 0
			tripl = chrt.options.trips[chrt.options.seltrip][tr][2]
			if tripl == 7:
				ok = False
			else:
				lon = chrt.planets.planets[tripl].data[planets.Planet.LONG]
		elif rul == Topicals.TERM:
			sign = int(lon/chart.Chart.SIGN_DEG)
			pos = lon%chart.Chart.SIGN_DEG

			subnum = len(chrt.options.terms[0][0])
			summa = 0.0
			for t in range(subnum):
				summa += chrt.options.terms[chrt.options.selterm][sign][t][1]#degs
				if summa > pos:
					break

			term = chrt.options.terms[chrt.options.selterm][sign][t][0]#planet
			lon = chrt.planets.planets[term].data[planets.Planet.LONG]
		elif rul == Topicals.DECAN:
			sign = int(lon/chart.Chart.SIGN_DEG)
			pos = lon%chart.Chart.SIGN_DEG
			dec = int(pos/10)
			decan = chrt.options.decans[chrt.options.seldecan][sign][dec]
			lon = chrt.planets.planets[decan].data[planets.Planet.LONG]

		if chrt.options.ayanamsha != 0:
			lon = util.normalize(lon-chrt.ayanamsha)

		return ok, lon


	def getData(self, i, lon, daytime):
		'''i is the index of the planet, and lon is the longitude to check'''

		score = 0
		scoretxt = ''
		share = 0

		sign = int(lon/chart.Chart.SIGN_DEG)
		if i == self.doms[sign]:
			sc = self.chart.options.dignityscores[0]
			score += sc
			add = '+'
			if scoretxt == '':
				add = ''
			scoretxt += add+str(sc)
			share += 1
		if self.exals[sign] != -1 and i == self.exals[sign]:
			mercuryinvirgo = sign == 5 and i == 2
			if not mercuryinvirgo or (mercuryinvirgo and self.chart.options.useexaltationmercury):
				sc = self.chart.options.dignityscores[1]
				score += sc
				add = '+'
				if scoretxt == '':
					add = ''
				scoretxt += add+str(sc)
				share += 1
		if self.chart.options.oneruler:
			tr = self.tripls[sign]
			tripl = 0
			if daytime:
				tripl = self.chart.options.trips[self.chart.options.seltrip][tr][0]
			else:
				tripl = self.chart.options.trips[self.chart.options.seltrip][tr][1]

			if tripl == i:
				sc = self.chart.options.dignityscores[2]
				score += sc
				add = '+'
				if scoretxt == '':
					add = ''
				scoretxt += add+str(sc)
				share += 1
		else:
			tr = self.tripls[sign]
			for k in range(3):#3 is the maximum number of triplicity rulers
				tripl = self.chart.options.trips[self.chart.options.seltrip][tr][k]

				if tripl != -1 and tripl == i:
					sc = self.chart.options.dignityscores[2]
					score += sc 
					add = '+'
					if scoretxt == '':
						add = ''
					scoretxt += add+str(sc)
					share += 1
					break

		pos = lon%chart.Chart.SIGN_DEG

		subnum = len(self.chart.options.terms[0][0])
		summa = 0.0
		for t in range(subnum):
			summa += self.chart.options.terms[self.chart.options.selterm][sign][t][1]#degs
			if summa > pos:
				break

		term = self.chart.options.terms[self.chart.options.selterm][sign][t][0]#planet
		if term == i:
			sc = self.chart.options.dignityscores[3]
			score += sc
			add = '+'
			if scoretxt == '':
				add = ''
			scoretxt += add+str(sc)
			share += 1

		dec = int(pos/10)
		decan = self.chart.options.decans[self.chart.options.seldecan][sign][dec]
		if decan == i:
			sc = self.chart.options.dignityscores[4]
			score += sc
			add = '+'
			if scoretxt == '':
				add = ''
			scoretxt += add+str(sc)
			share += 1

		return score, scoretxt, share


#recalc in case of almuten-options, syzygy, lof, housesystem, orb or/and appearanceI(traditional) change
class Almutens:
	'''Calculates the Almuten of the Chart'''

	def __init__(self, chrt):
		self.essentials = Essentials(chrt)
		self.accidentals = Accidentals(chrt)

		self.scores = []
		for i in range(astrology.SE_SATURN+1):
			self.scores.append(self.essentials.scores[i])
			self.scores[i] += self.accidentals.inhouses[i]
			self.scores[i] += self.accidentals.dayruler[i]
			self.scores[i] += self.accidentals.hourruler[i]

		for i in range(astrology.SE_MARS, astrology.SE_SATURN+1):
			self.scores[i] += self.accidentals.inphases[i-astrology.SE_MARS]	

		self.maxscore = [-1,-1, False]
		for i in range(astrology.SE_SATURN+1):
			if self.maxscore[1] == self.scores[i]:
				self.maxscore[2] = True
			elif self.maxscore[1] < self.scores[i]:
				self.maxscore[2] = False
				self.maxscore[0] = i
				self.maxscore[1] = self.scores[i]

		self.topicals = None
		if chrt.options.topicals != None:
			self.topicals = Topicals(chrt)






