import astrology
import planets
import zodparsbase


class AntZodPars(zodparsbase.ZodParsBase):
	"""Computes zodiacal parallels of the antiscia of the planets"""

	def __init__(self, ant, cant, obl):
		zodparsbase.ZodParsBase.__init__(self, obl)

		self.ant = ant
		self.cant = cant
		self.apars = []
		self.cpars = []

		self.calc()
	

	def calc(self):
		NODES = 2

		for p in range(planets.Planets.PLANETS_NUM-NODES):#Nodes are excluded
			lon = self.ant[p].lon
			lat = self.ant[p].lat
			decl = self.ant[p].decl

			onEcl = False
			if p == astrology.SE_SUN or lat == 0.0:
				onEcl = True
			self.apars.append(self.getEclPoints(lon, decl, onEcl))

		for p in range(planets.Planets.PLANETS_NUM-NODES):#Nodes are excluded
			lon = self.cant[p].lon
			lat = self.cant[p].lat
			decl = self.cant[p].decl

			onEcl = False
			if p == astrology.SE_SUN or lat == 0.0:
				onEcl = True
			self.cpars.append(self.getEclPoints(lon, decl, onEcl))



