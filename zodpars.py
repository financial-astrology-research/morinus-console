import astrology
import planets
import zodparsbase


class ZodPars(zodparsbase.ZodParsBase):
	"""Computes zodiacal parallels"""

	def __init__(self, pls, obl):
		zodparsbase.ZodParsBase.__init__(self, obl)

		self.pls = pls
		self.pars = []

		self.calc()
	

	def calc(self):
		NODES = 2

		for p in range(planets.Planets.PLANETS_NUM-NODES):#Nodes are excluded
			pl = self.pls.planets[p]

			onEcl = False
			if p == astrology.SE_SUN or pl.speculums[0][planets.Planet.LAT] == 0.0:
				onEcl = True
			self.pars.append(self.getEclPoints(pl.speculums[0][planets.Planet.LONG], pl.speculums[0][planets.Planet.DECL], onEcl))





