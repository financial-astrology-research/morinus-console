import math
import astrology
import houses
import planets
import chart
import placspec
import regiospec
import util


class Fortune:
	'''Computes Lot-of-Fortune'''
	LON = 0
	LAT = 1
	RA = 2
	DECL = 3

	def __init__(self, typ, ascmc2, raequasc, pls, obl, placelat, abovehorizon):
		self.fortune = [0.0, 0.0, 0.0, 0.0]

		self.abovehorizon = abovehorizon	

		if typ == chart.Chart.LFMOONSUN:
			diff = pls.planets[astrology.SE_MOON].data[planets.Planet.LONG]-pls.planets[astrology.SE_SUN].data[planets.Planet.LONG]
			if diff < 0.0:
				diff += 360.0
			self.fortune[Fortune.LON] = ascmc2[houses.Houses.ASC][houses.Houses.LON]+diff
			if self.fortune[Fortune.LON] > 360.0:
				self.fortune[Fortune.LON] -= 360.0
		elif typ == chart.Chart.LFDSUNMOON:
			diff = 0.0
			if abovehorizon:
				diff = pls.planets[astrology.SE_SUN].data[planets.Planet.LONG]-pls.planets[astrology.SE_MOON].data[planets.Planet.LONG]
			else:
				diff = pls.planets[astrology.SE_MOON].data[planets.Planet.LONG]-pls.planets[astrology.SE_SUN].data[planets.Planet.LONG]

			if diff < 0.0:
				diff += 360.0
			self.fortune[Fortune.LON] = ascmc2[houses.Houses.ASC][houses.Houses.LON]+diff
			if self.fortune[Fortune.LON] > 360.0:
				self.fortune[Fortune.LON] -= 360.0
		elif typ == chart.Chart.LFDMOONSUN:
			diff = 0.0
			if abovehorizon:
				diff = pls.planets[astrology.SE_MOON].data[planets.Planet.LONG]-pls.planets[astrology.SE_SUN].data[planets.Planet.LONG]
			else:
				diff = pls.planets[astrology.SE_SUN].data[planets.Planet.LONG]-pls.planets[astrology.SE_MOON].data[planets.Planet.LONG]

			if diff < 0.0:
				diff += 360.0
			self.fortune[Fortune.LON] = ascmc2[houses.Houses.ASC][houses.Houses.LON]+diff
			if self.fortune[Fortune.LON] > 360.0:
				self.fortune[Fortune.LON] -= 360.0

		self.fortune[Fortune.RA], self.fortune[Fortune.DECL], distprom = astrology.swe_cotrans(self.fortune[Fortune.LON], 0.0, 1.0, -obl)

		self.speculum = placspec.PlacidianSpeculum(placelat, ascmc2, self.fortune[Fortune.LON], self.fortune[Fortune.LAT], self.fortune[Fortune.RA], self.fortune[Fortune.DECL])
		self.speculum2 = regiospec.RegiomontanianSpeculum(placelat, ascmc2, raequasc, self.fortune[Fortune.LON], self.fortune[Fortune.LAT], self.fortune[Fortune.RA], self.fortune[Fortune.DECL])


	def calcProfPos(self, prof):
		self.fortune = (util.normalize(self.fortune[Fortune.LON]+prof.offs), self.fortune[Fortune.LAT], self.fortune[Fortune.RA], self.fortune[Fortune.DECL])


	def calcMundaneProfPos(self, ascmc2, fort, placelat, obl):
		ramc = ascmc2[houses.Houses.MC][houses.Houses.RA]
		raic = ramc+180.0
		if raic > 360.0:
			raic -= 360.0

		md = fort.speculum.speculum[placspec.PlacidianSpeculum.MD]
		if md < 0.0:
			md *= -1
		ra = fort.speculum.speculum[placspec.PlacidianSpeculum.RA]

		if fort.speculum.speculum[placspec.PlacidianSpeculum.PMP] < 90.0:
			ra = raic-md
		elif fort.speculum.speculum[placspec.PlacidianSpeculum.PMP] >= 90.0 and fort.speculum.speculum[placspec.PlacidianSpeculum.PMP] < 180.0:
			ra = raic+md
		elif fort.speculum.speculum[placspec.PlacidianSpeculum.PMP] >= 180.0 and fort.speculum.speculum[placspec.PlacidianSpeculum.PMP] < 270.0:
			ra = ramc-md
		elif fort.speculum.speculum[placspec.PlacidianSpeculum.PMP] >= 270.0 and fort.speculum.speculum[placspec.PlacidianSpeculum.PMP] < 360.0:
			ra = ramc+md

		ra = util.normalize(ra)

		ao = do = 0.0
		adph = math.fabs(fort.speculum.speculum[placspec.PlacidianSpeculum.ADPH])#####
		if placelat == 0.0 or fort.speculum.speculum[placspec.PlacidianSpeculum.DECL] == 0.0:
			ao = do = ra
		if (placelat > 0.0 and fort.speculum.speculum[placspec.PlacidianSpeculum.DECL] > 0.0) or (placelat < 0.0 and fort.speculum.speculum[placspec.PlacidianSpeculum.DECL] < 0.0):
			ao = ra-adph
			do = ra+adph
		if (placelat > 0.0 and fort.speculum.speculum[placspec.PlacidianSpeculum.DECL] < 0.0) or (placelat < 0.0 and fort.speculum.speculum[placspec.PlacidianSpeculum.DECL] > 0.0):
			ao = ra+adph
			do = ra-adph

		ao = util.normalize(ao)
		do = util.normalize(do)

		poh = fort.speculum.speculum[placspec.PlacidianSpeculum.POH]
		rao = math.radians(ao)
		rdo = math.radians(do)
		robl = math.radians(obl)
		rpoh = math.radians(poh)
		lon = fort.speculum.speculum[placspec.PlacidianSpeculum.LON]
		okGa, okGd, lon = self.iterate(fort, rao, rdo, robl, rpoh, lon)
		if not okGa:
			rao1 = rao+math.radians(0.5)
			lon1 = self.iterate(fort, rao1, rdo, robl, rpoh, lon)
			rao2 = rao-math.radians(0.5)
			lon2 = self.iterate(fort, rao2, rdo, robl, rpoh, lon)
			lon = (lon1+lon2)/2
			lon = util.normalize(lon)
		elif not okGd:
			rdo1 = rdo+math.radians(0.5)
			lon1 = self.iterate(fort, rao, rdo1, robl, rpoh, lon)
			rdo2 = rdo-math.radians(0.5)
			lon2 = self.iterate(fort, rao, rdo2, robl, rpoh, lon)
			lon = (lon1+lon2)/2
			lon = util.normalize(lon)

		lat = fort.fortune[Fortune.LAT]
		decl = fort.fortune[Fortune.DECL]
		self.fortune = [lon, lat, ra, decl]


	def iterate(self, fort, rao, rdo, robl, rpoh, lon):
		
		okGa = okGd = True

		pmp = fort.speculum.speculum[placspec.PlacidianSpeculum.PMP]
		if pmp < 90.0 or (pmp >= 270.0 and pmp < 360.0):
			Ga = math.degrees(math.cos(rao)*math.cos(robl)-math.sin(robl)*math.tan(rpoh))
			if Ga != 0.0:
				Fa = math.degrees(math.atan(math.sin(rao)/(math.cos(rao)*math.cos(robl)-math.sin(robl)*math.tan(rpoh))))

				if Fa >= 0.0 and Ga > 0.0:
					lon = Fa
				elif Fa < 0.0 and Ga > 0.0:
					lon = Fa+360.0
				elif Ga < 0.0:
					lon = Fa+180.0
			else:
				okGa = False
		else:
			Gd = math.degrees(math.cos(rdo)*math.cos(robl)+math.sin(robl)*math.tan(rpoh))
			if Gd != 0.0:
				Fd = math.degrees(math.atan(math.sin(rdo)/(math.cos(rdo)*math.cos(robl)+math.sin(robl)*math.tan(rpoh))))

				if Fd >= 0.0 and Gd > 0.0:
					lon = Fd
				elif Fd < 0.0 and Gd > 0.0:
					lon = Fd+360.0
				elif Gd < 0.0:
					lon = Fd+180.0
			else:
				okGd = False

		return okGa, okGd, lon


	def calcFullAstronomicalProc(self, fort, da, oblN):#, raN, declN):
		raN = fort.fortune[Fortune.RA]
		declN = fort.fortune[Fortune.DECL]

		ksi = raN+da
		ksi = util.normalize(ksi)

		roblN = math.radians(oblN)
		rksi = math.radians(ksi)
		rdeclN = math.radians(declN)
		longSZ = 0.0
		if ksi == 90.0:
			longSZ = 90.0
		elif ksi == 270.0:
			longSZ = 270.0
		else:
			Fd = 0.0
			if math.cos(rksi) != 0.0:
				Fd = math.degrees(math.atan((math.cos(roblN)*math.sin(rksi)+math.sin(roblN)*math.tan(rdeclN))/math.cos(rksi)))

			if ksi >= 0.0 and ksi < 90.0:
				longSZ = Fd
			elif ksi > 90.0 and ksi < 270.0:
				longSZ = Fd+180.0
			elif ksi > 270.0 and ksi < 360.0:
				longSZ = Fd+360.0

			if longSZ <= 0.0:
				longSZ = Fd+360.0

		latSZ = math.degrees(math.asin(math.sin(rdeclN)*math.cos(roblN)-math.cos(rdeclN)*math.sin(rksi)*math.sin(roblN)))
		raSZ, declSZ, distSZ = astrology.swe_cotrans(longSZ, latSZ, 1.0, -oblN)

		self.fortune = [longSZ, latSZ, raSZ, declSZ]


	def recalcForMundaneChart(self, lon, lat, ra, decl, ascmc2, raequasc, obl, placelat):
		self.fortune = [lon, lat, ra, decl]

		self.speculum = placspec.PlacidianSpeculum(placelat, ascmc2, self.fortune[Fortune.LON], self.fortune[Fortune.LAT], self.fortune[Fortune.RA], self.fortune[Fortune.DECL])
		self.speculum2 = regiospec.RegiomontanianSpeculum(placelat, ascmc2, raequasc, self.fortune[Fortune.LON], self.fortune[Fortune.LAT], self.fortune[Fortune.RA], self.fortune[Fortune.DECL])


	def calcRegioPDsInChartsPos(self, ascmc2, fort, placelat, obl):
		ramc = ascmc2[houses.Houses.MC][houses.Houses.RA]
		raic = ramc+180.0
		if raic > 360.0:
			raic -= 360.0

		md = fort.speculum.speculum[placspec.PlacidianSpeculum.MD]
		if md < 0.0:
			md *= -1
		ra = fort.speculum.speculum[placspec.PlacidianSpeculum.RA]

		if fort.speculum.speculum[placspec.PlacidianSpeculum.PMP] < 90.0:
			ra = raic-md
		elif fort.speculum.speculum[placspec.PlacidianSpeculum.PMP] >= 90.0 and fort.speculum.speculum[placspec.PlacidianSpeculum.PMP] < 180.0:
			ra = raic+md
		elif fort.speculum.speculum[placspec.PlacidianSpeculum.PMP] >= 180.0 and fort.speculum.speculum[placspec.PlacidianSpeculum.PMP] < 270.0:
			ra = ramc-md
		elif fort.speculum.speculum[placspec.PlacidianSpeculum.PMP] >= 270.0 and fort.speculum.speculum[placspec.PlacidianSpeculum.PMP] < 360.0:
			ra = ramc+md

		ra = util.normalize(ra)

		qreg = math.fabs(fort.speculum2.speculum[regiospec.RegiomontanianSpeculum.Q])#####
		wa = wd = 0.0
		if placelat == 0.0 or fort.speculum.speculum[placspec.PlacidianSpeculum.DECL] == 0.0:
			wa = ra
			wd = ra
		if (placelat > 0.0 and fort.speculum.speculum[placspec.PlacidianSpeculum.DECL] > 0.0) or (placelat < 0.0 and fort.speculum.speculum[placspec.PlacidianSpeculum.DECL] < 0.0):
			wa = ra-qreg
			wd = ra+qreg
		if (placelat > 0.0 and fort.speculum.speculum[placspec.PlacidianSpeculum.DECL] < 0.0) or (placelat < 0.0 and fort.speculum.speculum[placspec.PlacidianSpeculum.DECL] > 0.0):
			wa = ra+qreg
			wd = ra-qreg

		wa = util.normalize(wa)
		wd = util.normalize(wd)

		poh = fort.speculum2.speculum[regiospec.RegiomontanianSpeculum.POLE]
		rwa = math.radians(wa)
		rwd = math.radians(wd)
		robl = math.radians(obl)
		rpoh = math.radians(poh)
		lon = fort.speculum.speculum[placspec.PlacidianSpeculum.LON]
		okGa, okGd, lon = self.iterateRegio(fort, rwa, rwd, robl, rpoh, lon)
		if not okGa:
			rwa1 = rwa+math.radians(0.5)
			lon1 = self.iterateRegio(fort, rwa1, rwd, robl, rpoh, lon)
			rwa2 = rwa-math.radians(0.5)
			lon2 = self.iterateRegio(fort, rwa2, rwd, robl, rpoh, lon)
			lon = (lon1+lon2)/2
			lon = util.normalize(lon)
		elif not okGd:
			rwd1 = rwd+math.radians(0.5)
			lon1 = self.iterateRegio(fort, rwa, rwd1, robl, rpoh, lon)
			rwd2 = rwd-math.radians(0.5)
			lon2 = self.iterateRegio(fort, rwa, rwd2, robl, rpoh, lon)
			lon = (lon1+lon2)/2
			lon = util.normalize(lon)

		lat = fort.fortune[Fortune.LAT]
		decl = fort.fortune[Fortune.DECL]
		self.fortune = [lon, lat, ra, decl]


	def iterateRegio(self, fort, rwa, rwd, robl, rpoh, lon):
		
		okGa = okGd = True

		pmp = fort.speculum.speculum[placspec.PlacidianSpeculum.PMP]
		if pmp < 90.0 or (pmp >= 270.0 and pmp < 360.0):
			Ga = math.degrees(math.cos(rwa)*math.cos(robl)-math.sin(robl)*math.tan(rpoh))
			if Ga != 0.0:
				Fa = math.degrees(math.atan(math.sin(rwa)/(math.cos(rwa)*math.cos(robl)-math.sin(robl)*math.tan(rpoh))))

				if Fa >= 0.0 and Ga > 0.0:
					lon = Fa
				elif Fa < 0.0 and Ga > 0.0:
					lon = Fa+360.0
				elif Ga < 0.0:
					lon = Fa+180.0
			else:
				okGa = False
		else:
			Gd = math.degrees(math.cos(rwd)*math.cos(robl)+math.sin(robl)*math.tan(rpoh))
			if Gd != 0.0:
				Fd = math.degrees(math.atan(math.sin(rwd)/(math.cos(rwd)*math.cos(robl)+math.sin(robl)*math.tan(rpoh))))

				if Fd >= 0.0 and Gd > 0.0:
					lon = Fd
				elif Fd < 0.0 and Gd > 0.0:
					lon = Fd+360.0
				elif Gd < 0.0:
					lon = Fd+180.0
			else:
				okGd = False

		return okGa, okGd, lon





